# coding: utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Result(Item):

    ok = Field()
    query = Field()
    message = Field()
