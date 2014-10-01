import aiohttp
from asyncio import coroutine
from functools import partial
from .cache import cache0


def uri(id):
    return 'https://api.github.com/gists/{}'.format(id)


@coroutine
def meta(uri):
    resp = yield from aiohttp.request('GET', uri)
    return (yield from resp.read_and_close(decode=True))


@coroutine
def gist(id):
    return (yield from meta(uri(id)))


@coroutine
def cached_gist(id):
    return (yield from cache0('gist:'.format(id))(partial(gist, id))())
