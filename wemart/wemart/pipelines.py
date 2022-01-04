# -*- coding: UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os.path

from .settings import base_dir


class WemartPipeline:
    def __init__(self):
        self.file = open(os.path.join(base_dir, '总数据.csv'), 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(('名字', '一级分类', '二级分类', '编号', '产地', '重量(g)', '品牌', '规格', '保质期', '现价', '原价', '图片','接口地址'))

    def process_item(self, item, spider):
        self.writer.writerow((item['name'],
                              item['fir_cate'],
                              item['sec_cate'],
                              item['itemCode'],
                              item['productionPlace'],
                              item['weight'],
                              item['brandName'],
                              item['fullUnitName'],
                              item['qualityDate'],
                              item['price'],
                              item['originalPrice'],
                              item['mainImage'],
                              item['url'],
                              ))

        def close_spider(self, spider):
            self.file.close()
