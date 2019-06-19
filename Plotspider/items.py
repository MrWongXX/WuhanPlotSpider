# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlotspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PlotItem(scrapy.Item):    
    content = scrapy.Field()   
    plot_name = scrapy.Field(alias='小区名称')
    plot_address = scrapy.Field(alias='小区地址')
    plot_price = scrapy.Field(alias='小区均价')
    plot_type = scrapy.Field(alias='小区类型')
    plot_housenum = scrapy.Field(alias='小区总户数')
    plot_year_of_build = scrapy.Field(alias='小区建成时间')
    plot_business_area = scrapy.Field(alias='小区商圈')
