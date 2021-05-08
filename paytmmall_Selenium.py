# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time

class PaytmmallSpider(scrapy.Spider):
    name = 'paytmmall'
    allowed_domains = ['www.paytmmall.com']
    # start_urls = ['http://www.paytmmall.com/']

    def start_requests(self):
        yield SeleniumRequest(url=self.main_url,wait_time=3,screenshot=True,callback=self.parse)

    def parse(self, response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        if response_obj.xpath("//div[@class='o83B']/div[2]/span[2]"):
            if int(re.findall(r'\d+',response_obj.xpath("//div[@class='o83B']/div[2]/span[2]").get())[0]) <= 3:
                for review in response_obj.xpath("//div[@class='Ff8R']"):
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
                # find_all_review = driver.find_element_by_xpath("//a[@class='_2Fho']")
                # find_all_review.click()
                # yield scrapy.Request(url=,wait_time=3,screenshot=True,callback=self.parse)
                # time.sleep(2)

                # html = driver.page_source
                # response_obj = Selector(text=html)
                print(response.urljoin(response_obj.xpath("//a[@class='_2Fho']/@href").get())) 
                yield SeleniumRequest(url=response.urljoin(response_obj.xpath("//a[@class='_2Fho']/@href").get()),
                wait_time=3,
                screenshot=True,
                callback=self.parse_allreviews)
        else:
            #No review present
            print('No Reviews Present')
    
    def parse_allreviews(self, response):
        img = response.meta['screenshot']

        with open('screenshot.png', 'wb') as f:
            f.write(img)
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        print(response_obj)

    #     print(response.body)
    #     print('===========')
    #     # for review in response.xpath("//div[@class='Ff8R']"):
    #     #     yield{
    #     #         # 'User_Name' : review.xpath(".//div[@class='row _2pclJg']/div/p/text()").get(),
    #     #         'Rating' : review.xpath(".//div/div/text()").get(),
    #     #         # 'Rating_Title' : review.xpath("").get(),
    #     #         'Reviewed_Date': review.xpath(".//div[2]/div/text()[2]").get(),
    #     #         'Review_Context' : review.xpath(".//div/pre/text()").get(),
    #     #         # 'Helpful_Count' : review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB']/span/text()").get(),
    #     #         # 'Not_Helpful' : review.xpath(".//div[@class='row _2pclJg']/div[2]/div/div/div[@class='_2ZibVB _1FP7V7']/span/text()").get()
    #     #     }
    #     # if response.xpath("//a[text()='Next']/@href"):
    #     #     yield scrapy.Request(url=response.urljoin(response.xpath("//a[text()='Next']/@href").get()),
    #     #     callback=self.parse_allreviews,
    #     #     headers=self.HEAD)
