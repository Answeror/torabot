# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Art(Item):

    title = Field()
    author = Field()
    company = Field()
    uri = Field()
    status = Field()


class Page(Item):

    uri = Field()
    total = Field()
    arts = Field()
