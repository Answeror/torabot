import json
from urllib.parse import parse_qs
from asyncio import coroutine


class Request(object):

    def __init__(self, aioreq, aiopay):
        self.aioreq = aioreq
        self.aiopay = aiopay

        if '?' in aioreq.path:
            self.path, self.qs = self.aioreq.path.split('?')
            self.args = parse_qs(self.qs)
        else:
            self.path = self.aioreq.path
            self.qs = ''
            self.args = {}

    @coroutine
    def read(self):
        none = object()
        value = getattr(self, '_data', none)
        if value is none:
            self._data = value = yield from self.aiopay.read()
        return value

    @property
    @coroutine
    def json(self):
        value = getattr(self, '_json', None)
        if value is None:
            data = yield from self.read()
            self._json = value = json.loads(data.decode('ascii'))
        return value
