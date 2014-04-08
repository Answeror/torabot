# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import json
from scrapy import log
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Bangumi


class Bilibili(RedisSpider):

    name = 'bilibili'

    def __init__(self, life, *args, **kargs):
        RedisSpider.__init__(self, *args, **kargs)
        self.life = life

    def make_requests_from_query(self, query):
        d = json.loads(query)
        for req in {
            'bangumi': self.make_bangumi_requests,
        }[d['method']](query):
            yield req

    def make_bangumi_requests(self, query):
        req = self.make_requests_from_url('http://www.bilibili.tv/index/bangumi.json')
        req.meta['query'] = query
        yield req

    def parse(self, response):
        query = response.meta['query']
        try:
            return Bangumi(
                query=query,
                content=json.loads(response.body_as_unicode())
            )
        except:
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False, query=query)
