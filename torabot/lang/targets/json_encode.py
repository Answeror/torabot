from asyncio import coroutine
import json
from .base import Base


class Target(Base):

    unary = True

    @coroutine
    def __call__(self, data):
        return json.dumps(data)
