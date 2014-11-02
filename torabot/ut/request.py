import aiohttp
import joblib
import pickle
import base64
from flask import current_app
from asyncio import coroutine, wait_for
from time import time
from .facade import Facade
from .redis import redis


fields = ['url', 'method', 'headers', 'cookies', 'data']
lhs = object()
rhs = object()


@coroutine
def fetch(*, cache_life, **kargs):
    assert (set(kargs) & set(fields + ['connector'])) == set(kargs)

    connector = kargs.pop('connector', None)
    if connector is None:
        h = current_app.config['TORABOT_REQUEST_CACHE_PREFIX'] + joblib.hash(kargs)
        cache = yield from get_cache(h)
        if cache is not None:
            if time() - cache['time'] < cache_life:
                return cache['data']

    resp = yield from aiohttp.request(connector=connector, **kargs)
    if connector is not None or cache_life == 0:
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
    yield from set_cache(h, cache, current_app.config['TORABOT_REQUEST_CACHE_LIFE'])

    return cache['data']


@coroutine
def get_cache(key):
    value = yield from redis.get(key)
    return None if value is None else pickle.loads(base64.b64decode(value))


@coroutine
def set_cache(key, value, timeout):
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


class Request(Facade):

    name = 'request'

    def init_app(self, app):
        super().init_app(app)

        if self.get_inited(app):
            return

        redis.init_app(app)

        app.config.setdefault(
            'TORABOT_REQUEST_CACHE_PREFIX',
            'torabot:temp:request:'
        )
        app.config.setdefault('TORABOT_REQUEST_CACHE_LIFE', 300)
        app.config.setdefault('TORABOT_REQUEST_TIMEOUT', 30)
        self.set_inited(app)

    def session(self, stateless):
        return Session(stateless)

    @coroutine
    def fetch(self, uri, **kargs):
        return (yield from self.session(True).fetch(uri=uri, **kargs))

    @coroutine
    def get(self, uri, **kargs):
        return (yield from self.session(True).get(uri=uri, **kargs))

    @coroutine
    def post(self, uri, **kargs):
        return (yield from self.session(True).post(uri=uri, **kargs))


class Session(object):

    def __init__(self, stateless):
        if stateless:
            self.connector = None
        else:
            self.connector = aiohttp.TCPConnector(share_cookies=True)

    @coroutine
    def fetch(
        self,
        uri,
        *,
        method='GET',
        headers={},
        cookies={},
        data=None,
        cache_life=None,
        timeout=None
    ):
        if cache_life is None:
            cache_life = current_app.config['TORABOT_REQUEST_CACHE_LIFE']

        if timeout is not None:
            timeout = current_app.config['TORABOT_REQUEST_TIMEOUT']

        options = {}
        if self.connector:
            options['connector'] = self.connector

        return (yield from wait_for(
            fetch(
                url=uri,
                method=method,
                headers=headers,
                cookies=cookies,
                data=data,
                cache_life=cache_life,
                **options
            ),
            loop=current_app.loop,
            timeout=timeout
        ))

    @coroutine
    def get(self, uri, **kargs):
        return (yield from self.fetch(uri=uri, method='GET', **kargs))

    @coroutine
    def post(self, uri, **kargs):
        return (yield from self.fetch(uri=uri, method='POST', **kargs))


request = Request()


__all__ = ['request', 'Request', 'Session']
