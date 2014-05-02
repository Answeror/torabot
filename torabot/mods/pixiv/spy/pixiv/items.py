# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Art(Item):

    title = Field()
    author = Field()
    uri = Field()
    thumbnail_uri = Field()


class Page(Item):

    query = Field()
    uri = Field()
    total = Field()
    arts = Field()


class SearchUserPage(Page):

    recommendations = Field()


class Recommendation(Item):

    user_uri = Field()
    icon_uri = Field()
    title = Field()
    illustration_count = Field()
    caption = Field()
    images = Field()


class RecommendationImage(Item):

    uri = Field()
    thumbnail_uri = Field()
