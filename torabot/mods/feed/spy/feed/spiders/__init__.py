# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import json
import jsonpickle
import feedparser
from scrapy import log
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Feed


class FeedSpider(RedisSpider):

    name = 'feed'

    def __init__(self, life=60, *args, **kargs):
        super(FeedSpider, self).__init__(*args, life=life, **kargs)

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in {
            'uri': self.make_uri_requests,
        }[query['method']](query):
            yield req

    def make_uri_requests(self, query):
        yield Request(
            query['uri'],
            callback=self.parse_uri,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse_uri(self, response):
        query = response.meta['query']
        try:
            return Feed(
                uri=response.url,
                query=query,
                data=to_dict(response.body_as_unicode())
            )
        except Exception as e:
            return failed(query, str(e))


def to_dict(s):
    return json.loads(jsonpickle.encode(feedparser.parse(s)))


def failed(query, message):
    log.msg('parse failed: %s' % message, level=log.ERROR)
    return Result(ok=False, query=query, message=message)
