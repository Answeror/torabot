from hashlib import md5
from scrapy import log
from .items import Result
from ..core.redis import redis


def failed(query, message, response=None, expected=False):
    lines = [message]
    if response:
        key = u'torabot:temp:response:%s:body' % md5(response.body).hexdigest()
        redis.set(key, response.body)
        lines.append('response headers: {}'.format(response.headers))
        lines.append('response body dumped to ' + key)
    message = '\n---\n'.join(lines)
    log.msg(message, level=log.ERROR)
    return Result(ok=False, query=query, message=message, expected=expected)
