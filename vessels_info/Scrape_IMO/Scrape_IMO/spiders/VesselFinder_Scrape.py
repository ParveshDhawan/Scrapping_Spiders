import scrapy


class VesselfinderScrapeSpider(scrapy.Spider):
    name = 'VesselFinder_Scrape'
    allowed_domains = ['www.vesselfinder.com']
    start_urls = ['http://www.vesselfinder.com/']

    def parse(self, response):
        pass
