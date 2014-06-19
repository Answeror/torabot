# coding: utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
import traceback
from collections import OrderedDict
from urlparse import urljoin
from urllib import urlencode
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.error import failed
from ..items import Art, Page


BASE_URL = 'http://www.toranoana.jp/'
QUERY_URL = BASE_URL + 'cgi-bin/R2/allsearch.cgi'
COMPLEX_QUERY_URL = BASE_URL + 'cgi-bin/R2/d_search.cgi'
MAX_ARTS = 8


class Tora(RedisSpider):

    name = 'tora'

    def __init__(self, life=60, *args, **kargs):
        super(Tora, self).__init__(*args, life=life, **kargs)

    def make_list_request(self, query):
        try:
            d = json.loads(query)
            if not isinstance(d, dict):
                raise Exception('not standard')
            simple = False
        except:
            simple = True

        if simple:
            uri = makesimpleuri(query, 0)
            return Request(
                uri,
                cookies={'afg': '0'},
                headers={'Referer': QUERY_URL},
                callback=self.parse_list,
                meta=dict(
                    query=query,
                    uri=uri,
                ),
                dont_filter=True,
            )

        uri = makecomplexuri(d, 0)
        return Request(
            uri,
            cookies={'afg': '0'},
            headers={'Referer': COMPLEX_QUERY_URL},
            callback=self.parse_complex_list,
            meta=dict(
                query=query,
                uri=uri,
            ),
            dont_filter=True,
        )

    def make_art_request(self, uri):
        return Request(
            uri,
            cookies={'afg': '0'},
            headers={'Referer': QUERY_URL},
            callback=self.parse_art,
            meta=dict(
                uri=uri,
            ),
            dont_filter=True,
        )

    def make_request_from_query(self, query):
        if query.startswith(BASE_URL):
            return self.make_art_request(query)
        return self.make_list_request(query)

    def parse_art(self, response):
        uri = response.meta['uri']
        sel = Selector(response)
        try:
            art = Art(
                title=sel.xpath('//td[@class="td_title_bar_r1c2"]/text()').extract()[0],
                author=sel.xpath('//td[@class="DetailData_L"]/a[contains(@href, "author")]/text()').extract(),
                company=sel.xpath('//td[@class="CircleName"]/a[1]/text()').extract()[0],
                uri=uri,
                status=status_in_art(sel),
            )
        except:
            return failed(uri, traceback.format_exc(), response=response)

        if 'page' not in response.meta:
            return Page(
                query=uri,
                uri=uri,
                total=1,
                arts=[art]
            )
        else:
            page = response.meta['page']
            ranks = response.meta['ranks']
            page['arts'][ranks[uri]] = art
            if page_complete(page):
                return page

    def parse_complex_list(self, response):
        query = response.meta['query']
        uri = response.meta['uri']
        log.msg(u'got response of query %s' % query, level=log.INFO)

        if empty(response.body_as_unicode()):
            log.msg('empty result', level=log.INFO)
            yield Page(
                query=query,
                uri=uri,
                total=0,
                arts=[]
            )
            return

        sel = Selector(response)
        try:
            uris = [urljoin(BASE_URL, url) for url in sel.xpath('//tr[@class="TBLdtil"]/td[@class="noi_c2"]/a/@href').extract()[:MAX_ARTS]]
            log.msg('got %d arts' % len(uris))
            page = Page(
                query=query,
                uri=uri,
                total=total_complex(sel),
                arts=[None] * len(uris)
            )
            ranks = {uri: i for i, uri in enumerate(uris)}
            for uri in uris:
                req = self.make_art_request(uri)
                req.meta['page'] = page
                req.meta['ranks'] = ranks
                yield req
        except:
            yield failed(query, traceback.format_exc(), response=response)

    def parse_list(self, response):
        query = response.meta['query']
        uri = response.meta['uri']
        log.msg(u'got response of query %s' % query, level=log.INFO)

        if empty(response.body_as_unicode()):
            log.msg('empty result', level=log.INFO)
            return Page(
                query=query,
                uri=uri,
                total=0,
                arts=[]
            )

        def gen(trs):
            for tr in trs[2:-1:2][:MAX_ARTS]:
                yield Art(
                    title=tr.xpath('td[@class="c1"]/a/text()').extract()[0],
                    author=tr.xpath('td[@class="c2"]/a/text()').extract()[0],
                    company=tr.xpath('td[@class="c3"]/a/text()').extract()[0],
                    uri=urljoin(BASE_URL, tr.xpath('td[@class="c1"]/a/@href').extract()[0]),
                    status='reserve' if u'予' in tr.xpath('td[@class="c7"]/text()').extract() else 'other',
                )

        sel = Selector(response)
        try:
            trs = list(sel.xpath('//table[@class="FixFrame"]//tr'))
            return Page(
                query=query,
                uri=uri,
                total=total(sel),
                arts=list(gen(trs))
            )
        except:
            return failed(query, traceback.format_exc(), response=response)


def status_in_art(sel):
    try:
        return 'reserve' if u'予' in sel.xpath('//form[@action="/cgi-bin/R4/details.cgi"]/input[@type="submit"]/@value').extract()[0] else 'other',
    except:
        return 'other'


def total(sel):
    return int(sel.xpath('//table[@class="addrtbl"]//td[@class="DTW_td_l"]/span[2]/text()').re('\d+')[0])


def total_complex(sel):
    return int(sel.xpath('//table[@class="f_tbl_9cf"]/tr/td/span[2]/text()').re('\d+')[0])


def empty(content):
    for s in [
        u'該当する商品が見つかりませんでした。',
        u'同時に指定できる検索キーワードは最大３件までです。',
    ]:
        if s in content:
            return True
    return False


def makecomplexuri(query, start):
    return COMPLEX_QUERY_URL + '?' + urlencode(OrderedDict(
        (key, unicode(value).encode('Shift_JIS')) for key, value in query.items()
    ))


def makesimpleuri(query, start):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode('Shift_JIS')),
        ('ps', start + 1),
    ]))


def good(response):
    return u'大変混み合っています' not in response.body_as_unicode()


def page_complete(page):
    return None not in page['arts']
