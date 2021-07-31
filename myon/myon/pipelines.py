# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

import scrapy

from .items import ContentItem
from scrapy.pipelines.files import FilesPipeline


class MyonPipeline:
    def __init__(self):
        self.file = open('content.json', 'w')

    def process_item(self, item, spider):
        if isinstance(item, ContentItem):
            self.file.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
        return item

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class MyFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        mp4_name = item['fields']
        folder = item['folder']
        for url in item['file_urls']:
            yield scrapy.Request(
                url=url,
                meta={
                    'mp4_name': mp4_name,
                    'folder': folder
                }
            )

    def file_path(self, request: scrapy.Request, response=None, info=None, *, item=None):
        return request.meta['folder'] + '/' + request.meta['mp4_name']
