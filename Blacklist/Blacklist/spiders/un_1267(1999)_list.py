# -*- coding=utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
#from Blacklist_Crawl.items import WantedItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UN_1267_List_Spider(Spider):
    u"""
        联合国1267号决议协助基地组织个人及机构名单 
    """
    name = "un_1267"
    allowed_domains=['www.un.org']
    start_urls=[
        "http://www.un.org/sc/committees/1267/AQList.htm",
    ]
        
    def __init__(self):
        self.i_outfile="outfile/un_1267_list_Individuals.txt"
        self.e_outfile="outfile/un_1267_list_Entities.txt"

    def parse(self, response):
        u"""
            index of UN_1267_list
        """
        url_head = response.url[:17]
        sel = response.xpath("//table")  
        Individuals_Contain_Table = sel[1]
        Entities_Contain_Table =  sel[2]

        with open(self.i_outfile, "w") as i_file:
            self.parse_each_item(Individuals_Contain_Table, i_file)

        with open(self.e_outfile, "w") as e_file:
            self.parse_each_item(Entities_Contain_Table, e_file)


    def parse_each_item(self, Table, Outfile):
        u"""
            wirte data to file
        """
        rows = Table.xpath("tr/td/div[@class='rowtext']")
        for each in rows:
            title = each.xpath("b/text()").extract()
            each_title = ([t.strip() for t in title][1:])

            info = each.xpath("text()|span/text()").extract()
            each_info = (filter( lambda x: ''.join(x.split()), [i.strip() for i in info]))
            each_info.reverse()

            length_of_title = len(each_title)
            for t in range(length_of_title):
                if t == length_of_title-1:
                    Outfile.write("".join([each_info.pop() , '#']));break
                next_title = each_title[t+1]
                if 'a)' in next_title:
                    continue
                elif ')' in next_title and "original script" not in next_title:
                    Outfile.write("".join([each_info.pop() , '|']))
                else:
                    Outfile.write("".join([each_info.pop() , '#']))

            Outfile.write('\n')

