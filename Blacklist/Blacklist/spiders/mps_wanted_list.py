# -*- coding=utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
#from Blacklist_Crawl.items import WantedItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class A_Wanted_Spider(Spider):
    u"""
    公安部通缉令--A级通缉令
    """
    name = "a_wanted"
    allowed_domains=['www.mps.gov.cn']
    start_urls=[
        "http://www.mps.gov.cn/n16/n1237/n1417/n456851/", 
    ]
        
    def __init__(self):
        self.outfile=open("MPSAWantedList.txt","w")

    def parse(self, response):
        u"""
            index of Wanted list
        """
        url_head = response.url[:21]
        #item = WantedItem()
        sel = response.xpath("//td[@bgcolor='#E6E6E6']/a[@target='_blank']")    #td about wanted name and link  
        item_link_list = [''.join([url_head, l]) for l in sel.xpath('@href').extract()]
       
        for request_url in item_link_list:
            yield Request(url = request_url, callback = self.parse_each_item)
        
        #To Next Page
        for n in response.xpath("//a"):
            if bool(n.xpath("text()").extract()) and  n.xpath("text()").extract()[0]== u"下一页":
                next_page_link = ''.join([url_head, n.xpath('@href').extract()[0]])
                yield Request(url = next_page_link, callback = self.parse)

    def parse_each_item(self, response):
        u"""
            Page Of Each Wanted
        """
        sel = response.xpath("//table[@bgcolor='#f4faff']")
        elements = sel.xpath("tr/td[@align='left'] ")
        flag = 0
        for elem in elements.xpath("text() | font/text()"):
            if flag % 2:
                value =  ''.join(elem.extract().split())
                self.outfile.write(value + '|')
            flag+=1
        self.outfile.write('\n')


class B_Wanted_Spider(Spider):
    u"""
    公安部通缉令--B级通缉令
    """
    name = "b_wanted"
    allowed_domains=['www.mps.gov.cn']
    start_urls=[
        "http://www.mps.gov.cn/n16/n1237/n1417/n456866/",
    ]
        
    def __init__(self):
        self.outfile=open("MPSBWantedList.txt","w")

    def parse(self, response):
        """
            index of Wanted list
        """
        url_head = response.url[:21]
        sel = response.xpath("//a")    #td about wanted name and link  
        item_link_list=[]
        for a in sel:
            link = a.xpath('@href').extract()[0]
            if '/n456866' in link and 'index' not in link:
                item_link_list.append(''.join([url_head, link]) )

        for request_url in item_link_list:
            yield Request(url = request_url, callback = self.parse_each_item)
        
        #To Next Page
        for n in response.xpath("//a"):
            if bool(n.xpath("text()").extract()) and  n.xpath("text()").extract()[0]== u"下一页":
                next_page_link = ''.join([url_head, n.xpath('@href').extract()[0]])
                yield Request(url = next_page_link, callback = self.parse)

    def parse_each_item(self, response):
        """
            page of each Wanted
        """
        sel = response.xpath("//table[@bgcolor='#f4faff']")
        elements = sel.xpath("tr/td[@align='left'] ")
        flag = 0
        for elem in elements.xpath("text() | font/text()"):
            if flag % 2:
                value =  ''.join(elem.extract().split())
                self.outfile.write(value + '|')
            flag+=1
        self.outfile.write('\n')
