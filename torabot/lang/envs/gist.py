import aiohttp
from asyncio import coroutine
from .base import Base


class Env(Base):

    def __init__(self, id):
        super(Env, self).__init__()
        self.uri = uri(id)

    @coroutine
    def read(self, name):
        return (yield from self.meta)['files'][name]['content'].encode('utf-8')

    @property
    @coroutine
    def meta(self):
        value = getattr(self, '_meta', None)
        if value is None:
            resp = yield from aiohttp.request('GET', self.uri)
            self._meta = value = yield from resp.read_and_close(decode=True)
        return value


def uri(id):
    return 'https://api.github.com/gists/{}'.format(id)
