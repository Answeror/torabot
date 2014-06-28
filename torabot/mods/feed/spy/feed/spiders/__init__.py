# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import json
import traceback
import jsonpickle
import feedparser
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.error import failed
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
            feed = feedparser.parse(response.body_as_unicode())
            if feed.bozo:
                return failed(query, 'ill formed xml on line {}: {}'.format(
                    feed.bozo_exception.getLineNumber(),
                    feed.bozo_exception.getMessage()
                ), response=response)
            return Feed(
                uri=response.url,
                query=query,
                data=json.loads(jsonpickle.encode(feed))
            )
        except:
            return failed(query, traceback.format_exc(), response=response)
