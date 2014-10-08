# coding: utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import re
import json
import inspect
import traceback
from hashlib import md5
from itertools import chain
from urlparse import urljoin, urlparse, parse_qs
from urllib import urlencode
from scrapy import log
from scrapy.selector import Selector
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.error import failed
from ..items import Art, Page, SearchUserPage, Recommendation, RecommendationImage


BASE_URL = 'http://www.pixiv.net/'
USER_ILLUSTRATIONS_URL = 'http://www.pixiv.net/member_illust.php'
USER_URL = 'http://www.pixiv.net/member.php'
USER_ILLUSTRATIONS_URL_TEMPLATE = USER_ILLUSTRATIONS_URL + '?id=%s'
RANKING_URL = 'http://www.pixiv.net/ranking.php'
SEARCH_USER_URL = 'http://www.pixiv.net/search_user.php'
BUSY_BODY_MD5_LIST = {
    'ebf87808253b9892ef15bdfdbd1b7203',
}


def checkbusy(f):
    def check(response):
        return md5(response.body).hexdigest() in BUSY_BODY_MD5_LIST

    def make(response):
        failed(response.meta['query'], 'pixiv busy', expected=True)

    if inspect.isgeneratorfunction(f):
        def inner(self, response):
            if check(response):
                yield make()
                return
            for ret in f(self, response):
                yield ret
    else:
        def inner(self, response):
            return make() if check(response) else f(self, response)
    return inner


