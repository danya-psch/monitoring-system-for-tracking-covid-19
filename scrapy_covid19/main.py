from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


def cleanup():
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('coronavirus')
    process.start()


if __name__ == '__main__':
    cleanup()
    scrap_data()
