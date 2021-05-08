# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CointestItem(scrapy.Item):
    # define the fields for your item here like:
    currency_pair = scrapy.Field()
    volume_24h = scrapy.Field()
    Last_Price = scrapy.Field()
    Change_24h = scrapy.Field()
    High_24h = scrapy.Field()
    Low_24h = scrapy.Field()
    # pass