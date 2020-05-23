import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

r = redis.Redis(charset="utf-8", decode_responses=True)


def cleanup():
    try:
        os.remove("task_worldometers.xml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('worldometers')
    process.start()


if __name__ == '__main__':
    cleanup()
    # scrap_data()
