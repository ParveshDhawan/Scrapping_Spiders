# -*- coding: utf-8 -*-
import re
from ..items import ProductreviewItem
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    main_url = ''
    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.main_url = category
        super().__init__(**kwargs)

    custom_settings = {'FEED_URI': 'amazon/outputfile.json'}
    HEAD = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    
    def start_requests(self):
        yield scrapy.Request(url=self.main_url,
        callback=self.parse,
        headers=self.HEAD)

    def parse(self, response):
        if response.xpath("//a[text()='See all reviews from India'][1]/@href"):
            all_reviews_page = response.xpath("//a[text()='See all reviews from India'][1]/@href").get()
            yield scrapy.Request(url=response.urljoin(all_reviews_page),callback=self.parse_getreviews, headers=self.HEAD)
        else:
            print('No Reviews Yet !!!')
    
    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.strip()


    def parse_getreviews(self, response):
        Product_review = ProductreviewItem()
        for review in response.xpath('//div[@class="a-row a-spacing-none"][1]'):
            Product_review['User_Name'] = review.xpath(".//div/div/a/div[2]/span/text()").get(),
            Product_review['Rating'] = review.xpath(".//div/div[@class='a-row']/a/i/span/text()").get(),
            Product_review['Rating_Title'] = review.xpath(".//div/div[@class='a-row']/a[@data-hook='review-title']/span/text()").get(),
            Product_review['Reviewed_Date'] = review.xpath(".//div/span[@class='a-size-base a-color-secondary review-date']/text()").get(),
            Product_review['Review_Context'] = self.cleanhtml(review.xpath(".//div/div[@class='a-row a-spacing-small review-data']/span/span").get()),
            Product_review['Helpful_Count'] = review.xpath(".//div/div[5]/div/span/div/span/text()").get(),
            Product_review['Not_Helpful'] = 'NA'
            yield Product_review
        
        if response.xpath("//a[text()='Next page']"):
            next_page = response.xpath("//a[text()='Next page']/@href").get()
            yield scrapy.Request(url=response.urljoin(next_page),callback=self.parse_getreviews, headers=self.HEAD)
