# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductreviewItem(scrapy.Item):
    User_Name = scrapy.Field()
    Rating = scrapy.Field()
    Rating_Title = scrapy.Field()
    Reviewed_Date = scrapy.Field()
    Review_Context = scrapy.Field()
    Helpful_Count = scrapy.Field()
    Not_Helpful = scrapy.Field()