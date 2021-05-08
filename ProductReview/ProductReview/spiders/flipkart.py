# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import ProductreviewItem
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'

    main_url = ''
    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.main_url = category
        super().__init__(**kwargs)

    custom_settings = {'FEED_URI': 'flipkart/outputfile.json'}

    HEAD = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

    def start_requests(self):
        yield scrapy.Request(url=self.main_url,
        callback=self.parse,
        headers=self.HEAD)

    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.strip()

    def parse(self, response):
        Product_review = ProductreviewItem()
        #No review or rating
        if response.xpath("//div[@class='_1UZzwh']/span[1]/text()").get() == 'Be the first to Review this product':
            print('Be the first to Review this product')
        # no review but rating
        elif int(re.findall(r'\d+',response.xpath("//div[@class='niH0FQ _2nc08B']/span[2]/span/span[3]/text()").get())[0]) == 0:
            print("0 reviews available")
        # Single Page scrapper
        elif int(re.findall(r'\d+',response.xpath("//div[@class='niH0FQ _2nc08B']/span[2]/span/span[3]/text()").get())[0]) <= 3:
            print("Current page to scrap only")
            for review in response.xpath("//div[@class='col _390CkK']"):
                Product_review['User_Name'] = review.xpath(".//div[@class='row _2pclJg']/div/p/text()").get(),
                Product_review['Rating'] = review.xpath(".//div/div/text()").get(),
                Product_review['Rating_Title'] = review.xpath(".//div/p/text()").get(),
                Product_review['Reviewed_Date'] = review.xpath(".//div[@class='row _2pclJg']/div/p[@class='_3LYOAd']/text()").get(),
                Product_review['Review_Context'] = self.cleanhtml(review.xpath(".//div[2]/div/div/div").get()),
                Product_review['Helpful_Count'] = review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB']/span/text()").get(),
                Product_review['Not_Helpful'] = review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB _1FP7V7']/span/text()").get()
                yield Product_review

        # dig dive more than 3 available
        else:
            yield scrapy.Request(url=response.urljoin(response.xpath("//div[@class='col _39LH-M']/a/@href").get()),
            callback=self.parse_allreviews,
            headers=self.HEAD)

    def parse_allreviews(self,response):
        Product_review = ProductreviewItem()
        for review in response.xpath("//div[@class='col _390CkK _1gY8H-']"):
            Product_review['User_Name'] = review.xpath(".//div[@class='row _2pclJg']/div[1]/p/text()").get(),
            Product_review['Rating'] = review.xpath(".//div/div/text()").get(),
            Product_review['Rating_Title'] = review.xpath(".//div/p/text()").get(),
            Product_review['Reviewed_Date'] = review.xpath(".//div[@class='row _2pclJg']/div[1]/p[@class='_3LYOAd']/text()").get(),
            Product_review['Review_Context'] = self.cleanhtml(review.xpath(".//div[2]/div/div/div").get()),
            Product_review['Helpful_Count'] = review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB']/span/text()").get(),
            Product_review['Not_Helpful'] = review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB _1FP7V7']/span/text()").get()
            yield Product_review

        if response.xpath("//a[@class='_3fVaIS']/span[text()='Next']/parent::a/@href"):
            # print('New Page Found')
            yield scrapy.Request(url=response.urljoin(response.xpath("//a[@class='_3fVaIS']/span[text()='Next']/parent::a/@href").get()),
            callback=self.parse_allreviews,
            headers=self.HEAD)