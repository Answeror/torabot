import json
from urllib import urlencode
from scrapy import log
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from torabot.spy.error import failed
from .items import Posts


def try_decode(s, coding):
    return s.decode(coding) if not isinstance(s, unicode) else s


class Booru(RedisSpider):

    name = 'booru'

    def __init__(self, posts_url, life=60, *args, **kargs):
        super(Booru, self).__init__(*args, life=life, **kargs)
        self.posts_url = try_decode(posts_url, 'utf-8')

    @property
    def json_query_url(self):
        return self.posts_url + u'.json'

    def make_method_dict(self):
        return {
            'posts_uri': self.make_posts_uri_requests,
            'query': self.make_query_requests,
        }

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in self.make_method_dict()[query['method']](query):
            yield req

    def make_posts_uri_requests(self, query):
        assert query['uri'].startswith(self.posts_url)
        yield Request(
            self.json_query_url + query['uri'][len(self.posts_url):],
            callback=self.parse_posts,
            meta=dict(query=query, uri=query['uri']),
            dont_filter=True,
        )

    def make_query_requests(self, query):
        yield Request(
            self.json_query_url + u'?' + urlencode(dict(tags=query['query'])).decode('ascii'),
            callback=self.parse_posts,
            meta=dict(
                query=query,
                uri=self.posts_url + u'?' + urlencode(dict(tags=query['query'])).decode('ascii'),
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
        except ValueError as e:
            return failed(query, 'yande.re busy', expected=True)
        except Exception as e:
            return self.failed(query, str(e))

    def failed(self, query, message):
        log.msg('parse failed: %s' % message, level=log.ERROR)
        return Result(ok=False, query=query, message=message)
