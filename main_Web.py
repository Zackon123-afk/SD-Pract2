from scrapy.crawler import CrawlerProcess
import scrapy
from urllib.parse import urlencode
from lithops import Storage
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

BUCKET="2sdpractica"


class Reddit (scrapy.Spider):
    
    global BUCKET
    name = 'reddit_scraper'

    base_url = 'https://gateway.reddit.com/desktopapi/v1/subreddits/COVID19?'
    
    params = {
        "rtj":"only",
        "redditWebClient":"web2x",
        "app":"web2x-client-production",
        "allow_over18":"",
        "include":"prefsSubreddit",
        "after":"t3_nejiy5",
        "dist":"8",
        "layout":"card",
        "sort":"hot",
        "geo_filter":"ES"
    }
    max=35 #maximum value due to limitations of scrappy
    count=0
    titol = []
    likes = []
    post = {
        'titol': titol,
        'likes': likes
    }


    def start_requests(self):
        #generate API URL
        url = self.base_url + urlencode(self.params)
        
        #make initial HTTP request
        yield scrapy.Request(
            url=url,
            callback=self.parse_page
        )

    def parse_page(self,response):
        global BUCKET
        if (self.count<self.max) :
            json_data= json.loads(response.text)

            #loop over posts
            for post in json_data['posts']:
                posts_url = json_data['posts'][post]['permalink']

                # make HTTP request to the given post
                yield response.follow(
                    url=posts_url,
                    callback=self.parse_post
                )
                break
            #extract post urls
            # print(json_data['posts'])


            #update string query parameters
            self.params['after']= json_data['token']
            self.params['dist']= json_data['dist']

            #generate API URL
            url = self.base_url + urlencode(self.params)

            #update count
            self.count = self.count + 1

            #make recursive HTTP request to the next page
            yield scrapy.Request(
                url=url,
                callback=self.parse_page
            )
        else :
            storage = Storage()
            now = datetime.now()
            data = now.strftime("%m/%d/%Y")
            storage.put_object(BUCKET,data+"-"+"web.json",json.dumps(self.post))



    def parse_post(self,response):
        #extract data
        posts = {
            'title': response.css('h1[class="_eYtD2XCVieq6emjKBH3m"]::text').get(),
            'likes': response.css('div[class="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo"]::text').get(),
        }
        self.titol.append(response.css('h1[class="_eYtD2XCVieq6emjKBH3m"]::text').get())
        self.likes.append(response.css('div[class="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo"]::text').get())
        
        # write JSONL output
        # with open('posts.jsonl', 'a') as f:
        #     f.write(json.dumps(posts, indent=2) + '\n')
        
        print(json.dumps(posts, indent=2))

def grafic_web():
    global BUCKET

    def eliminateNaNs(list) :
        i = 0
        for x in list :
            if str(x) == 'nan':
                list[i] = 0
            i+=1
        return list

    #Treatment of json to pandas
    now = datetime.now()
    data = now.strftime("%m/%d/%Y")
    key= data+'-web.json'

    storage = Storage()
    json_read = storage.get_object(BUCKET,key)
    data_analize = json.loads(json_read)
    df = pd.DataFrame.from_dict(data_analize,orient='columns')
    df["likes"]=df["likes"].astype(int)


    # average likes about key words
    likesSARS=df[df["titol"].str.contains("SARS-CoV")].mean()["likes"]
    likesModerna=df[df["titol"].str.contains("Moderna")].mean()["likes"]
    likesPfizer=df[df["titol"].str.contains("Pfizer")].mean()["likes"]
    likesAstra=df[df["titol"].str.contains("AstraZeneca")].mean()["likes"]
    likesSputnik=df[df["titol"].str.contains("Sputnik")].mean()["likes"]
    likesJan=df[df["titol"].str.contains("Janssen")].mean()["likes"]

    name = ['SARS','Moderna','Pfizer','AstraZeneca', 'Sputnik' , 'Janssen']
    allLikes = [likesSARS,likesModerna,likesPfizer,likesAstra, likesSputnik, likesJan]
    allLikes = eliminateNaNs(allLikes)

    plt.bar(name,allLikes)
    plt.show()


if __name__ == '__main__':
    
    process = CrawlerProcess()
    process.crawl(Reddit)
    process.start()
    
    grafic_web()
