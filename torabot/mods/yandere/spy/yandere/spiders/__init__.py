# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
import traceback
from torabot.mods.booru.spiders import Booru
from torabot.spy.error import failed
from scrapy.http import Request
from ..items import Tags


class Yandere(Booru):

    name = 'yandere'

    def __init__(self, life=60, *args, **kargs):
        super(Yandere, self).__init__(
            *args,
            life=life,
            posts_url='https://yande.re/post'
        )

    def make_method_dict(self):
        d = super(Yandere, self).make_method_dict()
        d.update({
            'tags': self.make_tags_requests,
        })
        return d

    def make_tags_requests(self, query):
        yield Request(
            'https://yande.re/tag/summary.json',
            callback=self.parse_tags,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse_tags(self, response):
        query = response.meta['query']
        try:
            return Tags(
                query=query,
                content=json.loads(response.body_as_unicode())
            )
        except ValueError:
            return failed(query, 'yande.re busy', expected=True)
        except:
            return failed(query, traceback.format_exc(), response=response)
