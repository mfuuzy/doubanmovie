# -*- coding: utf-8 -*-
from scrapy.selector import Selector
# from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from douban.items import DoubanItem

class MoiveSpider(CrawlSpider):
    name="doubanmoive"
    allowed_domains=["movie.douban.com"]
    # start_urls=["https://movie.douban.com/top250?start=0&filter="]
    start_urls=["https://movie.douban.com/top250"]
    rules=[
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),callback="parse_item"),
    ]

    def parse_item(self,response):
        sel=Selector(response)
        item=DoubanItem()
        item['name']=sel.xpath('//span[@property="v:itemreviewed"]/text()').extract()
        item['year']= sel.xpath('//span[@class="year"]/text()').re('\d+')
        item['score']=sel.xpath('//strong[@class="ll rating_num"]/text()').extract()
        item['director']=sel.xpath('//a[@rel="v:directedBy"]/text()').extract()
        item['classification']=  sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//a[@rel="v:starring"]/text()').extract()[0]
        return item