# -*- coding: utf-8 -*-
import scrapy

class ImoSpider(scrapy.Spider):
    name = 'imo_srch'
    allowed_domains = ['www.vesselfinder.com']
#    start_urls = ['https://www.vesselfinder.com/vessels']
    # https://www.vesselfinder.com/vessels?name=9648714

    sturls = [str("https://www.vesselfinder.com/vessels?name="+l.strip()) for l in open('D:/PSC_Tokyo_refinie/All_IMO.csv').readlines()]

    def start_requests(self):
        for url in self.sturls:
            yield scrapy.Request(url = url, callback = self.parse,headers={
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                })

    def parse(self, response):
        for vessel in response.xpath("//table[@class='results table is-hoverable is-fullwidth']/tbody/tr"):
            yield response.follow(url=response.urljoin(vessel.xpath(".//td[@class='v2']/a/@href").get()),
             callback=self.parse_Callsign,
             headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'},
             meta={
                 '_Imo_Url' : response.request.url,
                 'Vessel_Name':vessel.xpath(".//td[@class='v2']/a/div[@class='sli']/div[@class='slna']/text()").get(),
                 'Flag' : vessel.xpath(".//td[@class='v2']/a/div/@title").get(),
                 'Vessel_Type': vessel.xpath(".//td[@class='v2']/a/div[@class='sli']/div[@class='slty']/text()").get(),
                 'Year_Built' : vessel.xpath(".//td[@class='v3 is-hidden-mobile']/text()").get(),
                 'GT' : vessel.xpath(".//td[@class='v4 is-hidden-mobile']/text()").get(),
                 'DWT' : vessel.xpath(".//td[@class='v4 is-hidden-mobile']/text()").get(),
                 'Size_m' : vessel.xpath(".//td[@class='v6 is-hidden-mobile']/text()").get()
                 })

    def parse_Callsign(self, response):
        _Imo_Url = response.request.meta['_Imo_Url'],
        Vessel_Name = response.request.meta['Vessel_Name'],
        Flag = response.request.meta['Flag'],
        Vessel_Type = response.request.meta['Vessel_Type'],
        Year_Built = response.request.meta['Year_Built'],
        GT = response.request.meta['GT'],
        DWT = response.request.meta['DWT'],
        Size_m = response.request.meta['Size_m']

        data_available = response.xpath("//div[@class='column vfix-top npr']/h2[@class='bar']/text()").get()
        if data_available == "Position & Voyage Data":
            yield {
                '_Imo_Url' : _Imo_Url,
                'URL_' : response.request.url,
                'Vessel_Name':Vessel_Name,
                'Flag' : Flag,
                'Callsign' : response.xpath("//td[text()='Callsign']/following::td[@class='v3']/text()").get(),
                'Vessel_Type': Vessel_Type,
                'AIS_Type' : response.xpath("//td[text()='AIS Type']/following::td[@class='v3']/text()").get(),
                'Year_Built' : Year_Built,
                'GT' : GT,
                'DWT' : DWT,
                'Size_m' : Size_m
            }

        else:
            yield {
                '_Imo_Url' : _Imo_Url,
                'URL_' : response.request.url,
                'Vessel_Name':Vessel_Name,
                'Flag' : Flag,
                'Callsign' : '-',
                'Vessel_Type': Vessel_Type,
                'AIS_Type' : '-',
                'Year_Built' : Year_Built,
                'GT' : GT,
                'DWT' : DWT,
                'Size_m' : Size_m
            }
