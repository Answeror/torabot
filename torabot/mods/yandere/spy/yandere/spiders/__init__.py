# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
from urllib import urlencode
from scrapy import log
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Posts


PREFIX = u'https://yande.re/post'
JSON_QUERY_URL = PREFIX + u'.json'


class Yandere(RedisSpider):

    name = 'yandere'

    def __init__(self, life=60, *args, **kargs):
        super(Yandere, self).__init__(*args, life=life, **kargs)

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in {
            'posts_uri': self.make_posts_uri_requests,
            'query': self.make_query_requests,
        }[query['method']](query):
            yield req

    def make_posts_uri_requests(self, query):
        assert query['uri'].startswith(PREFIX)
        yield Request(
            JSON_QUERY_URL + query['uri'][len(PREFIX):],
            callback=self.parse_posts,
            meta=dict(query=query, uri=query['uri']),
            dont_filter=True,
        )

    def make_query_requests(self, query):
        yield Request(
            JSON_QUERY_URL + u'?' + urlencode(dict(tags=query['query'])).decode('ascii'),
            callback=self.parse_posts,
            meta=dict(
                query=query,
                uri=PREFIX + u'?' + urlencode(dict(tags=query['query'])).decode('ascii'),
            ),
            dont_filter=True,
        )

    def parse_posts(self, response):
        query = response.meta['query']
        uri = response.meta['uri']
        try:
            return Posts(
                query=query,
                uri=uri,
                posts=json.loads(response.body_as_unicode())
            )
        except Exception as e:
            return failed(query, str(e))


def failed(query, message):
    log.msg('parse failed: %s' % message, level=log.ERROR)
    return Result(ok=False, query=query, message=message)
