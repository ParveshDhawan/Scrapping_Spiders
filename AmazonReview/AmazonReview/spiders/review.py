# -*- coding: utf-8 -*-
import scrapy


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['www.amazon.in']

    HEAD = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    #main_url = 'https://www.amazon.in/Redmi-Note-Pro-Storage-Processor/dp/B07X4PKGSN/ref=sr_1_1?dchild=1&keywords=Redmi+Note+8+Pro+%28Halo+White%2C+6GB+RAM%2C+128GB+Storage+with+Helio+G90T+Processor%29&qid=1593773378&s=electronics&sr=1-1'
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
    
    def parse_getreviews(self, response):
        for review in response.xpath('//div[@class="a-row a-spacing-none"][1]'):
            yield{
                'User_Name' : review.xpath(".//div/div/a/div[2]/span/text()").get(),
                'Rating' : review.xpath(".//div/div[@class='a-row']/a/i/span/text()").get(),
                'Rating_Title' : review.xpath(".//div/div[@class='a-row']/a[@data-hook='review-title']/span/text()").get(),
                'Reviewed_Date' : review.xpath(".//div/span[@class='a-size-base a-color-secondary review-date']/text()").get(),
                'Review_Context' : review.xpath(".//div/div[@class='a-row a-spacing-small review-data']/span/span").get(),
                'Helpful_Count' : review.xpath(".//div/div[5]/div/span/div/span/text()").get()
            }
        
        if response.xpath("//a[text()='Next page']"):
            next_page = response.xpath("//a[text()='Next page']/@href").get()
            yield scrapy.Request(url=response.urljoin(next_page),callback=self.parse_getreviews, headers=self.HEAD)
