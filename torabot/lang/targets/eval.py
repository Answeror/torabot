from asyncio import coroutine
from .base import Base


class Target(Base):

    unary = True

    @coroutine
    def __call__(self, conf):
        return (yield from Target.run(self.env, conf))
