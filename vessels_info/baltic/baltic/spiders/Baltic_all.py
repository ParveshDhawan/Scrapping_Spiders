import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException

class BalticAllSpider(scrapy.Spider):
    name = 'Baltic_all'
    responses = []

    def start_requests(self):
        yield SeleniumRequest(
            url='http://www.balticshipping.com/vessels/',
            # wait_time=10,
            screenshot=True,
            callback = self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        # save main_window
        main_window = driver.current_window_handle      
        while True:
            try:
                page_links = [h.get_attribute('href') for h in driver.find_elements_by_xpath("//a[@class='col-sm-4 vessel-list-item']")]
                if len(page_links) > 0:
                    driver.execute_script("window.open();")
                    driver.switch_to_window(driver.window_handles[1])
                    for i in page_links:
                        driver.get(i)
                        driver.implicitly_wait(10)
                        resp = driver.page_source
                        response_obj =Selector(text=resp)
                        yield {
                            'IMO':response_obj.xpath("(//table[1]/tbody/tr/td)[1]/text()").get(),
                            'MMSI':response_obj.xpath("(//table[1]/tbody/tr/td)[2]/text()").get(),
                            'ShipName':response_obj.xpath("(//table[1]/tbody/tr/td)[3]/text()").get(),
                            'ShipType':response_obj.xpath("(//table[1]/tbody/tr/td)[5]/text()").get(),
                            'Status':response_obj.xpath("(//table[1]/tbody/tr/td)[6]/text()").get(),
                            'Flag':response_obj.xpath("(//table[1]/tbody/tr/td)[7]/text()").get(),
                            'GT':response_obj.xpath("(//table[1]/tbody/tr/td)[8]/text()").get(),
                            'DeadWeight':response_obj.xpath("(//table[1]/tbody/tr/td)[9]/text()").get(),
                            'Built':response_obj.xpath("(//table[1]/tbody/tr/td)[9]/text()").get(),
                            'Builder':response_obj.xpath("(//table[1]/tbody/tr/td)[10]/text()").get(),
                            'ClassificationSoc':response_obj.xpath("(//table[1]/tbody/tr/td)[11]/text()").get(),
                            'HomePort':response_obj.xpath("(//table[1]/tbody/tr/td)[12]/text()").get(),
                            'Owner':response_obj.xpath("(//table[1]/tbody/tr/td)[13]/text()").get(),
                            'Manager':response_obj.xpath("(//table[1]/tbody/tr/td)[14]/text()").get(),
                            'Description':response_obj.xpath("(//table[1]/tbody/tr/td)[15]/text()").get(),
                            'OLD_Name':response_obj.xpath("(//table[1]/tbody/tr/td)[4]").get(),
                            'Entire_Table' : response_obj.xpath("(//table)[1]").get()
                            }
                        # self.responses.append(driver.page_source)
                    driver.close()
                    driver.switch_to_window(main_window)
                next_page = driver.find_element_by_xpath("//a[(text()= 'Next')]")
                next_page.click()
                driver.implicitly_wait(10)
                # self.responses.append(driver.page_source)

                # if len(self.responses) > 2:
                #     break
        
            except NoSuchElementException:
                break

        # for resp in self.responses:
        #     response_obj = Selector(text=resp)
        #     yield {
        #         'IMO':response_obj.xpath("(//table[1]/tbody/tr/td)[1]/text()").get(),
        #         'MMSI':response_obj.xpath("(//table[1]/tbody/tr/td)[2]/text()").get(),
        #         'ShipName':response_obj.xpath("(//table[1]/tbody/tr/td)[3]/text()").get(),
        #         'ShipType':response_obj.xpath("(//table[1]/tbody/tr/td)[5]/text()").get(),
        #         'Status':response_obj.xpath("(//table[1]/tbody/tr/td)[6]/text()").get(),
        #         'Flag':response_obj.xpath("(//table[1]/tbody/tr/td)[7]/text()").get(),
        #         'GT':response_obj.xpath("(//table[1]/tbody/tr/td)[8]/text()").get(),
        #         'DeadWeight':response_obj.xpath("(//table[1]/tbody/tr/td)[9]/text()").get(),
        #         'Built':response_obj.xpath("(//table[1]/tbody/tr/td)[9]/text()").get(),
        #         'Builder':response_obj.xpath("(//table[1]/tbody/tr/td)[10]/text()").get(),
        #         'ClassificationSoc':response_obj.xpath("(//table[1]/tbody/tr/td)[11]/text()").get(),
        #         'HomePort':response_obj.xpath("(//table[1]/tbody/tr/td)[12]/text()").get(),
        #         'Owner':response_obj.xpath("(//table[1]/tbody/tr/td)[13]/text()").get(),
        #         'Manager':response_obj.xpath("(//table[1]/tbody/tr/td)[14]/text()").get(),
        #         'Description':response_obj.xpath("(//table[1]/tbody/tr/td)[15]/text()").get(),
        #         'OLD_Name':response_obj.xpath("(//table[1]/tbody/tr/td)[4]").get(),
        #         'Entire_Table' : response_obj.xpath("(//table)[1]").get()
        #         }



        

        