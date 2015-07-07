# -*- coding=utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
#from Blacklist_Crawl.items import WantedItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class A_Wanted_Spider(Spider):
    u""" 
        天网行动 全球通缉百名外逃人员 
    """
    name = "operation_skynet"
    allowed_domains=['ccdi.gov.cn']
    start_urls=[
        "http://ccdi.gov.cn/xwtt/201504/t20150422_55183.html",
    ]
        
    def __init__(self):
        self.outfile=open("outfile/Operation_Skynet_List.txt","w")

    def parse(self, response):
        u""" index of Wanted list """
        url_head = response.url[:19]
        #item = WantedItem()
        sel = response.xpath("//table[@class='people_list']/tr")[1:]
        for each in sel:
            elems = each.xpath("td")
            # 姓名
            name   = elems[0].xpath('p/text()')[0].extract()
            # 性别
            gender = elems[1].xpath('text()')[0].extract()
            # 原工作单位及职务
            jobs   = elems[2].xpath('text()')[0].extract()
            # 身份证号码
            per_id = elems[3].xpath('text()').extract()
            for id in per_id:
                per_id = ''.join(per_id)
            # 外逃所持证照信息
            flee_certificate = elems[4].xpath('text()').extract()
            for fc in flee_certificate:
                flee_certificate = ''.join(flee_certificate)
            # 外逃时间 
            flee_date   = elems[5].xpath('text()')[0].extract()
            # 可能逃往国家和地区
            flee_country= elems[6].xpath('text()')[0].extract()
            # 立案单位
            filing_unit = elems[7].xpath('text()')[0].extract()
            # 涉嫌罪名
            charges     = elems[8].xpath('text()')[0].extract()
            # 发布红色通缉令时间
            wanted_date = elems[9].xpath('text()')[0].extract()
            # 红色通缉令号码
            wanted_no   = elems[10].xpath('text()')[0].extract()

            #print name,'|',gender,'|',jobs, '|', per_id,'|', flee_certificate, '|',flee_date, '|',flee_country, '|',charges, '|',wanted_date, '|',wanted_no
            each_date = ''.join([name,'|',gender,'|',jobs, '|', per_id,'|', flee_certificate, '|',flee_date, '|',flee_country, '|',charges, '|',wanted_date, '|',wanted_no, '\n'])
            self.outfile.write(each_date)

