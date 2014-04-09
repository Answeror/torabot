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
from ..items import Bangumi, User, Post


class PostLoader(ItemLoader):

    default_item_class = Post
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    def ctime_in(self, values):
        for s in values:
            yield s[5:]


class Bilibili(RedisSpider):

    name = 'bilibili'

    def __init__(self, life=60, *args, **kargs):
        RedisSpider.__init__(self, *args, **kargs)
        self.life = life

    def make_requests_from_query(self, query):
        d = json.loads(query)
        for req in {
            'bangumi': self.make_bangumi_requests,
            'user': self.make_user_requests,
        }[d['method']](d, query):
            yield req

    def make_bangumi_requests(self, d, query):
        yield Request(
            'http://www.bilibili.tv/index/bangumi.json',
            callback=self.parse_bangumi,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_user_requests(self, d, query):
        yield Request(
            'http://space.bilibili.tv/' + d['user_id'],
            callback=self.parse_user,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse_bangumi(self, response):
        query = response.meta['query']
        try:
            return Bangumi(
                query=query,
                content=json.loads(response.body_as_unicode())
            )
        except:
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False, query=query)

    def parse_user(self, response):
        query = response.meta['query']
        try:
            sel = Selector(response)
            return User(
                query=query,
                posts=[make_post(sub) for sub in sel.xpath('//div[@class="main_list"]/ul/li')]
            )
        except Exception as e:
            log.msg('parse failed: %s' % str(e), level=log.ERROR)
            return Result(ok=False, query=query)


def make_post(sel):
    loader = PostLoader(selector=sel)
    loader.add_xpath('title', './/a[@class="title"]/text()')
    loader.add_xpath('uri', './/a[@class="title"]/@href')
    loader.add_xpath('cover', './/img/@src')
    loader.add_xpath('kind', './/a[@class="l"]/text()')
    loader.add_xpath('ctime', './/div[@class="c"]/text()')
    loader.add_xpath('desc', './/div[@class="q"]/text()')
    return loader.load_item()
