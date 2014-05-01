# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Art(Item):

    link = Field()
    title = Field()
    guid = Field()
    description = Field()
    pubDate = Field()


class RSS(Item):

    query = Field()
    uri = Field()
    arts = Field()
