# import scrapy
# from selenium import webdriver
# from template.items import TemplateItem
#
# class FoxSpider(scrapy.Spider):
#     name = 'fox'
#     #allowed_domains = ['news.163.com']
#     start_urls = ['https://news.163.com/']
#     model_urls = []
#
#     def __init__(self):
#         self.bro = webdriver.Chrome(executable_path='C:\\Users\\76512\\template\\chromedriver.exe')
#
#     def parse(self, response):
#         li_list = response.xpath('//*[@id="index2016_wrap"]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
#         a_list = [2,3]
#         for index in a_list:
#             model_url = li_list[index].xpath('./a/@href').extract_first()
#             self.model_urls.append(model_url)
#
#         for url in self.model_urls:
#             yield scrapy.Request(url, callback=self.parse_model)
#
#     def parse_model(self, response):
#         div_list = response.xpath("/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div")
#         for div in div_list:
#             title = div.xpath('./ div / div[1] / h3 / a/ text()').extract_first()
#             new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
#             print(title,new_detail_url)
#
#             item = TemplateItem()
#             item['title'] = title
#
#         yield scrapy.Request(url=new_detail_url, callback=self.parse_detail,meta={'item': item})
#
#     def parse_detail(self, response):
#         content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
#         content = ''.join(content)
#         item = response.meta['item']
#         item['content'] = content
#         yield item
#
#     def closed(self,spider):
#         self.bro.quit()

# import scrapy
# from selenium import webdriver
# from template.items import TemplateItem
#
#
# class FoxSpider(scrapy.Spider):
#     name = 'fox'
#     # allowed_domains = ['news.163.com']
#     start_urls = ['https://www.foxnews.com/sitemap.xml']
#     model_urls = []
#     model_urls_2 = []
#     url_list = ['https://www.foxnews.com/sitemap.xml?type=articles&from=1549916433000']
#
#     def __init__(self):
#         self.bro = webdriver.Chrome(executable_path='C:\\Users\\76512\\template\\chromedriver.exe')
#
#     def parse(self, response):
#         test = response.xpath('//*[@id="folder2"]/div[2]/div/span[2]/text()').extract()
#         print(test)
#         li_list = response.xpath('//*[@id="folder0"]/div[2]/div')
#         # //*[@id="folder1"]
#         # // *[ @ id = "folder130"]
#         # //*[@id="folder159"] //*[@id="folder0"]/div[2]
#         # //*[@id="folder136"]/div[2]/div/span[2]
#         num = len(li_list)
#         print(li_list)
#         for index in range(num)[29:]:
#             model_url = li_list[index].xpath('./div[2]/div/span[2]/text()').extract_first()
#             self.model_urls.append(model_url)
#
#         for url in self.model_urls:
#             yield scrapy.Request(url, callback=self.parse_model)
#
#     def parse_model(self, response):
#         # //*[@id="folder1"]
#         # //*[@id="folder0"]/div[2]
#         # //*[@id="folder1"]/div[2]/div[1]/span[2]/text()
#         div_list = response.xpath('//*[@id="folder0"]/div[2]')
#         for div in div_list:
#             model_url = div_list[div].xpath('./span[2]/text()').extract_first()
#             self.model_urls_2.append(model_url)
#         for url in self.model_urls_2:
#             item = TemplateItem()
#             item['url'] = url
#             yield scrapy.Request(url, callback=self.parse_model_2, meta={'item': item})
#
#     def parse_model_2(self, response):
#         time = response.xpath('// *[ @ id = "wrapper"] / div[2] / div[1] / main / article / header / div[1] / div[2] / time/text()').extract()
#         time = ''.join(time)
#         title = response.xpath(
#             '// *[ @ id = "wrapper"] / div[2] / div[1] / main / article / header / h1/text()').extract()
#         title = ''.join(title)
#         content = response.xpath(
#             '// *[ @ id = "wrapper"] / div[2] / div[1] / main / article / div / div[1] / div[1]/text()').extract()
#         content = ''.join(content)
#         source='foxnews'
#         item = response.meta['item']
#         item['content'] = content
#         item['time'] = time
#         item['title'] = title
#         item['content'] = content
#         item['source'] = source
#         yield  item
#
#
#
#     def parse_detail(self, response):
#         content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
#         content = ''.join(content)
#         item = response.meta['item']
#         item['content'] = content
#         yield item
#
#     def closed(self, spider):
#         self.bro.quit()
import scrapy
from selenium import webdriver
from template.items import TemplateItem
import re
from scrapy.utils.response import body_or_str
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import SitemapSpider

class FoxSpider(scrapy.Spider):
    name = 'fox'
    # allowed_domains = ['news.163.com']
    allowed_domains = []
    start_urls = ['https://www.foxnews.com/sitemap.xml?type=articles&from=1549916433000']
    model_urls = []
    model_urls_2 = []
    url_list = [
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1544720097000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1549916433000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1553519278000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1556804866000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1560013608000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1564180227000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1569201976000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1573674339000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1578735978000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1583262653000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1587394961000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1591206945000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1595289096000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1599424466000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1603731064000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1608260633000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1613041237000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1617436814000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1621964334000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1626399579000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1631028668000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1635599507000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1640797685000',
        'https://www.foxnews.com/sitemap.xml?type=articles&from=1645754286000'
                ]

    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='C:\\Users\\76512\\template\\chromedriver.exe')

    def parse(self, response):
        for url in self.url_list:
            yield scrapy.Request(url, self.parseList)

    def parse_sitemap(self, response):
        nodename = 'loc'
        text = body_or_str(response)
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield scrapy.Request(url, self.parseList)


    def parseList(self, response):
        nodename = 'loc'
        text = body_or_str(response)
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            item = TemplateItem()
            print(url)
            item['url'] = url
            yield scrapy.Request(url, self.parse_items, meta={'item': item})

    def parse_items(self, response):
       time = response.xpath('// *[ @ id = "wrapper"] / div[2] / div[1] / main / article / header / div[1] / div[2] / time/text()').extract()
       time = ''.join(time)
       title = response.xpath('// *[ @ id = "wrapper"] / div[2] / div[1] / main / article / header / h1/text()').extract()
       title = ''.join(title)

       #//*[@id="wrapper"]/div[2]/div[1]/main/article/div/div[1]/div[1]
       desc_info = response.xpath('// *[ @ id = "wrapper"] / div[2] / div[1] / main / article / div / div[1] / div[1]')
       desc_ = desc_info.xpath('string(.)').extract()
       content = ""
       for description in desc_:
           description_ = description.strip()
           content = content.join(description_)
       content = ''.join(content)

       source='foxnews'
       item = response.meta['item']
       item['content'] = content
       item['time'] = time
       item['title'] = title
       item['content'] = content
       item['source'] = source
       yield  item


    def closed(self, spider):
        self.bro.quit()
