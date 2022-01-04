from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from wemart.spiders.wemart_spider import WemartSpiderSpider

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(WemartSpiderSpider)
    process.start()


if __name__ == '__main__':
    run()
