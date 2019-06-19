# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import sys
import os

class PlotspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class PlotExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['小区名称', '小区地址', '小区均价', '小区类型', '小区总户数', '小区建成时间','小区商圈'])  # 设置表头


    def process_item(self, item, spider):  # 工序具体内容
        line = [item['plot_name'], item['plot_address'], item['plot_price'], item['plot_type'], item['plot_housenum'], item['plot_year_of_build'], item['plot_business_area']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('plotinfo.xlsx')  # 保存xlsx文件
        return item 