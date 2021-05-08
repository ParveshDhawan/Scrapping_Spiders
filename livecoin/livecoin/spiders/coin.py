# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

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
            rur_tab[4]:mouse_click()
            assert(splash:wait(2))
            splash:set_viewport_full()
            return splash:html()
        end
    '''
    def start_requests(self):
        yield SplashRequest(url = 'https://www.livecoin.net/en', callback=self.parse, endpoint="execute", args={
            'lua_source' : self.script,
        })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get(),
                'Last Price' : currency.xpath(".//div[3]/span/text()").get(),
                'Change (24h)' : currency.xpath(".//div[4]/span/span/text()").get(),
                'High (24h)' : currency.xpath(".//div[5]/span/text()").get(),
                'Low (24h)' : currency.xpath(".//div[6]/span/text()").get(),
            }