# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
from urllib import urlencode
from torabot.mods.booru.spiders import Booru
from scrapy.http import Request
from ..items import Tags


class Danbooru(Booru):

    name = 'danbooru'

    def __init__(self, life=60, *args, **kargs):
        super(Danbooru, self).__init__(
            *args,
            life=life,
            posts_url='http://danbooru.donmai.us/posts'
        )

    def make_method_dict(self):
        d = super(Danbooru, self).make_method_dict()
        d.update({
            'tags': self.make_tags_requests,
        })
        return d

    def make_tags_requests(self, query):
        yield Request(
            self.make_json_uri(query),
            callback=self.parse_tags,
            meta=dict(query=query),
            dont_filter=True,
        )

    def make_json_uri(self, query):
        return 'http://danbooru.donmai.us/tags.json?' + urlencode({
            'search[order]': 'count',
            'limit': 10,
            'search[name_matches]': query['query']
        })

    def parse_tags(self, response):
        query = response.meta['query']
        try:
            return Tags(
                query=query,
                content=json.loads(response.body_as_unicode())
            )
        except Exception as e:
            return self.failed(query, str(e))
