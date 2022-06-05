# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from HuXiu.items import HuXiuItem
import re
from scrapy.utils.response import body_or_str

class HuXiu(scrapy.Spider):
    name = 'HuXiu'
    allowed_domains = []
    #280001.html
    start_urls = ['https://www.huxiu.com/article/']
    model_urls = []

    def parse(self, response):
        for i in range(280001, 565000, 3):
            url = self.start_urls[0]+str(i)+'.html'
            item = HuXiuItem()
            item['url'] = url
            yield scrapy.Request(url, self.parseList, meta={'item': item})

    def parseList(self, response):
        print(response)
        time = response.xpath('//*[@id="js-article-read-wrap"]/span/text()').extract()
        time = ''.join(time)

        title = response.xpath('//*[@id="js-article-read-wrap"]/h1/text()').extract()
        title = ''.join(title)

        source = response.xpath('//*[@id="js-article-read-wrap"]/div[1]/a/span[1]/text()').extract()
        source = ''.join(source)

        desc_info = response.xpath('//*[@id="article-content"]')
        desc_ = desc_info.xpath('string(.)').extract()
        content = ""
        for description in desc_:
            description_ = description.strip()
            content = content.join(description_)
        content = ''.join(content)

        item = response.meta['item']
        print(item["url"])
        item['source'] = source
        item['content'] = content
        item['time'] = time
        item['title'] = title
        yield item

    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='C:\\Users\\76512\\template\\chromedriver.exe')
