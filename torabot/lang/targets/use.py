from asyncio import coroutine
from .base import Base


class Target(Base):

    unary = True
    shortcut_prefix = '&'

    @coroutine
    def __call__(self, name):
        none = object()
        value = self.env.result.get(name, none)
        if value is none:
            raise Exception("Result of %s haven't been computed" % name)
        return value
