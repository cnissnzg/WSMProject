# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from GlobalTimes.items import GlobaltimesItem
import re
from scrapy.utils.response import body_or_str

class GlobaltimesSpider(scrapy.Spider):
    name = 'globaltimes'
    allowed_domains = []
    start_urls = ['http://globaltimes.cn/']
    model_urls = []
    url_list = [
        'https://www.globaltimes.cn/page/202204/',#1257500-1257700
        'https://www.globaltimes.cn/page/202203/',#1254500-1254700
        'https://www.globaltimes.cn/page/202202/',#1251500-1251700
        'https://www.globaltimes.cn/page/202201/',#1245500-1245700
        'https://www.globaltimes.cn/page/202112/',#1241500-1241700
        "https://www.globaltimes.cn/page/202111/",#1239500-1239700
        'https://www.globaltimes.cn/page/202110/',#1237500-1237700
        'https://www.globaltimes.cn/page/202109/',#1234500-12314700
        'https://www.globaltimes.cn/page/202108/',#1231500-1231700
        'https://www.globaltimes.cn/page/202107/',#1228500-1228700
        'https://www.globaltimes.cn/page/202106/',#1225500 - 1225700
        'https://www.globaltimes.cn/page/202105/',#1222700 - 1222900
        'https://www.globaltimes.cn/page/202104/',#1221000 - 1221200
        'https://www.globaltimes.cn/page/202103/', #1219000-1219200
        'https://www.globaltimes.cn/page/202102/',# 1216000-1216200
        'https://www.globaltimes.cn/page/202101/',# 1213000-1213200
        'https://www.globaltimes.cn/page/202012/',#1210500-1210700
        'https://www.globaltimes.cn/page/202011/',#1207500-1207700
        'https://www.globaltimes.cn/page/202010/',#1204500-1204700
        'https://www.globaltimes.cn/page/202009/',#1201500-1201700
        'https://www.globaltimes.cn/page/202008/',#1198500-1198700
        "https://www.globaltimes.cn/page/202007/",#1195500-1195700
        'https://www.globaltimes.cn/page/202006/',#1192500-1192700
        'https://www.globaltimes.cn/page/202005/',#1189500-1189700
        'https://www.globaltimes.cn/page/202004/',#1186500-1186700
        'https://www.globaltimes.cn/page/202003/',#1183500-1183700
        'https://www.globaltimes.cn/page/202002/',#1180500-1180700
        'https://www.globaltimes.cn/page/202001/',#1177500-1177700
        'https://www.globaltimes.cn/page/201912/',#1174500-1174700
        'https://www.globaltimes.cn/page/201911/',#1169500-1169700
        'https://www.globaltimes.cn/page/201910/',#1166500-1166700
        'https://www.globaltimes.cn/page/201909/',#1163500-1163700
        'https://www.globaltimes.cn/page/201908/',#1160500-1160700
        'https://www.globaltimes.cn/page/201907/',#1157500-1157700
        'https://www.globaltimes.cn/page/201906/',#1154500-1154700
        'https://www.globaltimes.cn/page/201905/',#1151500-1151700
        'https://www.globaltimes.cn/page/201904/',#1146500-1146700
        'https://www.globaltimes.cn/page/201903/',#1143500-1143700
        'https://www.globaltimes.cn/page/201902/',#1139500-1139700
        'https://www.globaltimes.cn/page/201901/',#1136500
                ]
    index_list= [1257500,1254500,1251500,1245500,1241500,1239500,1237500,1234500,1231500,1228500,1225500,1222500,1221000,1219000,1216000,1213000,
                 1210500,1207500,1204500,1201500,1198500,1195500,1192500,1189500,1186500,1183500,1180500,1177500,1174500,1169500,1166500,
                 1163500,1160500,1157500,1154500,1151500,1146500,1143500,1139500,1136500]

    def parse(self, response):
        print(len(self.url_list))
        for i in range(len(self.url_list)):
            for j in range(200):
                url = self.url_list[i] + str(j+self.index_list[i]) + '.shtml'
                item = GlobaltimesItem()

                item['url'] = url
                yield scrapy.Request(url, self.parseList, meta={'item': item})

    def parseList(self, response):
        print(response)
        time = response.xpath('//span[@class="pub_time"]/text()').extract()
        time = ''.join(time)

        #title = response.xpath('/html/body/div[4]/div/div/div[2]/div[1]/div[2]/text()').extract()
        title = response.xpath('//div[@class="article_title"]/text()').extract()
        title = ''.join(title)

        content = ''.join(response.xpath('//div[@class="article_right"]/text()').extract()[3:])
        # desc_info = response.xpath('/html/body/div[4]/div/div/div[2]/div[2]')
        # desc_ = desc_info.xpath('string(.)').extract()
        # content = ""
        # for description in desc_:
        #     description_ = description.strip()
        #     content = content.join(description_)
        # content = ''.join(content)

        item = response.meta['item']
        print(item["url"])
        item['source'] = 'Global Times'
        item['content'] = content
        item['time'] = time
        item['title'] = title
        yield item

        # print('title',title)
        # print('time',time)
        # print('content', content)

    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='C:\\Users\\76512\\template\\chromedriver.exe')
