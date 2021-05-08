# -*- coding: utf-8 -*-
import scrapy


class RiyadhSpider(scrapy.Spider):
    name = 'riyadh'
    # allowed_domains = ['www.riyadhmou.org/basicsearch.html?lang=en']
    start_urls = ['https://www.riyadhmou.org/basicsearch.html?lang=en']

    def start_requests(self):
        for url in self.start_urls:
            token, agent = cfscrape.get_tokens(url, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        yield Request(url=url, cookies=token, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' })

    def parse(self, response):
        print(response.body)
