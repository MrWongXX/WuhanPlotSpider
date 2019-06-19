# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from Plotspider.items import PlotItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['https://wuhan.anjuke.com']
    start_urls = ['https://wuhan.anjuke.com/community/']
    base_url = 'https://wuhan.anjuke.com/'

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))
    
    
    def parse(self, response):

        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")
        
        plot_nodes = response.xpath("//div[@_soj='xqlb']")
        for plot_node in plot_nodes:
            plot_url = plot_node.css("div::attr(link)").extract_first("")
            plot_price = plot_node.xpath("./div[@class='li-side']/p/strong/text()").extract_first("")
            yield Request(url=plot_url,meta={"plot-price":plot_price},callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url = response.css(".aNxt::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        plot = PlotItem()
        plot['plot_name'] = response.xpath("//div[@class='comm-title']/h1/text()").extract_first().strip()
        plot['plot_address'] = response.xpath("//div[@class='comm-title']/h1/span/text()").extract_first().strip()
        plot['plot_price'] = response.meta.get("plot-price","")
        plot['plot_type'] = response.xpath("//dl[@class='basic-parms-mod']/dd[1]/text()").extract_first().strip()
        plot['plot_housenum'] = response.xpath("//dl[@class='basic-parms-mod']/dd[4]/text()").extract_first().strip()
        plot['plot_year_of_build'] = response.xpath("//dl[@class='basic-parms-mod']/dd[5]/text()").extract_first().strip()
        plot['plot_business_area'] = response.xpath("//dl[@class='basic-parms-mod']/dd[11]/text()").extract_first().strip()

        yield plot