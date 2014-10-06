import base64
from asyncio import coroutine
from .base import Base


class Target(Base):

    unary = False

    @coroutine
    def __call__(self, text, encoding='utf-8'):
        return base64.b64encode(text.encode(encoding)).decode('ascii')
