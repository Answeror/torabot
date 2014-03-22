# coding: utf-8

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from .spiders import good


class Retry(RetryMiddleware):

    def process_response(self, request, response, spider):
        ret = RetryMiddleware.process_response(self, request, response, spider)
        if spider.name != 'tora' or good(response):
            return ret
        reason = 'tora request failed'
        return self._retry(request, reason, spider) or response
