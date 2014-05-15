from scrapy.item import Item, Field


class Posts(Item):

    query = Field()
    uri = Field()
    posts = Field()
