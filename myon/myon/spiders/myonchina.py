import json
import os

import scrapy
from loguru import logger
from lxml.etree import fromstring
from scrapy.http import Response
from ..items import ContentItem, Mp4Item
from .. import target_ids
from ..settings import BASE_DIR


class MyonchinaSpider(scrapy.Spider):
    name = 'myonchina'
    allowed_domains = ['myonchina.cn']
    start_urls = ['http://myonchina.cn/']
    domain = 'https://www.myonchina.cn'
    data = {
        'building': '12073',
        'username': 'xxxx',
        'password': 'xxxx',
    }
    total_ids = []

    def start_requests(self):
        logger.info('starting login crawler...')
        login_url = 'https://www.myonchina.cn/login/index.html'
        yield scrapy.FormRequest(
            url=login_url,
            method='POST',
            formdata=self.data,
            callback=self.get_xml_sign_link,
            dont_filter=True
        )

    # def fetch_category(self, response: Response):
    #     logger.success(f'this is response:{response}')
    #
    #     category_url = 'https://www.myonchina.cn/library/browse.html'
    #     yield scrapy.Request(
    #         url=category_url,
    #         dont_filter=True,
    #         callback=self.parse_category,
    #     )
    #
    # def parse_category(self, response: Response):
    #     item = BigCategoryItem()
    #     resp = response.body.decode('utf-8')
    #     html = etree.HTML(resp)
    #     lis = html.xpath('//li[@class="flex_item -n1 flex"]')
    #
    #     for li in lis:
    #         href = self.domain + li.xpath('./a/@href')[0]
    #         category_name = li.xpath('./a/div[2]/text()')[0].strip()
    #         item['name'] = category_name
    #         item['href'] = href
    #         item['parent'] = response.meta.get('parent', None)
    #         yield item
    #         yield scrapy.Request(
    #             url=href,
    #             dont_filter=True,
    #             callback=self.parse_category,
    #             meta={'parent': category_name}
    #         )
    #
    #         if response.meta.get('parent'):
    #             yield scrapy.Request(
    #                 url=href,
    #                 dont_filter=True,
    #                 callback=self.parse_2_category,
    #                 meta={'parent': category_name}
    #             )
    #
    # def parse_2_category(self, response: Response):
    #     resp = response.body.decode('utf-8')
    #     # 获取ids
    #     ids_pattern = r'"bookIds":\[(.+?)\],"bookData":'
    #     if re.search(ids_pattern, resp):
    #         book_ids = re.findall(ids_pattern, resp)[0].replace("\"", "").split(',')
    #     else:
    #         book_ids = ''
    #
    #     self.total_ids += book_ids
    #     logger.error(f'get bookids,{self.total_ids}')

    # def fetch_books_json(self, response: Response):
    #     """
    #     根据id获取所有书的json文件
    #     :param response:
    #     :return:
    #     """
    #     logger.success(f'login success,response is {response}')
    #     json_url = 'https://www.myonchina.cn/api/books.json'
    #     num = int(len(target_ids) / 30)
    #     for i in range(num + 1):
    #         data_ids = target_ids[i * 30:(i + 1) * 30]
    #         data = {f'bookId[{idx}]': book_id for idx, book_id in enumerate(data_ids)}
    #         yield scrapy.FormRequest(
    #             url=json_url,
    #             method='POST',
    #             formdata=data,
    #             dont_filter=True,
    #             callback=self.parse_books_json
    #         )
    #
    # def parse_books_json(self, response: Response):
    #     content_item = ContentItem()
    #     result = json.loads(response.body)['result']
    #     for k, v in result.items():
    #         content_item['book_id'] = k
    #         content_item['content'] = v
    #         yield content_item

    def get_xml_sign_link(self, response: Response):
        api_link = 'https://www.myonchina.cn/api/sign_asset.json'
        # 书本唯一code，从json获取
        # book_code = 'odp_usdte_s17'
        # book_id = '6064'

        # with open(os.path.join(BASE_DIR, 'content.txt'), 'r') as f:
        #     for b in f.read().split('\n'):
        #         book_json = json.loads(b)
        #

        # book_code = book_json['content']['archiveCode']
        # book_id = book_json['book_id']

        book_id = '1932'
        book_code = 'fgmc_fires_f10'


        thumbs_key = f'{book_code}/thumbs/thumbs.json?attempt=0'
        xml_key = f'{book_code}/svg/contents.xml?attempt=0'

        data = {
            f'filettl[{thumbs_key}]': '60',
            f'filettl[{xml_key}]': '60'
        }
        yield scrapy.FormRequest(
            url=api_link,
            method='POST',
            formdata=data,
            dont_filter=True,
            callback=self.parse_xml_link,
            meta={
                'xml_key': xml_key,
                'book_code': book_code,
                'book_id': book_id,
            }
        )

    def parse_xml_link(self, response: Response):
        """
        获取 content xml的链接
        :param response:
        :return:
        """
        # json数据
        resp = json.loads(response.body)
        xml_key = response.meta['xml_key']
        book_code = response.meta['book_code']
        book_id = response.meta['book_id']
        # 获取到带sign的链接
        xml_link = resp['result']['files'][xml_key]
        yield scrapy.Request(
            url=xml_link,
            dont_filter=True,
            callback=self.parse_xml_content,
            meta={
                'book_code': book_code,
                'book_id': book_id,
            }
        )

    def parse_xml_content(self, response: Response):
        """
        解析xml文件获取资源
        :param response:
        :return:
        """
        api_link = 'https://www.myonchina.cn/api/sign_asset.json'
        book_code = response.meta['book_code']
        book_id = response.meta['book_id']

        root = fromstring(response.text)
        for spread in root.find('content').find('body').findall('spread'):
            mp4_name = spread.find('audio').find('file').get('name')
            key = f'{book_code}/svg/mp4/{mp4_name}?attempt=0'
            data = {f'filettl[{key}]': '86400'}
            yield scrapy.FormRequest(
                url=api_link,
                method='POST',
                formdata=data,
                dont_filter=True,
                callback=self.get_sign_mp4_link,
                meta={
                    'key_name': key,
                    'book_code': book_code,
                    'book_id': book_id,
                    'mp4_name': mp4_name
                }
            )

    def get_sign_mp4_link(self, response: Response):
        item = Mp4Item()
        logger.debug(f'mp4 response:{response}')
        key_name = response.meta['key_name']
        resp = json.loads(response.body)
        mp4_link = resp['result']['files'][key_name]

        item['file_urls'] = [mp4_link]
        item['fields'] = response.meta['mp4_name']
        item['folder'] = response.meta['book_id']
        yield item
