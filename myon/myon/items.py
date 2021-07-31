# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ContentItem(scrapy.Item):
    book_id = scrapy.Field()
    content = scrapy.Field()


class Mp4Item(scrapy.Item):
    file_urls = scrapy.Field()
    fields = scrapy.Field()
    folder = scrapy.Field()
