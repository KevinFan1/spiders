# -*- coding: UTF-8 -*-
import json
import os
import time

import scrapy
from loguru import logger
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy.utils.project import get_project_settings

from ..items import WemartItem
from ..settings import base_dir


class WemartSpiderSpider(scrapy.Spider):
    name = 'wemart_spider'
    allowed_domains = ['wemart.com']
    start_urls = ['http://wemart.com/']

    headers = {'Host': 'm.wenmarket.wemart.com',
               'Accept': 'application/json',
               'Pragma': 'no-cache',
               'Accept-Language': 'zh-cn',
               'User-Agent': 'tmall-app/20 CFNetwork/1325.0.1 Darwin/21.1.0', 'Cache-Control': 'no-cache',
               'x-requested-with': 'XMLHttpRequest',
               }
    cookies = {}
    raw_product_url = 'https://m.wenmarket.wemart.com/api/item/store/item/searchStoreSku?frontCategoryId={}&pageNo={}&pageSize=10&_={}'

    def start_requests(self):
        url = f'https://m.wenmarket.wemart.com/api/herd/set/cookie?name=Display_Language&value=zh_CN&_={int(time.time() * 1000)}'
        # 获取cookie
        yield scrapy.Request(url, headers=self.headers, callback=self.req_first_category, dont_filter=True)

    def req_first_category(self, response: Response):
        cookie_byte_list = response.headers.getlist('Set-Cookie')
        cookies = {}
        for i in cookie_byte_list:
            st = i.decode().split(';')
            for s in st:
                key = s.strip().split('=')[0]
                value = ''.join(s.strip().split('=')[1:])
                cookies[key] = value
        self.cookies = cookies
        self.cookies['sick'] = '1100025015'
        self.cookies['sick.sig'] = 'q66qlP6DJiip5huD3TrVy1iEptw'
        # 获取大级别的分类
        url = f'https://m.wenmarket.wemart.com/api/web/item/shop-category/list?pid=1605&_={int(time.time() * 1000)}'
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_first_category, dont_filter=True)

    def parse_first_category(self, response: Response):
        dataset = json.loads(response.text)['data']
        for data in dataset:
            # 创建文件夹
            dir_name = os.path.join(base_dir, data['name'])
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            # 写入info信息
            with open(os.path.join(dir_name, 'info.json'), 'w') as f:
                f.write(json.dumps(data, ensure_ascii=False))

            # 获取小分类信息
            url = f'https://m.wenmarket.wemart.com/api/web/item/shop-category/tree?pid={data["id"]}&_={int(time.time() * 1000)}'
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_sec_category, dont_filter=True,
                                 meta={
                                     'parent_path': dir_name,
                                     'fir_cate': data['name']
                                 })
            logger.debug(f'【{data["name"]}】一级分类写入完成')

    def parse_sec_category(self, response: Response):
        # 获取父类的路径
        parent_path = response.meta['parent_path']
        fir_cate = response.meta['fir_cate']
        dataset = json.loads(response.text)['data']
        for data in dataset:
            # category info
            info = data['shopCategoryInfo']

            category_name = str(info["name"]).replace('/', '&')
            dir_name = os.path.join(parent_path, category_name)

            # 创建文件夹
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            # 写入信息
            with open(os.path.join(dir_name, 'info.json'), 'w') as f:
                f.write(json.dumps(info, ensure_ascii=False))

            # 获取商品信息
            pid = info['id']
            page_no = 1
            url = self.raw_product_url.format(pid, page_no, int(time.time() * 1000))
            yield scrapy.Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse_product_info,
                                 meta={
                                     'parent_path': dir_name,
                                     'category_name': category_name,
                                     'fir_cate': fir_cate,
                                     'pid': pid,
                                     'url': url,
                                     'is_first': True
                                 })
            logger.warning(f'【{category_name}】二级分类写入完成')

    def parse_product_info(self, response: Response):
        # 获取header信息
        is_first = response.meta['is_first']
        parent_path = response.meta['parent_path']
        category_name = response.meta['category_name']
        fir_cate = response.meta['fir_cate']
        pid = response.meta['pid']
        api_url = response.meta['url']
        # 获取response数据
        resp_data = json.loads(response.text)['data']
        total = resp_data['total']
        dataset = resp_data['data']

        if is_first:
            # 如果是第一页：
            for page_no in range(2, total // 10 + 2):
                url = self.raw_product_url.format(pid, page_no, int(time.time() * 1000))
                yield scrapy.Request(url, headers=self.headers, cookies=self.cookies,
                                     callback=self.parse_product_info,
                                     meta={
                                         'parent_path': parent_path,
                                         'category_name': category_name,
                                         'fir_cate': fir_cate,
                                         'pid': pid,
                                         'url': url,
                                         'is_first': False
                                     })

            with open(os.path.join(parent_path, '商品信息.csv'), 'w') as f:
                f.write('名字,编号,产地,重量(g),品牌,规格,保质期,现价,原价,图片,接口地址\n')
                # item init
                for data in dataset:
                    # 总数据
                    item = WemartItem()
                    item['name'] = data['name']
                    item['fir_cate'] = fir_cate
                    item['sec_cate'] = category_name
                    item['itemCode'] = data['itemCode']
                    item['productionPlace'] = data['productionPlace']
                    item['weight'] = data['weight']
                    item['brandName'] = data['brandName']
                    item['fullUnitName'] = '{}/{}'.format(data['fullUnit'], data['unitName'], )
                    item['qualityDate'] = data['qualityDate']
                    item['price'] = data['price'] / 100
                    item['originalPrice'] = data['originalPrice'] / 100 if data['originalPrice'] else '暂无'
                    item['mainImage'] = data['mainImage']
                    item['url'] = api_url
                    yield item

                    # 写入内容
                    content = '{},{},{},{},{},{}/{},{},{},{},{},{}'.format(
                        data['name'],
                        data['itemCode'],
                        data['productionPlace'],
                        data['weight'],
                        data['brandName'],
                        data['fullUnit'],
                        data['unitName'],
                        data['qualityDate'],
                        data['price'] / 100,
                        data['originalPrice'] / 100 if data['originalPrice'] else '暂无',
                        data['mainImage'],
                        api_url,
                    )

                f.write(f'{content}\n')
        else:
            with open(os.path.join(parent_path, '商品信息.csv'), 'a') as f:
                # item init
                for data in dataset:
                    # 总数据
                    item = WemartItem()
                    item['name'] = data['name']
                    item['fir_cate'] = fir_cate
                    item['sec_cate'] = category_name
                    item['itemCode'] = data['itemCode']
                    item['productionPlace'] = data['productionPlace']
                    item['weight'] = data['weight']
                    item['brandName'] = data['brandName']
                    item['fullUnitName'] = '{}/{}'.format(data['fullUnit'], data['unitName'], )
                    item['qualityDate'] = data['qualityDate']
                    item['price'] = data['price'] / 100
                    item['originalPrice'] = data['originalPrice'] / 100 if data['originalPrice'] else '暂无'
                    item['mainImage'] = data['mainImage']
                    item['url'] = api_url
                    yield item

                    # 写入内容
                    content = '{},{},{},{},{},{}/{},{},{},{},{},{}'.format(
                        data['name'],
                        data['itemCode'],
                        data['productionPlace'],
                        data['weight'],
                        data['brandName'],
                        data['fullUnit'],
                        data['unitName'],
                        data['qualityDate'],
                        data['price'] / 100,
                        data['originalPrice'] / 100 if data['originalPrice'] else '暂无',
                        data['mainImage'],
                        api_url,
                    )
                    f.write(f'{content}\n')
                logger.debug(f'{parent_path}_{category_name}_{pid}追加完成')
