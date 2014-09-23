# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import json
import base64
import traceback
from scrapy.http import Request
from torabot.spy.spiders.redis import RedisSpider
from torabot.spy.error import failed
from ..items import Response


class OnereqSpider(RedisSpider):

    name = 'onereq'

    def make_requests_from_query(self, query):
        query = json.loads(query)
        yield Request(
            query.get('uri'),
            method=query.get('method', 'GET'),
            headers=query.get('headers', {}),
            body=query.get('body', ''),
            callback=self.parse,
            meta=dict(
                query=query,
                payload=query.get('payload'),
                cookiejar=query.get('env')
            ),
            dont_filter=True,
        )

    def parse(self, response):
        query = response.meta['query']
        try:
            data = dict(
                status=response.status,
                headers=dict(response.headers),
                body=base64.b64encode(response.body)
            )
            payload = response.meta.get('payload')
            if payload:
                data['payload'] = payload
            return Response(
                data=data,
                query=query
            )
        except:
            return failed(query, traceback.format_exc(), response=response)
