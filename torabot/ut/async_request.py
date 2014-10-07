import aiohttp
import joblib
import pickle
import base64
from asyncio import coroutine
from time import time
from .async_local import local


prefix = 'torabot:temp:request:'
fields = ['url', 'method', 'headers', 'cookies', 'data']
lhs = object()
rhs = object()


def request(cache_life=None, **kargs):
    assert (set(kargs) & set(fields + ['connector'])) == set(kargs)

    if cache_life is None:
        cache_life = local.conf['TORABOT_REQUEST_CACHE_LIFE']

    if 'connector' not in kargs:
        h = prefix + joblib.hash(kargs)
        cache = yield from get_cache(h)
        if cache is not None:
            if time() - cache['time'] < cache_life:
                return cache['data']

    resp = yield from aiohttp.request(**kargs)
    if 'connector' in kargs:
        return resp

    if cache is not None:
        if (
            resp.headers.get('etag', lhs) == cache['data'].headers.get('etag', rhs) or
            resp.headers.get('last-modified', lhs) == cache['data'].headers.get('last-modified', rhs)
        ):
            return cache['data']

    cache = {
        'time': time(),
        'data': (yield from freeze(resp))
    }
    yield from set_cache(h, cache, local.conf['TORABOT_REQUEST_CACHE_LIFE'])

    return cache['data']


@coroutine
def get_cache(key):
    redis = yield from local.redis
    value = yield from redis.get(key)
    return None if value is None else pickle.loads(base64.b64decode(value))


@coroutine
def set_cache(key, value, timeout):
    redis = yield from local.redis
    yield from redis.set(key, base64.b64encode(pickle.dumps(value)).decode('ascii'))
    assert int(timeout) == timeout, 'Timeout must be seconds'
    yield from redis.expire(key, int(timeout))


@coroutine
def freeze(resp):
    return Response(
        status=resp.status,
        headers=resp.headers,
        cookies=resp.cookies,
        body=(yield from resp.read())
    )


class Response(object):

    def __init__(self, status, headers, cookies, body):
        self.status = status
        self.headers = headers
        self.cookies = cookies
        self.body = body

    @coroutine
    def read(self):
        return self.body
