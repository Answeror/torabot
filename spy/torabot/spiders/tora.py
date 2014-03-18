# coding: utf-8

from collections import OrderedDict
from urlparse import urljoin
from urllib import urlencode
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import Art, Page, Result


BASE_URL = 'http://www.toranoana.jp/'
QUERY_URL = 'http://www.toranoana.jp/cgi-bin/R2/allsearch.cgi'
MAX_TRIES = 10


class Tora(Spider):

    name = 'tora'

    def __init__(self, query, id, *args, **kargs):
        Spider.__init__(self, *args, **kargs)
        self.uri = makeuri(encode(query))
        self.id = id
        self.tries = 0

    @property
    def request(self):
        return Request(
            self.uri,
            cookies={'afg': '0'},
            callback=self.parse
        )

    def start_requests(self):
        return [self.request]

    def parse(self, response):
        def gen(trs):
            for tr in trs[2:-1:2]:
                yield Art(
                    title=tr.xpath('td[@class="c1"]/a/text()').extract()[0],
                    author=tr.xpath('td[@class="c2"]/a/text()').extract()[0],
                    company=tr.xpath('td[@class="c3"]/a/text()').extract()[0],
                    uri=urljoin(BASE_URL, tr.xpath('td[@class="c1"]/a/@href').extract()[0]),
                    status='reserve' if u'予' in tr.xpath('td[@class="c7"]/text()').extract() else 'other',
                )

        self.tries += 1
        sel = Selector(response)

        try:
            trs = list(sel.xpath('//table[@class="FixFrame"]//tr'))
            return Page(
                uri=self.uri,
                total=int(sel.xpath('//table[@class="addrtbl"]//td[@class="DTW_td_l"]/span[2]/text()').re('\d+')[0]),
                arts=list(gen(trs))
            )
        except:
            if self.tries >= MAX_TRIES:
                return Result(ok=False)
            return self.request


def encode(query):
    return query.decode('utf-8') if isinstance(query, str) else query


def makeuri(query, start=0):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode('Shift_JIS')),
        ('ps', start + 1),
    ]))
