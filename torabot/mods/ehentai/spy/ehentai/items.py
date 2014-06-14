# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Page(Item):

    uri = Field()
    query = Field()
    posts = Field()


class Post(Item):

    uri = Field()
    title = Field()
    cover_uri = Field()
    category = Field()
    ctime = Field()
    uploader = Field()
    rating = Field()
    torrent_uri = Field()
