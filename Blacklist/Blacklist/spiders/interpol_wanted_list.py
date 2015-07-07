# -*- coding=utf-8 -*-
from scrapy.http import Request, FormRequest
from scrapy.spider import Spider
#from Blacklist_Crawl.items import WantedItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Interpol_Wanted_Spider(Spider):
    u""" 国际刑警通缉名单 """
    name = "interpol_wanted"
    allowed_domains=['www.interpol.int']
    start_urls=[
         "http://www.interpol.int/notice/search/wanted/(Nationality)/146/(search)/1"
    ]
        
    def __init__(self):
        self.outfile=open("outfile/interpol_wanted_list.txt", 'w+')

    def parse(self, response):
        """
            search page of interpol wanted person
        """
        url_head = response.url[:23]

        sel = response.xpath("//div[@class='wanted']")  
        wanted_link_list = [''.join([url_head, s.xpath("div[@class='links']/a/@href").extract()[0]]) for s in sel]

        #Processing Each Wanted
        for wll in wanted_link_list:
            yield Request(url =wll, callback=self.parse_each_item)

        #To Next Page
        next_page_link = ''.join([url_head, response.xpath("//span[@class='next']/a/@href").extract()[0]])
        yield Request(url=next_page_link, callback=self.parse)
        
    def parse_each_item(self, response):
        """
            parse each item, save the data
        """
        name = response.xpath("//div[@class='nom_fugitif_wanted']")
        info_block = response.xpath("//table[@class='table_detail_profil table_detail_profil_result_datasheet']")[0]
        each_info = filter( lambda x: ''.join(x.split()), [i.strip() for i in \
                 info_block.xpath("tr/td[@class='col2 strong']/text() | td[@class='col2 strong']/p/text() ").extract()])
        for i in each_info:
            self.outfile.write(''.join([i, '|']))

        self.outfile.write('\n')

