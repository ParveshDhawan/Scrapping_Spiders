# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DatascrapperItem

class FlipkartSpider(CrawlSpider):
    name = 'flipkart'
    allowed_domains = ['www.flipkart.com']
    # start_urls = ['http://www.flipkart.com/']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url = 'https://www.flipkart.com/audio-video/headphones/pr?sid=0pm,fcn&q=HEadphones&otracker=categorytree',
        headers={'User-Agent':self.user_agent})

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//a[@class='_2cLu-l']"),
            callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(
            restrict_xpaths="//span[text()='Next']/parent::a"),process_request='set_user_agent'))

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    # Clean HTML
    def clean_html(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        tmp = TAG_RE.sub('', text)
        return re.sub(r'[^\x00-\x7F]+','',tmp)

    def remove_space(self,text):
        return re.sub(r'[^\x00-\x7F]+','',text)
        
    # CLeaning technical Specification
    def technical_clean(self,text):
        key = ['_' if len(re.findall(r'<td class="_3-wDH3 col col-3-12">(.*?)</td>',text[x])) == 0 else re.findall(r'<td class="_3-wDH3 col col-3-12">(.*?)</td>',text[x])[0] for x in range(len(text))]
        val = ['_' if len(re.findall(r'<li class="_3YhLQA">(.*?)</li>',text[x])) == 0 else re.findall(r'<li class="_3YhLQA">(.*?)</li>',text[x])[0] for x in range(len(text))]
        return list(zip(key,val)) # For csv
        # return dict(zip(key,val)) # For JSON

    # Rating Tags
    def clean_tags(self,text):
        return list(zip(re.findall(r'<div class="_3wUVEm">(.*?)</div>',text),re.findall(r'<text.*?>(.*?)<\/text>',text))) # for csv
        # return dict(zip(re.findall(r'<div class="_3wUVEm">(.*?)</div>',text),re.findall(r'<text.*?>(.*?)<\/text>',text))) # for JSON

    def parse_item(self, response):
        items = DatascrapperItem()
        items['P_Title'] = self.clean_html(str(response.xpath("//span[@class='_35KyD6']").get())),
        items['P_Url'] = response.url,
        items['P_Description'] = self.clean_html(str(response.xpath("//div[@class='_3cpW1u']/div[1]").get())),
        items['P_Rating'] = response.xpath("//div[@class='_3ors59']/div/span/div/text()").get(),
        items['P_Ratingcount'] = self.remove_space(str(response.xpath("//div[@class='_3ors59']/div/span[@class='_38sUEc']/span/span[1]/text()").get())),
        items['P_Reviewcount'] = self.remove_space(str(response.xpath("//div[@class='_3ors59']/div/span[@class='_38sUEc']/span/span[3]/text()").get())),
        items['P_Price'] = self.clean_html(str(response.xpath("//div[@class='_1vC4OE _3qQ9m1']/text()").get())),
        items['P_MRP'] = self.clean_html(str(response.xpath("//div[@class='_3auQ3N _1POkHg']").get())),
        items['P_OFF'] = response.xpath("//div[@class='VGWI6T _1iCvwn']/span/text()").get(),
        items['P_Highlights'] = response.xpath("//div[@class='_3WHvuP']/ul/li/text()").getall(),
        items['P_Services'] = response.xpath("//ul[@class='_77jr7B']/li/div[2]/text()").getall(),
        items['Seller_Name'] = response.xpath("//div[@id='sellerName']/span/span/text()").get(),
        items['Seller_Rating'] = response.xpath("//div[@class='hGSR34 YddkNl']/text()").get(),
        items['Technical_Specification'] = self.technical_clean(response.xpath("//tr[@class='_3_6Uyw row']").getall()),
        items['Customer_Ratings5star'] = response.xpath("//div[@class='_1n1j36 DrZOea uD3lY9']/ul[3]/li[1]/div/text()").get(),
        items['Customer_Ratings4star'] = response.xpath("//div[@class='_1n1j36 DrZOea uD3lY9']/ul[3]/li[2]/div/text()").get(),
        items['Customer_Ratings3star'] = response.xpath("//div[@class='_1n1j36 DrZOea uD3lY9']/ul[3]/li[3]/div/text()").get(),
        items['Customer_Ratings2star'] = response.xpath("//div[@class='_1n1j36 DrZOea uD3lY9']/ul[3]/li[4]/div/text()").get(),
        items['Customer_Ratings1star'] = response.xpath("//div[@class='_1n1j36 DrZOea uD3lY9']/ul[3]/li[5]/div/text()").get(),
        items['Customer_Ratingstags'] = self.clean_tags(str(response.xpath("//div[@class='_251bNL']").get()))
        yield items

        