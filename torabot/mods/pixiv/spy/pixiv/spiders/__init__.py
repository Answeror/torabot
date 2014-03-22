# coding: utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from urlparse import urljoin
from scrapy import log
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import NotSupported
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.items import Result
from ..items import Art, Page


BASE_URL = 'http://www.pixiv.net/'
AUTHOR_URL = 'http://www.pixiv.net/member_illust.php'


class Pixiv(RedisSpider):

    name = 'pixiv'

    def __init__(self, phpsessid, life=60, *args, **kargs):
        RedisSpider.__init__(self, *args, **kargs)
        self.life = float(life)
        self.phpsessid = phpsessid

    def make_request_from_query(self, query):
        if query.startswith(AUTHOR_URL):
            return self.make_author_uri_request(query)
        raise NotSupported('only support author uri query now')

    def make_author_uri_request(self, uri):
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
            callback=self.parse_author_uri,
            meta=dict(
                uri=uri,
            ),
            dont_filter=True,
        )

    def parse_author_uri(self, response):
        uri = response.meta['uri']
        log.msg(u'got response of query %s' % uri)

        with open('out.html', 'wb') as f:
            f.write(response.body)

        def gen(sel):
            author = sel.xpath('//h1[@class="user"]/text()').extract()[0]
            for a in sel.xpath('//a[@class="work"]'):
                yield Art(
                    title=a.xpath('h1/@title').extract()[0],
                    author=author,
                    uri=urljoin(BASE_URL, a.xpath('@href').extract()[0]),
                    thumbnail_uri=a.xpath('img/@src').extract()[0],
                )

        sel = Selector(response)
        try:
            return Page(
                query=uri,
                uri=uri,
                total=sel.xpath('//*[@id="wrapper"]/div[1]/div[1]/div/span/text()').re(r'\d+')[0],
                arts=list(gen(sel)),
            )
        except:
            log.msg('parse failed', level=log.ERROR)
            return Result(ok=False, query=uri)
