import scrapy


class ShiptackSpider(scrapy.Spider):
    name = 'shiptack'
    allowed_domains = ['www.myshiptracking.com']
    start_urls = ['http://www.myshiptracking.com/']

    def parse(self, response):
        pass
