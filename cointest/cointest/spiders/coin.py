# -*- coding: utf-8 -*-
import scrapy,csv
from scrapy_splash import SplashRequest
from ..items import CointestItem
class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            splash:on_request(function(request)
                request:set_headers('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')  
            end)
            assert(splash:go(args.url))
            assert(splash:wait(4))
            if assert(splash:select(".showMoreContainer___2HlS0")) then
                more_tab = assert(splash:select(".showMoreContainer___2HlS0"))
                more_tab:mouse_click()
            end
            assert(splash:wait(5))
            rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            rur_tab[splash.args.num]:mouse_click()
            assert(splash:wait(2))
            splash:set_viewport_full()
            return splash:html()
        end
    '''
    f = 1
    def start_requests(self):
        yield SplashRequest(url = 'https://www.livecoin.net/en', callback=self.parse, endpoint="execute", args={
            'lua_source' : self.script, 'num':self.f
        })

    def parse(self, response):
        items = CointestItem()
        data = []
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            currency_pair = currency.xpath(".//div[1]/div/text()").get()
            volume_24h = currency.xpath(".//div[2]/span/text()").get()
            Last_Price = currency.xpath(".//div[3]/span/text()").get()
            Change_24h = currency.xpath(".//div[4]/span/span/text()").get()
            High_24h = currency.xpath(".//div[5]/span/text()").get()
            Low_24h = currency.xpath(".//div[6]/span/text()").get()

            items['currency_pair'] = currency_pair
            items['volume_24h'] = volume_24h
            items['Last_Price'] = Last_Price
            items['Change_24h'] = Change_24h
            items['High_24h'] = High_24h
            items['Low_24h'] = Low_24h

            data.append({
                'currency_pair':currency_pair,
                'volume_24h':volume_24h,
                'Last_Price':Last_Price,
                'Change_24h':Change_24h,
                'High_24h':High_24h,
                'Low_24h':Low_24h
                })

            yield items
        
        print(data)
        with open(str(self.f)+'.csv', 'w',newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[i for i in items])
            writer.writeheader()
            for d in data:
                writer.writerow(d)

        self.f = self.f+1
        if self.f < 7:           
            yield SplashRequest(url = 'https://www.livecoin.net/en', callback=self.parse, endpoint="execute", args={
            'lua_source' : self.script, 'num':self.f},
            dont_filter=True)