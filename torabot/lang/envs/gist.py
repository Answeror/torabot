import json
from asyncio import coroutine
from ...ut.request import request
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
            resp = yield from request.get(self.uri)
            self._meta = value = json.loads(
                (yield from resp.read()).decode('utf-8')
            )
        return value


def uri(id):
    return 'https://api.github.com/gists/{}'.format(id)
