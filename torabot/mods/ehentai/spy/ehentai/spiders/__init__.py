# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import pytz
import traceback
from datetime import datetime
from urllib import urlencode
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.spiders.mixins import RequestMethodMixin
from torabot.spy.error import failed
from torabot.ut.time import TIME_FORMAT
from ..items import Page, Post
from ..rating import parse_rating


class Ehentai(RequestMethodMixin, RedisSpider):

    name = 'ehentai'

    @property
    def request_method_mapping(self):
        return {
            'uri': self.make_uri_requests,
            'query': self.make_query_requests,
        }

    def make_query_requests(self, query):
        yield Request(
            make_query_uri(query),
            callback=self.parse,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_uri_requests(self, query):
        yield Request(
            query['uri'],
            callback=self.parse,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse(self, response):
        query = response.meta['query']
        try:
            sel = Selector(response)
            return Page(
                uri=response.url,
                query=query,
                posts=[make_post(sub) for sub in sel.xpath(
                    '//table[@class="itg"]/tr[starts-with(@class, "gtr")]'
                )]
            )
        except:
            return failed(query, traceback.format_exc(), response=response)


class PostLoader(ItemLoader):

    default_item_class = Post
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    def ctime_in(self, values):
        for s in values:
            yield (
                datetime
                .strptime(s.strip(), '%Y-%m-%d %H:%M')
                .replace(tzinfo=pytz.timezone('America/Anguilla'))  # UTC -4
                .astimezone(pytz.utc)
                .strftime(TIME_FORMAT)
            )

    def cover_uri_in(self, values):
        for s in values:
            if s.startswith('http://'):
                yield s
            else:
                parts = s.split('~')
                # title may contain ~
                if len(parts) >= 4 and parts[0] == 'init':
                    yield 'http://%s/%s' % (parts[1], parts[2])

    def rating_in(self, values):
        for s in values:
            yield parse_rating(s)


def make_post(sel):
    loader = PostLoader(selector=sel)
    loader.add_xpath('uri', './/div[@class="it5"]/a/@href')
    loader.add_xpath('title', 'string(.//div[@class="it5"]/a)')
    loader.add_xpath('cover_uri', './/div[@class="it2"]/img/@src')
    loader.add_xpath('cover_uri', './/div[@class="it2"]/text()')
    loader.add_xpath('category', './/td[@class="itdc"]//img/@alt')
    loader.add_xpath('ctime', './/td[@class="itd"]/text()')
    loader.add_xpath('uploader', 'string(.//td[@class="itu"]//a)')
    loader.add_xpath('rating', './/div[@class="it4"]/div/@style')
    loader.add_xpath('torrent_uri', './/div[@class="it3"]//a/@href')
    return loader.load_item()


def make_query_uri(query):
    get = lambda name: 1 if len(query) == 2 else int(query.get(name, 0))
    return 'http://g.e-hentai.org/?' + urlencode({
        'f_doujinshi': get('doujinshi'),
        'f_manga': get('manga'),
        'f_artistcg': get('artistcg'),
        'f_gamecg': get('gamecg'),
        'f_western': get('western'),
        'f_non-h': get('non-h'),
        'f_imageset': get('imageset'),
        'f_cosplay': get('cosplay'),
        'f_asianporn': get('asianporn'),
        'f_misc': get('misc'),
        'f_search': query['query'].encode('utf-8'),
        'f_apply': 'Apply+Filter',
    })
