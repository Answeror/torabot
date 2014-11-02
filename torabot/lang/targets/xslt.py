from asyncio import coroutine
from ...ut.xml import xslt
from .base import Base


class Target(Base):

    unary = False

    @coroutine
    def __call__(self, **kargs):
        return (yield from xslt(**kargs))
