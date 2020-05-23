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
<<<<<<< HEAD
    b = process.crawl('worldometers')
    a = process.start()
=======
    process.crawl('worldometers')
    process.start()
>>>>>>> deefa3209e6410b6f398bb5ee29f6e268089aebe


if __name__ == '__main__':
    cleanup()
    # scrap_data()
