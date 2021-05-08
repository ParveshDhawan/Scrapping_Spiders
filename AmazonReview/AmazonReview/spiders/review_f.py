# -*- coding: utf-8 -*-
import scrapy


class ReviewFSpider(scrapy.Spider):
    name = 'review_f'
    allowed_domains = ['www.flipkart.com']
    start_urls = ['http://www.flipkart.com/']

    def parse(self, response):
        pass
