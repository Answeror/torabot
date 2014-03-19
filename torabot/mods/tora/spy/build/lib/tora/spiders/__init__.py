# coding: utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from collections import OrderedDict
from urlparse import urljoin
from urllib import urlencode
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from hashlib import md5
from ..items import Art, Page
from torabot.items import Result


BASE_URL = 'http://www.toranoana.jp/'
QUERY_URL = 'http://www.toranoana.jp/cgi-bin/R2/allsearch.cgi'


class Tora(Spider):

    name = 'tora'

    def __init__(self, query, *args, **kargs):
        Spider.__init__(self, *args, **kargs)
        self.query = decode(query)

    @property
    def id(self):
        return md5(self.query.encode('utf-8')).hexdigest()

    @property
    def uri(self):
        return makeuri(self.query)

    @property
    def request(self):
        return Request(
            self.uri,
            cookies={'afg': '0'},
            headers={'Referer': QUERY_URL},
            callback=self.parse
        )

    def start_requests(self):
        try:
            return [self.request]
        except:
            log.msg('start requests failed', level=log.ERROR)
            return []

    def parse(self, response):
        if empty(response.body_as_unicode()):
            log.msg('empty result', level=log.INFO)
            return Page(uri=self.uri, total=0, arts=[])

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
            return Page(uri=self.uri, total=total(sel), arts=list(gen(trs)))
        except:
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False)


def total(sel):
    return int(sel.xpath('//table[@class="addrtbl"]//td[@class="DTW_td_l"]/span[2]/text()').re('\d+')[0])


def empty(content):
    return u'該当する商品が見つかりませんでした。' in content


def decode(query):
    return query.decode('utf-8') if isinstance(query, str) else query


def makeuri(query, start=0):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode('Shift_JIS')),
        ('ps', start + 1),
    ]))


def good(response):
    return u'大変混み合っています' not in response.body_as_unicode()
