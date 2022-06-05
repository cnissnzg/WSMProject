import scrapy


class SpidernameSpider(scrapy.Spider):
    name = 'spiderName'
    allowed_domains = ['www.foxnews.com']
    start_urls = ['http://www.foxnews.com/']

    def parse(self, response):
        pass
