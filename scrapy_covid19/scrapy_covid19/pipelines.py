# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from lxml import etree


class ScrapyCovid19Pipeline:
    def open_spider(self, spider):
        self.root = etree.Element("worldometers")

    def close_spider(self, spider):
        with open('task_worldometers.xml', 'wb') as f:
            f.write(etree.tostring(self.root, encoding="UTF-8", pretty_print=True, xml_declaration=True))

    def process_item(self, item, spider):
        if spider.name == "worldometers":
            product = etree.Element("record")
            list_of_evements = []
            for key, value in item.items():
                el = etree.Element(key)
                el.text = value
                list_of_evements.append(el)
            for el in list_of_evements:
                product.append(el)
            self.root.append(product)
        return item
