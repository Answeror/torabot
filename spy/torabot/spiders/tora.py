# coding: utf-8

from collections import OrderedDict
from urlparse import urljoin
from urllib import urlencode
from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import Art, Result


BASE_URL = 'http://www.toranoana.jp/'
QUERY_URL = 'http://www.toranoana.jp/cgi-bin/R2/allsearch.cgi'


class Tora(Spider):

    name = 'tora'

    def __init__(self, query, *args, **kargs):
        Spider.__init__(self, *args, **kargs)
        self.start_urls = [makeuri(encode(query))]

    def parse(self, response):
        sel = Selector(response)
        trs = list(sel.xpath('//table[@class="FixFrame"]//tr'))

        def gen():
            for tr in trs[2:-1:2]:
                yield Art(
                    title=tr.xpath('td[@class="c1"]/a/text()').extract()[0],
                    author=tr.xpath('td[@class="c2"]/a/text()').extract()[0],
                    company=tr.xpath('td[@class="c3"]/a/text()').extract()[0],
                    uri=urljoin(BASE_URL, tr.xpath('td[@class="c1"]/a/@href').extract()[0]),
                    status='reserve' if u'予' in tr.xpath('td[@class="c7"]/text()').extract() else 'other',
                )

        return Result(arts=list(gen()))


def encode(query):
    return query.decode('utf-8') if isinstance(query, str) else query


def makeuri(query, start=0):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode('Shift_JIS')),
        ('ps', start + 1),
    ]))
