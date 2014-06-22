# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Gist(Item):

    uri = Field()
    query = Field()
    meta = Field()
    files = Field()


class File(Item):

    name = Field()
    content = Field()
