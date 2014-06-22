# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
import traceback
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.spiders.mixins import RequestMethodMixin
from torabot.spy.error import failed
from ..items import Gist, File


class GistSpider(RequestMethodMixin, RedisSpider):

    name = 'gist'

    @property
    def request_method_mapping(self):
        return {
            'id': self.make_id_requests,
        }

    def make_id_requests(self, query):
        yield Request(
            make_gist_uri(query),
            callback=self.parse_gist,
            meta=dict(query=query),
            dont_filter=True,
        )

    def parse_gist(self, response):
        query = response.meta['query']
        try:
            gist = Gist(
                uri=response.url,
                query=query,
                meta=json.loads(response.body_as_unicode()),
                files=[]
            )
            files = gist['meta'].get('files')
            if files is None:
                yield failed(query, response.body_as_unicode())
                return
            for name, info in files.items():
                yield self.make_file_request(name, info, gist)
        except:
            yield failed(query, traceback.format_exc(), response=response)

    def make_file_request(self, name, info, gist):
        return Request(
            info['raw_url'],
            callback=self.parse_file,
            meta=dict(gist=gist, name=name),
            dont_filter=True,
        )

    def parse_file(self, response):
        gist = response.meta['gist']
        try:
            gist['files'].append(File(
                name=response.meta['name'],
                content=response.body_as_unicode()
            ))
            if len(gist['files']) == len(gist['meta']['files']):
                return gist
        except:
            return failed(gist['query'], traceback.format_exc(), response=response)


def make_gist_uri(query):
    return 'https://api.github.com/gists/' + query['id']
