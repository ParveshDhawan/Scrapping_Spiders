# -*- coding: utf-8 -*-
import scrapy
import re


class PaytmmallSpider(scrapy.Spider):
    name = 'paytmmall'
    allowed_domains = ['www.paytmmall.com']
    # start_urls = ['http://www.paytmmall.com/']
    HEAD = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    
    def start_requests(self):
        yield scrapy.Request(url=self.main_url,callback=self.parse,headers=self.HEAD)

    def parse(self, response):
        if response.xpath("//div[@class='o83B']/div[2]/span[2]"):
            if int(re.findall(r'\d+',response.xpath("//div[@class='o83B']/div[2]/span[2]").get())[0]) <= 3:
                for review in response.xpath("//div[@class='Ff8R']"):
                    yield{
                        # 'User_Name' : review.xpath(".//div[@class='row _2pclJg']/div/p/text()").get(),
                        'Rating' : review.xpath(".//div/div/text()").get(),
                        # 'Rating_Title' : review.xpath("").get(),
                        'Reviewed_Date': review.xpath(".//div[2]/div/text()[2]").get(),
                        'Review_Context' : review.xpath(".//div/pre/text()").get(),
                        # 'Helpful_Count' : review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB']/span/text()").get(),
                        # 'Not_Helpful' : review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB _1FP7V7']/span/text()").get()
                    }               
            else:
                reviews_count = re.findall(r'\d+',response.xpath("//div[@class='o83B']/div[2]/span[2]").get())[0]
                child_site_id = re.findall(r'&child_site_id=([0-9]*)',self.main_url)[0]
                site_id = re.findall(r'&site_id=([0-9]*)',self.main_url)[0]
                productId = re.findall(r'product_id=([0-9]*)',self.main_url)[0]
                review_url = str('https://paytmmall.com/proxy/review-ratings/get-product-reviews?channel=web&child_site_id='+child_site_id+'&site_id='+site_id+'&version=2&productId='+productId+'&pageSize='+reviews_count)
                yield scrapy.Request(url=review_url,callback=self.parse_allreviews,headers=self.HEAD)
        else:
            #No review present
            print('No Reviews Present')
    
    def parse_allreviews(self, response):
        print(response.body)