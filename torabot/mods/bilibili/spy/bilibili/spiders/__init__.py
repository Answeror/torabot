# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import json
from urllib import urlencode
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import (
    Bangumi,
    User,
    Post,
    SearchResult,
    SearchResultPost,
    Recommendation,
    QueryResult,
)


class Bilibili(RedisSpider):

    name = 'bilibili'

    def __init__(self, life=60, *args, **kargs):
        super(Bilibili, self).__init__(*args, life=life, **kargs)

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in {
            'bangumi': self.make_bangumi_requests,
            'user': self.make_user_requests,
            'username': self.make_username_requests,
            'query': self.make_query_requests,
        }[query['method']](query):
            yield req

    def make_username_requests(self, query):
        yield Request(
            make_username_search_uri(query['username']),
            callback=self.parse_username_prepare,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_query_requests(self, query):
        yield Request(
            make_query_uri(query['query']),
            callback=self.parse_query,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_bangumi_requests(self, query):
        yield Request(
            'http://www.bilibili.tv/index/bangumi.json',
            callback=self.parse_bangumi,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_user_requests(self, query):
        yield Request(
            'http://space.bilibili.tv/' + query['user_id'],
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
                user_uri=response.url,
                query=query,
                posts=[make_post(sub) for sub in sel.xpath('//div[@class="main_list"]/ul/li')]
            )
        except Exception as e:
            return failed(query, str(e))

    def parse_query(self, response):
        query = response.meta['query']
        try:
            sel = Selector(response)
            return QueryResult(
                uri=response.url,
                query=query,
                posts=[make_search_post(sub) for sub in sel.xpath('//ul[@class="result"]/li')]
            )
        except Exception as e:
            return failed(query, str(e))

    def parse_username_prepare(self, response):
        query = response.meta['query']
        try:
            sel = Selector(response)
            posts = []
            for li in sel.xpath('//ul[@class="result"]/li'):
                post = make_search_post(li)
                if query['username'] == post['upper']:
                    return Request(
                        post['user_uri'],
                        callback=self.parse_user,
                        meta=dict(query=query),
                        dont_filter=True,
                    )
                posts.append(post)
            return SearchResult(
                query=query,
                posts=[],
                recommendations=make_recommendations(posts),
            )
        except Exception as e:
            return failed(query, str(e))


def make_recommendations(posts):
    def gen():
        names = {}
        for p in posts:
            r = make_recommendation(p)
            if r['username'] not in names:
                yield r
                names[r['username']] = 1

    return list(gen())


def make_recommendation(post):
    return Recommendation(
        user_uri=post['user_uri'],
        username=post['upper'],
    )


def failed(query, message):
    log.msg('parse failed: %s' % message, level=log.ERROR)
    return Result(ok=False, query=query, message=message)


class SearchResultPostLoader(ItemLoader):

    default_item_class = SearchResultPost
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    def date_in(self, values):
        for s in values:
            yield s.strip()


def make_search_post(sel):
    loader = SearchResultPostLoader(selector=sel)
    loader.add_xpath('title', 'string(.//div[@class="t"])')
    loader.add_xpath('upper', 'string(.//a[@class="upper"])')
    loader.add_xpath('kind', 'string(.//div[@class="t"]/span)')
    loader.add_xpath('date', 'string(.//i[@class="date"])')
    loader.add_xpath('intro', 'string(.//i[@class="intro"])')
    # mylist don't have title a, use first a instead
    # loader.add_xpath('uri', './/a[@class="title"]/@href')
    loader.add_xpath('uri', './/a/@href')
    loader.add_xpath('user_uri', './/a[@class="upper"]/@href')
    loader.add_xpath('cover', './/a[@class="title"]//img/@src')
    post = loader.load_item()
    if post.get('title', '') and post['title'].startswith(post.get('kind', '')):
        post['title'] = post['title'][len(post.get('kind', '')):]
    return post


class PostLoader(ItemLoader):

    default_item_class = Post
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    def ctime_in(self, values):
        for s in values:
            yield s[5:]


def make_post(sel):
    loader = PostLoader(selector=sel)
    loader.add_xpath('title', 'string(.//a[@class="title"])')
    loader.add_xpath('uri', './/a[@class="title"]/@href')
    loader.add_xpath('cover', './/img/@src')
    loader.add_xpath('kind', 'string(.//a[@class="l"])')
    loader.add_xpath('ctime', 'string(.//div[@class="c"])')
    loader.add_xpath('desc', 'string(.//div[@class="q"])')
    return loader.load_item()


def make_username_search_uri(username):
    return make_query_uri(u'@author %s' % username)


def make_query_uri(query):
    return 'http://www.bilibili.tv/search?' + urlencode({
        'keyword': query.encode('utf-8'),
        'orderby': 'senddate',
    })
