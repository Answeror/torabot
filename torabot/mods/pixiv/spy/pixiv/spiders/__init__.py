# coding: utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
from urlparse import urljoin, urlparse, parse_qs
from scrapy import log
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import NotSupported
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Art, Page


BASE_URL = 'http://www.pixiv.net/'
USER_ILLUSTRATIONS_URL = 'http://www.pixiv.net/member_illust.php'
USER_URL = 'http://www.pixiv.net/member.php'
USER_ILLUSTRATIONS_URL_TEMPLATE = USER_ILLUSTRATIONS_URL + '?id=%s'
RANKING_URL = 'http://www.pixiv.net/ranking.php'


class Pixiv(RedisSpider):

    name = 'pixiv'

    def __init__(self, max_arts, phpsessid, life=60, *args, **kargs):
        RedisSpider.__init__(self, *args, **kargs)
        self.life = float(life)
        self.max_arts = int(max_arts)
        self.phpsessid = phpsessid

    def make_requests_from_query(self, query):
        query = json.loads(query)
        yield {
            'user_id': self.make_user_id_request,
            'user_uri': self.make_user_uri_request,
            'user_illustrations_uri': self.make_user_uri_request,
        }[query['method']](query)

    def make_user_id_request(self, query):
        return self._make_user_illustrations_uri_request(
            USER_ILLUSTRATIONS_URL_TEMPLATE % query['user_id'],
            query
        )

    def make_ranking_uri_requests(self, uri):
        page_count = 10
        pages = [None] * page_count
        for page in range(page_count):
            yield Request(
                make_ranking_json_uri(uri, page),
                callback=self.parse_ranking_uri,
                meta=dict(
                    uri=uri,
                    page=page,
                    pages=pages,
                ),
                dont_filter=True,
            )

    def parse_ranking_uri(self, response):
        raise NotSupported('not implemented')

    def make_user_uri_request(self, query):
        d = parse_qs(urlparse(query['uri']).query)
        assert 'id' in d
        return self._make_user_illustrations_uri_request(
            USER_ILLUSTRATIONS_URL_TEMPLATE % d['id'][0],
            query
        )

    def make_user_illustrations_uri_request(self, query):
        return self._make_user_illustrations_uri_request(query['uri'], query)

    def _make_user_illustrations_uri_request(self, uri, query):
        return Request(
            uri,
            headers={
                'Cookie': ' '.join([
                    'p_ab_id=3;',
                    'login_ever=yes;',
                    'manga_viewer_expanded=1;',
                    'bookmark_tag_type=count;',
                    'bookmark_tag_order=desc;',
                    'visit_ever=yes;',
                    'PHPSESSID=%s;' % self.phpsessid,
                ])
            },
            callback=self.parse_user_illustrations_uri,
            meta=dict(
                uri=uri,
                query=query,
            ),
            dont_filter=True,
        )

    def parse_user_illustrations_uri(self, response):
        query = response.meta['query']
        uri = response.meta['uri']
        log.msg(u'got response of query %s' % uri)

        def gen(sel):
            author = sel.xpath('//h1[@class="user"]/text()').extract()[0]
            for a in sel.xpath('//a[@class="work"]')[:self.max_arts]:
                yield Art(
                    title=a.xpath('h1/@title').extract()[0],
                    author=author,
                    uri=urljoin(BASE_URL, a.xpath('@href').extract()[0]),
                    thumbnail_uri=a.xpath('img/@src').extract()[0],
                )

        sel = Selector(response)
        try:
            return Page(
                query=query,
                uri=uri,
                total=sel.xpath('//*[@id="wrapper"]/div[1]/div[1]/div/span/text()').re(r'\d+')[0],
                arts=list(gen(sel)),
            )
        except:
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False, query=query)


def make_ranking_json_uri(uri, page):
    raise NotSupported('not implemented')