class Pixiv(RedisSpider):

    name = 'pixiv'
    handle_httpstatus_list = [404]

    def __init__(self, max_arts, phpsessid, life=60, *args, **kargs):
        super(Pixiv, self).__init__(*args, life=life, **kargs)
        self.max_arts = int(max_arts)
        self.phpsessid = phpsessid

    def make_requests_from_query(self, query):
        query = json.loads(query)
        for req in {
            'user_id': self.make_user_id_requests,
            'user_uri': self.make_user_uri_requests,
            'user_illustrations_uri': self.make_user_illustrations_uri_requests,
            'ranking': self.make_ranking_uri_requests,
            'username': self.make_username_requests,
        }[query['method']](query):
            yield req

    def make_user_id_requests(self, query):
        yield self._make_user_illustrations_uri_request(
            USER_ILLUSTRATIONS_URL_TEMPLATE % query['user_id'],
            query
        )

    def _make_headers(self):
        return {
            'Cookie': ' '.join([
                'p_ab_id=3;',
                'login_ever=yes;',
                'manga_viewer_expanded=1;',
                'bookmark_tag_type=count;',
                'bookmark_tag_order=desc;',
                'visit_ever=yes;',
                'PHPSESSID=%s;' % self.phpsessid,
            ])
        }

    def make_username_requests(self, query):
        yield Request(
            SEARCH_USER_URL + '?' + urlencode({
                's_mode': 's_usr',
                'nick_mf': 1,
                'i': 0,
                'nick': query['username'].encode('utf-8'),
            }),
            headers=self._make_headers(),
            callback=self.parse_username,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_ranking_uri_requests(self, query):
        page_count = 10
        pages = [None] * page_count
        for page in range(page_count):
            yield Request(
                make_ranking_json_uri(query, page),
                headers=self._make_headers(),
                callback=self.parse_ranking_uri,
                meta=dict(
                    page=page,
                    pages=pages,
                    query=query,
                ),
                dont_filter=True,
            )

    def parse_ranking_uri(self, response):
        query = response.meta['query']
        try:
            pages = response.meta['pages']
            try:
                d = json.loads(response.body_as_unicode())
            except ValueError:
                return failed(query, 'pixiv busy', expected=True)
            pages[response.meta['page']] = [] if 'error' in d else d['contents']
            if None not in pages:
                arts = list(chain(*pages))
                return Page(
                    query=query,
                    uri=make_ranking_uri(query),
                    total=len(arts),
                    arts=arts,
                )
        except:
            return failed(query, traceback.format_exc(), response=response)

    def make_user_uri_requests(self, query):
        d = parse_qs(urlparse(query['uri']).query)
        assert 'id' in d
        yield self._make_user_illustrations_uri_request(
            USER_ILLUSTRATIONS_URL_TEMPLATE % d['id'][0],
            query
        )

    def make_user_illustrations_uri_requests(self, query):
        yield self._make_user_illustrations_uri_request(query['uri'], query)

    def _make_user_illustrations_uri_request(self, uri, query):
        return Request(
            uri,
            headers=self._make_headers(),
            callback=self.parse_user_illustrations_uri,
            meta=dict(
                uri=uri,
                query=query,
            ),
            dont_filter=True,
        )

    @checkbusy
    def parse_user_illustrations_uri(self, response):
        query = response.meta['query']
        if response.status == 404:
            return failed(query, '404', expected=True)
        uri = response.meta['uri']
        log.msg(u'got response of query %s' % uri)

        sel = Selector(response)
        try:
            total = int(sel.xpath('//*[@id="wrapper"]//span[@class="count-badge"]/text()').re(r'\d+')[0])
            arts = list(parse_user_arts(sel))[:self.max_arts]
            if not arts and total > 0:
                return failed(query, 'data inconsist', response=response)
            return Page(
                query=query,
                uri=uri,
                total=total,
                arts=arts,
            )
        except:
            return failed(query, traceback.format_exc(), response=response)

    @checkbusy
    def parse_username(self, response):
        query = response.meta['query']
        if response.status == 404:
            return failed(query, '404')
        sel = Selector(response)
        try:
            if not sel.xpath('//div[@class="_no-item"]'):
                items = list(sel.xpath('//li[@class="user-recommendation-item"]'))
                if len(items) == 0:
                    return failed(query, 'inconsist username search result', response=response)
                if len(items) == 1:
                    user_id = items[0].xpath('.//a[@class="title"]/@href').extract()[0].split('=')[-1]
                    check_user_id(user_id)
                    return self._make_user_illustrations_uri_request(
                        USER_ILLUSTRATIONS_URL_TEMPLATE % user_id,
                        query
                    )
            return Request(
                SEARCH_USER_URL + '?' + urlencode({
                    's_mode': 's_usr',
                    'nick': query['username'].encode('utf-8'),
                }),
                headers=self._make_headers(),
                callback=self.parse_username_recommendations,
                meta=dict(query=query),
                dont_filter=True,
            )
        except:
            return failed(query, traceback.format_exc(), response=response)

    @checkbusy
    def parse_username_recommendations(self, response):
        query = response.meta['query']
        if response.status == 404:
            return failed(query, '404')
        sel = Selector(response)
        try:
            return SearchUserPage(
                query=query,
                uri=response.url,
                total=0,
                arts=[],
                recommendations=list(gen_recommendations(sel))
            )
        except:
            return failed(query, traceback.format_exc(), response=response)


def gen_recommendations(sel):
    for item in sel.xpath('//li[@class="user-recommendation-item"]'):
        yield make_recommendation(item)


def make_recommendation(item):
    return Recommendation(
        user_uri=urljoin(BASE_URL, item.xpath('.//a[@class="title"]/@href').extract()[0]),
        icon_uri=item.xpath('.//a[@class="user-icon-container ui-scroll-view"]/@data-src').extract()[0],
        title=item.xpath('.//a[@class="title"]/text()').extract()[0],
        illustration_count=int(item.xpath('.//dl/dd/a/text()').extract()[0]),
        caption=''.join(item.xpath('.//p[@class="caption"]/text()').extract()),
        images=list(gen_recommendation_images(item.xpath('.//ul[@class="images"]/li'))),
    )


def gen_recommendation_images(images):
    for image in images:
        yield RecommendationImage(
            uri=image.xpath('.//a/@href').extract()[0],
            thumbnail_uri=image.xpath('@data-src').extract()[0],
        )


def check_user_id(id):
    assert re.match(r'^\d+$', id)


def make_ranking_json_uri(query, page):
    return 'http://www.pixiv.net/ranking.php?format=json&mode=%(mode)s&p=%(page)d' % dict(
        mode=query['mode'],
        page=page + 1,
    )


def make_ranking_uri(query):
    return 'http://www.pixiv.net/ranking.php?mode=%(mode)s' % query


def parse_user_arts(sel):
    author = sel.xpath('//h1[@class="user"]/text()').extract()[0]
    # http://stackoverflow.com/a/9133579
    for li in sel.xpath('//li[contains(concat(" ", normalize-space(@class), " "), " image-item ")]'):
        yield Art(
            title=li.xpath('.//h1/@title').extract()[0],
            author=author,
            uri=urljoin(BASE_URL, li.xpath('.//a/@href').extract()[0]),
            thumbnail_uri=li.xpath('.//img/@src').extract()[0],
        )
