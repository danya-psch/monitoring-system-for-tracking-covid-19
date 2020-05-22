# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from lxml import etree


class ScrapyCovid19Pipeline:
    def open_spider(self, spider):
        self.root = etree.Element("coronavirus")

    def close_spider(self, spider):
        with open('task_coronavirus.xml', 'wb') as f:
            f.write(etree.tostring(self.root, encoding="UTF-8", pretty_print=True, xml_declaration=True))

    def process_item(self, item, spider):
        if spider.name == "coronavirus":
            page = etree.Element("page", url=item["url"])
            for payload in item["payload"]:
                print('!' + payload + '!')
                fragment = etree.Element("fragment", type=payload["type"])
                fragment.text = payload["data"]
                page.append(fragment)
            self.root.append(page)
        return item
