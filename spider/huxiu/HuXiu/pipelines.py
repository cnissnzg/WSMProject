# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class HuXiuPipeline(object):
    def __init__(self):
        self.file = open('HuXiu.json', 'wb')

    def process_item(self, item, spider):
        print(item)
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        line = line.encode()
        self.file.write(line)
        return item