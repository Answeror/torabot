from asyncio import coroutine
from .base import Base


class Target(Base):

    unary = False

    @coroutine
    def __call__(self, *args):
        return args[-1]
