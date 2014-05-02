# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import json
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Art, RSS


class Yyets(RedisSpider):

    name = 'yyets'

    def __init__(self, life=60, *args, **kargs):
        super(Yyets, self).__init__(*args, life=life, **kargs)

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in {
            'rss': self.make_rss_requests,
        }[query['method']](query):
            yield req

    def make_rss_requests(self, query):
        yield Request(
            query['uri'],
            callback=self.parse_rss,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse_rss(self, response):
        query = response.meta['query']
        try:
            sel = Selector(response)
            return RSS(
                query=query,
                arts=[make_art(sub) for sub in sel.xpath('//item')]
            )
        except Exception as e:
            log.msg('parse failed: %s' % str(e), level=log.ERROR)
            return Result(ok=False, query=query)


class ArtLoader(ItemLoader):

    default_item_class = Art
    default_input_processor = Identity()
    default_output_processor = TakeFirst()


def make_art(sel):
    loader = ArtLoader(selector=sel)
    for field in Art.__dict__['fields']:
        loader.add_xpath(field, './/%s/text()' % field)
    return loader.load_item()
