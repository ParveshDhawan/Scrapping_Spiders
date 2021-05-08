# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DatascrapperItem

class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['www.amazon.in']
    # start_urls = ['https://www.amazon.in']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url = 'https://www.amazon.in/s/ref=lp_1388921031_st?rh=n%3A976419031%2Cn%3A%21976420031%2Cn%3A1388921031&qid=1594237116&sort=popularity-rank&x=10&y=7',
        headers={'User-Agent':self.user_agent})

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//span[@class='a-size-medium a-color-base a-text-normal']/parent::a"),
            callback='parse_item', follow=True, process_request='set_user_agent'),
        # Rule(LinkExtractor(
        #     restrict_xpaths="//a[@id='sellerProfileTriggerId']"),callback='parse_seller',
        #     follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(
            restrict_xpaths="//a[text()='Next']"),process_request='set_user_agent'))

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    # Cleaning Price uft char
    def clean_price(self,text):
        return re.sub(r'[^\x00-\x7F]+','',text)

    # CLeaning technical Specification
    def technical_clean(self,text):
        tmp = re.findall("<td.*?>(.*?)<\/td>",text)
        key = tmp[:-2:2]
        value = [tmp[i] for i in range(len(tmp)-2) if i%2!=0]
        # return list(dict(zip(key, value)))
        return list(zip(key,value))

    def parse_item(self, response):
        items = DatascrapperItem()
        items['P_Title'] = response.xpath("normalize-space(//span[@id='productTitle']/text())").get(),
        items['P_Url'] = response.url,
        items['P_Description'] = response.xpath("normalize-space(//div[@id='productDescription']/p/text())").get(),
        items['P_Name'] = response.xpath("normalize-space(//div[@id='prodDetails']/h2/text())").get(),
        items['P_Rating'] = response.xpath("//span[@id='acrPopover']/@title").get(),
        items['P_Ratingcount'] = response.xpath("normalize-space(//span[@id='acrCustomerReviewText']/text())").get(),
        items['P_MRP'] = self.clean_price(response.xpath("normalize-space(//span[@class='priceBlockStrikePriceString a-text-strike']/text())").get()),
        items['P_Price'] = self.clean_price(response.xpath("normalize-space(//span[@class='a-size-medium a-color-price priceBlockBuyingPriceString']/text())").get()),
        items['You_Save'] = self.clean_price(response.xpath("normalize-space(//td[@class='a-span12 a-color-price a-size-base priceBlockSavingsString']/text())").get()),
        items['Technical_Specification'] = self.technical_clean(str(response.xpath("//div[@class='content pdClearfix'][1]/div[@class='attrG']/div[@class='pdTab']").get())),#response.xpath("//table[@id='productDetails_techSpec_section_1']").get(),
        items['Seller_Name'] = response.xpath("normalize-space(//a[@id='sellerProfileTriggerId']/text())").get(),
        items['Seller_Url'] = response.xpath("//a[@id='sellerProfileTriggerId']/@href").get(),
        items['Customer_Ratings5star'] = response.xpath("//table[@class='a-normal a-align-center a-spacing-base']/tr/td/span/a/@title").get(),
        items['Customer_Ratings4star'] = response.xpath("//table[@class='a-normal a-align-center a-spacing-base']/tr[2]/td/span/a/@title").get(),
        items['Customer_Ratings3star'] = response.xpath("//table[@class='a-normal a-align-center a-spacing-base']/tr[3]/td/span/a/@title").get(),
        items['Customer_Ratings2star'] = response.xpath("//table[@class='a-normal a-align-center a-spacing-base']/tr[4]/td/span/a/@title").get(),
        items['Customer_Ratings1star'] = response.xpath("//table[@class='a-normal a-align-center a-spacing-base']/tr[5]/td/span/a/@title").get()
        yield items
        # print('------------------------------------------------------__')
        # yield scrapy.Request(url=response.urljoin(response.xpath("//a[@id='sellerProfileTriggerId']/@href").get()),callback=self.parse_getsellerinfo,
        # headers={
        #         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        #         'authority': 'www.amazon.in',
        #         'upgrade-insecure-requests' : 1,
        #         'sec-fetch-user': '?1',
        #         'sec-fetch-site': 'same-origin',
        #         'sec-fetch-mode': 'navigate',
        #         'sec-fetch-dest': 'document',
        #         'rtt': '250',
        #         'ect': '4g',
        #         'downlink': 2,
        #         'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        #         'accept-encoding': 'gzip, deflate, br',
        #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #         'scheme': 'https'
        #     })
        # print('------------------------------------------------------??')
        
