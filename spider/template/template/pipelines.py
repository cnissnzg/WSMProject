# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json

class TemplatePipeline:
    def __init__(self):
        self.file = open('foxnews.json', 'wb')

    def process_item(self, item, spider):
        print(item)
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        line = line.encode()
        self.file.write(line)
        return item
