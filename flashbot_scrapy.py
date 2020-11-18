## /!\ To be run with 'scrapy runspider' (not python)

import scrapy
from scrapy import Request
from pymongo import MongoClient

class FlashbotSpider(scrapy.Spider):
    name = 'flashbot'
    ############### CONFIGURATION ########################
    #User-Agent and download-delay with required values:
    custom_settings = {'USER_AGENT': "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 OPR/59.1.2926.54067",
                       'DOWNLOAD_DELAY': '0.2'}     
    allowed_domains = ['rss.jobsearch.monster.com']
    #start_urls = ['file:///home/julien/Documents/20201112_mongodb/monster_bigdata.rss.xml']
    start_urls = ['http://rss.jobsearch.monster.com/rssquery.ashx?q={query}']
    thesaurus = ["machine learning", "big data", "deep learning"]
    
    client = MongoClient('localhost', 27017)
    db = client['flashbot']
    collection = db['jobsearch']    
    ######################################################

    def parse(self, response):
        url = self.start_urls[0]
        # Build and send a request for each word in the thesaurus
        for query in self.thesaurus:
            target = url.format(query=query)
            print("fetching the URL: %s" % target)
            if target.startswith("file://"):
                r = Request(target, callback=self.scrapit, dont_filter=True)
            else:
                r = Request(target, callback=self.scrapit)
            r.meta['query'] = query
            yield r

    def scrapit(self, response):
        query = response.meta["query"]
        for doc in response.xpath("//item"):
            item = {"query": query}
            item["title"] = doc.xpath("title/text()").extract()
            item["description"] = doc.xpath("description/text()").extract()
            item["link"] = doc.xpath("link/text()").extract()
            item["pubDate"] = doc.xpath("pubDate/text()").extract()
            item["guid"] = doc.xpath("guid/text()").extract()
            guidresult = self.collection.find({"guid": item["guid"][0]}).count()
            if guidresult == 0:
                self.collection.insert_one(item)
                print("Inserting new scraped item:", item["guid"][0])
            else:
                print("Item already known:", item["guid"][0])
            yield item
        self.client.close()
