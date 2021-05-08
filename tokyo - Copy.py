# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import operator

class TokyoSpider(scrapy.Spider):
    name = 'tokyo'
    # allowed_domains = ['www.apcis.tmou.org/public']
    # start_urls = ['http://www.apcis.tmou.org/public/']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://apcis.tmou.org/public/',
            wait_time=2,
            screenshot=True,
            callback=self.parse_authorize
        )

    def parse_authorize(self, response):
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        driver = response.meta['driver']
        cookies = driver.get_cookies()
        driver.quit()


        # Captcha Frame
        search_captcha = driver.find_element_by_xpath("//form/span").text
        search_captcha = search_captcha.split()
        ops = { "+": operator.add, "-": operator.sub, "*":operator.mul, "/":operator.floordiv }
        val = ops[search_captcha[1]](int(search_captcha[0]),int(search_captcha[2]))
        captcha_fill = driver.find_element_by_xpath("//input")
        captcha_fill.clear()
        captcha_fill.send_keys(val)
        driver.find_element_by_xpath("//button").click()
        # driver.save_screenshot('screenshot.png')
        # Selecter Frame
        from_date = driver.find_element_by_xpath("//input[@name='From']")
        from_date.clear()
        from_date.click()
        from_date.send_keys("12.06.2020")
        to_date = driver.find_element_by_xpath("//input[@name='Till']")
        to_date.clear()
        to_date.click()
        to_date.send_keys("12.07.2020")
        driver.find_element_by_xpath("//button[@id='inspections-search-button']").click()
        driver.save_screenshot('screenshot.png')




    def parse(self, response):
        pass
