    # -*- coding: utf-8 -*-
import scrapy
import re
import json
from ..items import ProductreviewItem
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class PaytmmallSpider(scrapy.Spider):
    name = 'paytmmall'

    main_url = ''
    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.main_url = category
        super().__init__(**kwargs)

    custom_settings = {'FEED_URI': 'flipkart/outputfile.json'}

    HEAD = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    
    def start_requests(self):
        print(self.main_url)
        yield scrapy.Request(url=self.main_url,callback=self.parse,headers=self.HEAD)

    def parse(self, response):
        Product_review = ProductreviewItem()
        if response.xpath("//div[@class='o83B']/div[2]/span[2]"):
            if int(re.findall(r'\d+',response.xpath("//div[@class='o83B']/div[2]/span[2]").get())[0]) <= 3:
                for review in response.xpath("//div[@class='Ff8R']"):
                    Product_review['User_Name'] = 'NA',
                    Product_review['Rating'] = review.xpath(".//div/div/text()").get(),
                    Product_review['Rating_Title'] = 'NA',
                    Product_review['Reviewed_Date'] = review.xpath(".//div[2]/div/text()[2]").get(),
                    Product_review['Review_Context'] = review.xpath(".//div/pre/text()").get(),
                    Product_review['Helpful_Count'] = 'NA',
                    Product_review['Not_Helpful'] = 'NA'
                    yield Product_review
            else:
                # print('===========')
                # print(review_url)
                # print('+++++++++++')
                reviews_count = re.findall(r'\d+',response.xpath("//div[@class='o83B']/div[2]/span[2]").get())[0]
                child_site_id = re.findall(r'&child_site_id=([0-9]*)',self.main_url)[0]
                site_id = re.findall(r'&site_id=([0-9]*)',self.main_url)[0]
                productId = re.findall(r'get_review_id=([0-9]*)',self.main_url)[0]
                review_url = str('https://paytmmall.com/proxy/review-ratings/get-product-reviews?channel=web&child_site_id='+child_site_id+'&site_id='+site_id+'&version=2&productId='+productId+'&pageSize='+reviews_count)
                # review_url = str('https://paytmmall.com/proxy/review-ratings/get-product-reviews?channel=web&child_site_id=6&site_id=2&version=2&productId='+productId+'&pageSize='+reviews_count)               
                yield scrapy.Request(url=review_url,callback=self.parse_allreviews,headers=self.HEAD,dont_filter=True)
        else:
            #No review present
            print('No Reviews Present')
    
    def parse_allreviews(self, response):
        Product_review = ProductreviewItem()
        r = json.loads(response.text)
        for i in range(len(r['reviews'])):
            Product_review['User_Name'] = 'NA',
            Product_review['Rating'] = r['reviews'][i]['rating'],
            Product_review['Rating_Title'] = 'NA',
            Product_review['Reviewed_Date'] = r['reviews'][i]['reviewDate'],
            Product_review['Review_Context'] = r['reviews'][i]['reviewDTO']['reviewDetail'],
            Product_review['Helpful_Count'] = 'NA',
            Product_review['Not_Helpful'] = 'NA'
            yield Product_review
