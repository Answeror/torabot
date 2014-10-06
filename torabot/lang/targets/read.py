from asyncio import coroutine
import json
from .base import Base


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
