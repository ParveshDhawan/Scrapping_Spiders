import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

class BalticReqSpider(scrapy.Spider):
    name = 'baltic_Req'
    sturls = [str("https://www.balticshipping.com/vessel/imo/"+l.strip()) for l in open('D:/PSC_Tokyo_refinie/All_IMO.csv').readlines()]
    def start_requests(self):
        for url in self.sturls:
            yield SeleniumRequest(
                url=url,
                # wait_time=10,
                screenshot=True,
                callback = self.parse
            )
    def parse(self, response):
        yield{
            'IMO':response.xpath("(//table[1]/tbody/tr/td)[1]/text()").get(),
            'MMSI':response.xpath("(//table[1]/tbody/tr/td)[2]/text()").get(),
            'ShipName':response.xpath("(//table[1]/tbody/tr/td)[3]/text()").get(),
            'ShipType':response.xpath("(//table[1]/tbody/tr/td)[5]/text()").get(),
            'Status':response.xpath("(//table[1]/tbody/tr/td)[6]/text()").get(),
            'Flag':response.xpath("(//table[1]/tbody/tr/td)[7]/text()").get(),
            'GT':response.xpath("(//table[1]/tbody/tr/td)[8]/text()").get(),
            'DeadWeight':response.xpath("(//table[1]/tbody/tr/td)[9]/text()").get(),
            'Built':response.xpath("(//table[1]/tbody/tr/td)[9]/text()").get(),
            'Builder':response.xpath("(//table[1]/tbody/tr/td)[10]/text()").get(),
            'ClassificationSoc':response.xpath("(//table[1]/tbody/tr/td)[11]/text()").get(),
            'HomePort':response.xpath("(//table[1]/tbody/tr/td)[12]/text()").get(),
            'Owner':response.xpath("(//table[1]/tbody/tr/td)[13]/text()").get(),
            'Manager':response.xpath("(//table[1]/tbody/tr/td)[14]/text()").get(),
            'Description':response.xpath("(//table[1]/tbody/tr/td)[15]/text()").get(),
            'OLD_Name':response.xpath("(//table[1]/tbody/tr/td)[4]").get(),
            'Entire_Table' : response.xpath("(//table)[1]").get()
            }





