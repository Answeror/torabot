# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
from scrapy import log
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Posts


class Yandere(RedisSpider):

    name = 'yandere'

    def __init__(self, life=60, *args, **kargs):
        super(Yandere, self).__init__(*args, life=life, **kargs)

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in {
            'posts_uri': self.make_posts_uri_requests,
        }[query['method']](query):
            yield req

    def make_posts_uri_requests(self, query):
        PREFIX = u'https://yande.re/post'
        assert query['uri'].startswith(PREFIX)
        yield Request(
            PREFIX + u'.json' + query['uri'][len(PREFIX):],
            callback=self.parse_posts,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse_posts(self, response):
        query = response.meta['query']
        try:
            return Posts(
                query=query,
                uri=query['uri'],
                posts=json.loads(response.body_as_unicode())
            )
        except Exception as e:
            return failed(query, str(e))


def failed(query, message):
    log.msg('parse failed: %s' % message, level=log.ERROR)
    return Result(ok=False, query=query, message=message)
