from scrapy.crawler import CrawlerProcess
import scrapy
from urllib.parse import urlencode
import json


class Reddit (scrapy.Spider):

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

    def start_requests(self):
        #generate API URL
        url = self.base_url + urlencode(self.params)
        
        #make initial HTTP request
        yield scrapy.Request(
            url=url,
            callback=self.parse_page
        )

    def parse_page(self,response):
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

        #make recursive HTTP request to the next page
        yield scrapy.Request(
            url=url,
            callback=self.parse_page
        )


    def parse_post(self,response):
        #extract data
        posts = {
            'title': response.css('h1[class="_eYtD2XCVieq6emjKBH3m"]::text').get(),
            'likes': response.css('div[class="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo"]::text').get(),
        }

        # write JSONL output
        with open('posts.jsonl', 'a') as f:
            f.write(json.dumps(posts, indent=2) + '\n')

        print(json.dumps(posts, indent=2))


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Reddit)
    process.start()
