import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException

class BalticImoOnlySpider(scrapy.Spider):
    name = 'Baltic_IMO_only'
    responses = []

    def start_requests(self):
        yield SeleniumRequest(
            url='http://www.balticshipping.com/vessels/',
            screenshot=True,
            callback = self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        self.responses.append(driver.page_source)
        while True:
            try:
                next_page = driver.find_element_by_xpath("//a[(text()= 'Next')]")
                next_page.click()
                driver.implicitly_wait(10)
                self.responses.append(driver.page_source)        
            except NoSuchElementException:
                break

        for resp in self.responses:
            r = Selector(text=resp)
            for links in r.xpath("//a[@class='col-sm-4 vessel-list-item']"):
                yield {
                    'url' : links.xpath(".//@href").get()
                }