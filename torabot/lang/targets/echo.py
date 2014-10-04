from asyncio import coroutine
from .base import Base


class Target(Base):

    unary = True

    @coroutine
    def __call__(self, ping):
        return ping
