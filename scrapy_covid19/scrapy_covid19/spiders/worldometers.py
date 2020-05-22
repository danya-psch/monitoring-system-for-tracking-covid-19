import scrapy
from scrapy import Request
from scrapy.http.response import Response


class WorldometersSpider(scrapy.Spider):
    name = 'worldometers'
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response: Response):
        products = response.xpath("//table[@id='main_table_countries_today']/tbody/tr")
        for product in products:
            class_attrib = product.attrib
            if 'style' in class_attrib and len(class_attrib) == 1:
                columns = product.xpath('./td')
                yield {
                    'num': columns[0].xpath('./text()[1]').get(),
                    'country': columns[1].xpath('./a/text()[1]').get(),
                    'total_cases': columns[2].xpath('./text()[1]').get(),
                    'new_cases': columns[3].xpath('./text()[1]').get(),
                    'total_deaths': columns[4].xpath('./text()[1]').get(),
                    'new_deaths': columns[5].xpath('./text()[1]').get(),
                    'total_recovered': columns[6].xpath('./text()[1]').get(),
                    'active_cases': columns[7].xpath('./text()[1]').get(),
                    'serious_critical': columns[8].xpath('./text()[1]').get(),
                    'tot_cases': columns[9].xpath('./text()[1]').get(),
                    'deaths': columns[10].xpath('./text()[1]').get(),
                    'total_tests': columns[11].xpath('./text()[1]').get(),
                    'tests': columns[12].xpath('./text()[1]').get(),
                    'population': columns[13].xpath('./a/text()[1]').get(),
                }


