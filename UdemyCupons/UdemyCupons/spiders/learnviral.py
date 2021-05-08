# -*- coding: utf-8 -*-
import scrapy


class LearnviralSpider(scrapy.Spider):
    name = 'learnviral'
    allowed_domains = ['udemycoupon.learnviral.com']
    start_urls = ['https://udemycoupon.learnviral.com/coupon-category/free100-discount']

    def parse(self, response):
        for cupn in response.xpath("//div[@class='content-box'][2]/div[@class='box-c']/div[@class='box-holder']/div[contains(@class,'coupon type-coupon')]/div[@class='item-holder']"):
            #course_name = cupn.xpath(".//div[@class='item-frame']/div[@class='item-panel']/h3/a/text()").get()
            #cupon_url = cupn.xpath(".//div[@class='item-actions']/div[@class='couponAndTip']/div[@class='link-holder']/a/@href").get()
            yield{
                'title' : cupn.xpath(".//div[@class='item-frame']/div[@class='item-panel']/h3/a/text()").get(),#course_name,
                'cupon_URL' : cupn.xpath(".//div[@class='item-actions']/div[@class='couponAndTip']/div[@class='link-holder']/a/@href").get()#cupon_url
            }

            next_page = response.xpath("//div[@class='content-box'][2]/div[@class='box-c']/div[@class='box-holder']/div[@class='paging']/div[@class='pages']/a[@class='next page-numbers']/@href").get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
