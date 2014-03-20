# coding: utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from collections import OrderedDict
from urlparse import urljoin
from urllib import urlencode
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from torabot.spy.items import Result
from torabot.spy.spiders.redis import RedisSpider
from ..items import Art, Page


BASE_URL = 'http://www.toranoana.jp/'
QUERY_URL = 'http://www.toranoana.jp/cgi-bin/R2/allsearch.cgi'


class Tora(RedisSpider):

    name = 'tora'

    def __init__(self, life=60, *args, **kargs):
        RedisSpider.__init__(self, *args, **kargs)
        self.life = float(life)

    def make_request_from_query(self, query):
        if query.startswith(BASE_URL):
            return Request(
                query,
                cookies={'afg': '0'},
                headers={'Referer': QUERY_URL},
                callback=self.parse_art,
                meta=dict(
                    uri=query,
                ),
                dont_filter=True,
            )
        else:
            uri = makeuri(query)
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

    def parse_art(self, response):
        uri = response.meta['uri']
        sel = Selector(response)
        try:
            art = Art(
                title=sel.xpath('//td[@class="td_title_bar_r1c2"]/text()').extract()[0],
                author=sel.xpath('//td[@class="DetailData_L"]/a[contains(@href, "author")]/text()').extract(),
                company=sel.xpath('//td[@class="CircleName"]/a[1]/text()').extract()[0],
                uri=uri,
                status='reserve' if u'予' in sel.xpath('//form[@action="/cgi-bin/R4/details.cgi"]/input[@type="submit"]/@value').extract()[0] else 'other',
            )
            return Page(
                query=uri,
                uri=uri,
                total=1,
                arts=[art]
            )
        except:
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False, query=uri)

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
            for tr in trs[2:-1:2]:
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
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False, query=query)


def total(sel):
    return int(sel.xpath('//table[@class="addrtbl"]//td[@class="DTW_td_l"]/span[2]/text()').re('\d+')[0])


def empty(content):
    return u'該当する商品が見つかりませんでした。' in content


def makeuri(query, start=0):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode('Shift_JIS')),
        ('ps', start + 1),
    ]))


def good(response):
    return u'大変混み合っています' not in response.body_as_unicode()
