# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json

from itemadapter import ItemAdapter


class AmzspiderPipeline:

    def __init__(self):
        self.file = codecs.open('article.json', 'wb+', encoding="utf-8")

    def process_item(self, item, spider):
        print("-------------pipeline done")
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()
