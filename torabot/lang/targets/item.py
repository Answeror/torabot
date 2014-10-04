from asyncio import coroutine
from .base import Base
from ..errors import LangError


class Target(Base):

    unary = False

    @coroutine
    def __call__(self, cont, key, *args):
        for k in [key] + list(args):
            if k not in cont:
                raise LangError('{} not in {}'.format(k, cont))
            cont = cont[k]
        return cont
