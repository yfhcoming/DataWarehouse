# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmzspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    title = scrapy.Field()
    otherFormat = scrapy.Field()  # DVD, VHS Tape, etc.

    primeMeta = scrapy.Field()  # only in prime video

    format = scrapy.Field()
    productDetail = scrapy.Field()
    additionalOptions = scrapy.Field()  # DVD1, DVD2, etc.
    pass
