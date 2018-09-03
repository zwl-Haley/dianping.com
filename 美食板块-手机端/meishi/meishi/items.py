# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeishiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    level = scrapy.Field()
