import scrapy
from scrapy import Request
from scrapy.http.response import Response


class CoronavirusZoneSpider(scrapy.Spider):
    name = 'coronavirus'
    allowed_domains = ['coronavirus.zone']
    start_urls = ['https://coronavirus.zone/']

    def start_requests(self):  #was a mistake without it (INFO: Ignoring response <403 https://allo.ua/ua/velosipedy/>: HTTP status code is not handled or not allowed)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response: Response):
        products = response.xpath("//div[(contains(@class, 'info'))]/")
        for product in products:
            yield {
                product
            }
