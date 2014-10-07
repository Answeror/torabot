import re
import json
from asyncio import coroutine
from .base import Base


RE = re.compile(r'^([_\w\d]*)<')


class Target(Base):

    unary = False
    shortcut_prefix = '<'

    @coroutine
    def __call__(self, name, type):
        return (yield from {
            'blob': self.read,
            'text': self.read_text,
            'json': self.read_json,
        }[type](name))

    @coroutine
    def read(self, name):
        return (yield from self.env.read(name))

    @coroutine
    def read_text(self, name):
        return (yield from self.read(name)).decode('utf-8')

    @coroutine
    def read_json(self, name):
        return json.loads((yield from self.read_text(name)))

    @classmethod
    def try_expand_shortcut(cls, key, value):
        expanded = Base.try_expand_shortcut(key, value)
        if expanded is not None:
            return expanded

        match = RE.search(key)
        if not match:
            return None
        if match.group(1):
            return {'args': [value, match.group(1)]}
        return {'arg': value}
