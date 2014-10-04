from asyncio import coroutine
import json
from .base import Base


class Target(Base):

    unary = False

    @coroutine
    def __call__(self, name, type):
        return {
            'blob': self.read,
            'text': self.read_text,
            'json': self.read_json,
        }[type](name)

    def read(self, name):
        return self.env.read(name)

    def read_text(self, name):
        return self.read(name).decode('utf-8')

    def read_json(self, name):
        return json.loads(self.read_text(name))
