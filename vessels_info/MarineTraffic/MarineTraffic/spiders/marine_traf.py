import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import pandas as pd

class MarineTrafSpider(scrapy.Spider):
    name = 'marine_traf'
    # sturls = ['https://www.marinetraffic.com/en/ais/details/ships/imo:9444728']
    sturls = [str("https://www.marinetraffic.com/en/ais/details/ships/imo:"+l.strip()) for l in open('D:/PSC_Tokyo_refinie/All_IMO.csv').readlines()]
    
    def start_requests(self):
        for url in self.sturls:
            yield SeleniumRequest(
                url=url,
                # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'},
                wait_time=3,
                screenshot=True,
                callback = self.parse
            )
    

    def parse(self, response):
        driver = response.meta['driver']
        driver.find_element_by_xpath("//button[@class='sc-ifAKCX ljEJIv']").click()
        driver.execute_script("window.scrollTo(10,3500)")
        # driver.implicitly_wait(20)
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(total_width, total_height)
        driver.implicitly_wait(20)
        vesselData = driver.find_element_by_xpath("//div[@class='MuiExpansionPanelDetails-root']").text.split('\n')
        # vesselData = dict([i.split(':') for i in vesselData])
        driver.find_element_by_xpath("//div[@id='Ex_Names_History-header']").click()
        past_data= driver.find_elements_by_xpath("//table/tbody/tr/td[@class='MuiTableCell-root MuiTableCell-body MuiTableCell-sizeSmall']")
        # driver.get_screenshot_as_file("screenshot.png")
        soup = BeautifulSoup(driver.page_source,"lxml")
        old_names = []
        try:
            for i in soup.find('table').find_all('td',class_='MuiTableCell-root MuiTableCell-body MuiTableCell-sizeSmall'):
                if i.find('img'):
                    t = i.find('img')
                    old_names.append(t['title'])
                old_names.append(i.text)
            old_names = [i for i in old_names if i != '']
            n = 3
            old = pd.DataFrame([old_names[i * n:(i + 1) * n] for i in range((len(old_names) + n - 1) // n )],columns=['Flag','Name','Date'])
            old_names = pd.DataFrame([old_names[i * n:(i + 1) * n] for i in range((len(old_names) + n - 1) // n )],columns=['Flag','Name','Date'])
            old_names = old_names.to_dict()

        except:
            print('No Old Names Found')
            old_names = ['-']
        try:
            image_url = driver.find_element_by_xpath("//a[@class='MuiButtonBase-root MuiCardActionArea-root']").get_attribute('href')
        except:
            image_url = ''

        yield {
            'vessel_detail' : vesselData,
            'Vessel_url' : driver.current_url,
            'Image_url' : image_url,
            'Old_Names' : old_names
        }
