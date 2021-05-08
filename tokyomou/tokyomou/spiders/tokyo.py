# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import operator
import time 
from ..items import TokyomouItem

class TokyoSpider(scrapy.Spider):
    name = 'tokyo'
    # allowed_domains = ['www.apcis.tmou.org/public']
    # start_urls = ['http://www.apcis.tmou.org/public/']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://apcis.tmou.org/public/',
            wait_time=2,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        items = TokyomouItem()
        driver = response.meta['driver']
        # Captcha Frame
        search_captcha = driver.find_element_by_xpath("//form/span").text
        search_captcha = search_captcha.split()
        ops = { "+": operator.add, "-": operator.sub, "*":operator.mul, "/":operator.floordiv }
        val = ops[search_captcha[1]](int(search_captcha[0]),int(search_captcha[2]))
        captcha_fill = driver.find_element_by_xpath("//input")
        captcha_fill.clear()
        captcha_fill.send_keys(val)
        fill_captcha = driver.find_element_by_xpath("//button")
        fill_captcha.click()
        time.sleep(7)
        # driver.save_screenshot('a.png')
        # Selecter Frame
        from_date = driver.find_element_by_xpath("//input[@name='From']")
        from_date.clear()
        from_date.click()
        from_date.send_keys("01.01.2020")
        to_date = driver.find_element_by_xpath("//input[@name='Till']")
        to_date.clear()
        to_date.click()
        to_date.send_keys("13.07.2020")
        driver.find_element_by_xpath("//button[@id='inspections-search-button']").click()
        time.sleep(15)
        # driver.save_screenshot('screenshot.png')
        #Main Frame
        html = driver.page_source
        response_obj = Selector(text=html)
        Deficiencies = response_obj.xpath('''//tr[@onclick="onclick_shipinsp(this,'insp')"]/td[9]/text()''').getall()
        for r in range(1,len(Deficiencies)+1):
            row = str('''//tr[@onclick="onclick_shipinsp(this,'insp')"]''')+str('['+str(r)+']')
            driver.find_element_by_xpath(row).click()
            time.sleep(10)
            # driver.save_screenshot('screenshot.png')

            #Final Frame
            html = driver.page_source
            response_obj = Selector(text=html)
            # yield{
            #     'InspectionDate' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td/text()").get(),
            #     'Authority' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            #     'Port' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            #     'InspectionType' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            #     'Detention' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            #     'ShipName' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[1]/text()").get(),
            #     'IMONumber' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            #     'MMSI' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            #     'Callsign' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            #     'ClassificationSociety' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            #     'Flag' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[6]/text()").get(),
            #     'ShipType' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[7]/text()").get(),
            #     'DateKeelLaid' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[8]/text()").get(),
            #     'DWT' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[9]/text()").get(),
            #     'Tonnage' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[10]/text()").get(),
            #     'C_Name' : response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[1]/text()").get(),
            #     'C_IMONumber' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[2]/text()").get(),
            #     'C_Residence' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[3]/text()").get(),
            #     'C_Registered' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[4]/text()").get(),
            #     'C_Phone' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[5]/text()").get(),
            #     'C_Fax' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[6]/text()").get(),
            #     'C_Email' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[7]/text()").get(),
            #     'Deficiency_Count' : Deficiencies[r-1],
            #     'Ship_Deficiencies' : response_obj.xpath("//h2[text()='Ship deficiencies']/following::table[1]/tbody/tr/td/text()").getall()
            # }
            items['InspectionDate'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td/text()").get(),
            items['Authority'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            items['Port'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            items['InspectionType'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            items['Detention'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            items['ShipName'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[1]/text()").get(),
            items['IMONumber'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            items['MMSI'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            items['Callsign'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            items['ClassificationSociety'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            items['Flag'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[6]/text()").get(),
            items['ShipType'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[7]/text()").get(),
            items['DateKeelLaid'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[8]/text()").get(),
            items['DWT'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[9]/text()").get(),
            items['Tonnage'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[10]/text()").get(),
            items['C_Name'] = response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[1]/text()").get(),
            items['C_IMONumber'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[2]/text()").get(),
            items['C_Residence'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[3]/text()").get(),
            items['C_Registered'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[4]/text()").get(),
            items['C_Phone'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[5]/text()").get(),
            items['C_Fax'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[6]/text()").get(),
            items['C_Email'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[7]/text()").get(),
            items['Deficiency_Count'] = Deficiencies[r-1],
            items['Ship_Deficiencies'] = response_obj.xpath("//h2[text()='Ship deficiencies']/following::table[1]/tbody/tr/td/text()").getall()
            yield items

            driver.find_element_by_xpath('''//button[@onclick="return_to_getinspections(this)"]''').click()
            time.sleep(10)
            driver.save_screenshot('screenshot.png')
            time.sleep(4)

        html = driver.page_source
        response_obj = Selector(text=html)
        while response_obj.xpath("//a[@title='To the next page']"):
            driver.find_element_by_xpath("//a[@title='To the next page']").click()
            time.sleep(15)
            html = driver.page_source
            response_obj = Selector(text=html)
            Deficiencies = response_obj.xpath('''//tr[@onclick="onclick_shipinsp(this,'insp')"]/td[9]/text()''').getall()
        for r in range(1,len(Deficiencies)+1):
            row = str('''//tr[@onclick="onclick_shipinsp(this,'insp')"]''')+str('['+str(r)+']')
            driver.find_element_by_xpath(row).click()
            time.sleep(10)
            # driver.save_screenshot('screenshot.png')

            #Final Frame
            html = driver.page_source
            response_obj = Selector(text=html)
            # yield{
            #     'InspectionDate' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td/text()").get(),
            #     'Authority' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            #     'Port' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            #     'InspectionType' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            #     'Detention' : response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            #     'ShipName' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[1]/text()").get(),
            #     'IMONumber' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            #     'MMSI' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            #     'Callsign' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            #     'ClassificationSociety' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            #     'Flag' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[6]/text()").get(),
            #     'ShipType' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[7]/text()").get(),
            #     'DateKeelLaid' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[8]/text()").get(),
            #     'DWT' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[9]/text()").get(),
            #     'Tonnage' : response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[10]/text()").get(),
            #     'C_Name' : response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[1]/text()").get(),
            #     'C_IMONumber' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[2]/text()").get(),
            #     'C_Residence' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[3]/text()").get(),
            #     'C_Registered' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[4]/text()").get(),
            #     'C_Phone' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[5]/text()").get(),
            #     'C_Fax' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[6]/text()").get(),
            #     'C_Email' :response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[7]/text()").get(),
            #     'Deficiency_Count' : Deficiencies[r-1],
            #     'Ship_Deficiencies' : response_obj.xpath("//h2[text()='Ship deficiencies']/following::table[1]/tbody/tr/td/text()").getall()
            # }
            items['InspectionDate'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td/text()").get(),
            items['Authority'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            items['Port'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            items['InspectionType'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            items['Detention'] = response_obj.xpath("//h2[text()='Inspection data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            items['ShipName'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[1]/text()").get(),
            items['IMONumber'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[2]/text()").get(),
            items['MMSI'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[3]/text()").get(),
            items['Callsign'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[4]/text()").get(),
            items['ClassificationSociety'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[5]/text()").get(),
            items['Flag'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[6]/text()").get(),
            items['ShipType'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[7]/text()").get(),
            items['DateKeelLaid'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[8]/text()").get(),
            items['DWT'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[9]/text()").get(),
            items['Tonnage'] = response_obj.xpath("//h2[text()='Ship data']/following::table[1]/tbody/tr/td[10]/text()").get(),
            items['C_Name'] = response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[1]/text()").get(),
            items['C_IMONumber'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[2]/text()").get(),
            items['C_Residence'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[3]/text()").get(),
            items['C_Registered'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[4]/text()").get(),
            items['C_Phone'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[5]/text()").get(),
            items['C_Fax'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[6]/text()").get(),
            items['C_Email'] =response_obj.xpath("//h2[text()='Company details']/following::table[1]/tbody/tr/td[7]/text()").get(),
            items['Deficiency_Count'] = Deficiencies[r-1],
            items['Ship_Deficiencies'] = response_obj.xpath("//h2[text()='Ship deficiencies']/following::table[1]/tbody/tr/td/text()").getall()
            yield items

            driver.find_element_by_xpath('''//button[@onclick="return_to_getinspections(this)"]''').click()
            time.sleep(10)
            driver.save_screenshot('screenshot.png')
            time.sleep(4)




