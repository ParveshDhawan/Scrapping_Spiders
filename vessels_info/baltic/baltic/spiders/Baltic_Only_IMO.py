import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException

class BalticOnlyImoSpider(scrapy.Spider):
    name = 'Baltic_Only_IMO'
    def start_requests(self):
        yield SeleniumRequest(
            url='http://www.balticshipping.com/vessels/',
            screenshot=True,
            callback = self.parse
        )
    def parse(self, response):
        driver = response.meta['driver']
        while True:
            try:
                page_links = [h.get_attribute('href') for h in driver.find_elements_by_xpath("//a[@class='col-sm-4 vessel-list-item']")]
                for i in page_links:
                    yield {
                        'IMO_Links':i,
                        }
                next_page = driver.find_element_by_xpath("//a[(text()= 'Next')]")
                next_page.click()
                driver.implicitly_wait(10)
            except NoSuchElementException:
                break