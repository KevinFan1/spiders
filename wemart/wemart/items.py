# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WemartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    fir_cate = scrapy.Field()
    sec_cate = scrapy.Field()
    itemCode = scrapy.Field()
    productionPlace = scrapy.Field()
    weight = scrapy.Field()
    brandName = scrapy.Field()
    fullUnitName = scrapy.Field()
    qualityDate = scrapy.Field()
    price = scrapy.Field()
    originalPrice = scrapy.Field()
    mainImage = scrapy.Field()
    url = scrapy.Field()
