import scrapy


class VesselfinderSpider(scrapy.Spider):
    name = 'VesselFinder'
    allowed_domains = ['www.vesselfinder.com']
    start_urls = ['http://www.vesselfinder.com/']

    def parse(self, response):
        pass
