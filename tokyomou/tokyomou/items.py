# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TokyomouItem(scrapy.Item):
    InspectionDate = scrapy.Field()
    Authority = scrapy.Field()
    Port = scrapy.Field()
    InspectionType = scrapy.Field()
    Detention = scrapy.Field()
    ShipName = scrapy.Field()
    IMONumber = scrapy.Field()
    MMSI = scrapy.Field()
    Callsign = scrapy.Field()
    ClassificationSociety = scrapy.Field()
    Flag = scrapy.Field()
    ShipType = scrapy.Field()
    DateKeelLaid = scrapy.Field()
    DWT = scrapy.Field()
    Tonnage = scrapy.Field()
    C_Name = scrapy.Field()
    C_IMONumber = scrapy.Field()
    C_Residence = scrapy.Field()
    C_Registered = scrapy.Field()
    C_Phone = scrapy.Field()
    C_Fax = scrapy.Field()
    C_Email = scrapy.Field()
    Deficiency_Count = scrapy.Field()
    Ship_Deficiencies = scrapy.Field()