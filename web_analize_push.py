from scrapy.crawler import CrawlerProcess
from lithops import Storage, storage
import scrapy

nom_bucket="2sdpractica"

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.reddit.com/r/COVID19/'
            #'https://www.elperiodico.com/es/temas/coronavirus-noticias-43419'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'

        storage = Storage()
        storage.put_object(nom_bucket,filename,response.body)

        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log(f'Saved file {filename}')


process = CrawlerProcess()
process.crawl(QuotesSpider) #testSpider sera el nom de la teva aranya
process.start()
