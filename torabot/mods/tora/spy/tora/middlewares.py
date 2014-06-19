# coding: utf-8

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from .spiders import busy


class Retry(RetryMiddleware):

    def process_response(self, request, response, spider):
        if not busy(response.body_as_unicode()):
            return RetryMiddleware.process_response(self, request, response, spider)
        reason = 'tora request failed'
        return self._retry(request, reason, spider) or response
