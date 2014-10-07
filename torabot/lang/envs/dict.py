from asyncio import coroutine
from .base import Base


class Env(Base):

    def __init__(self, d):
        super(Env, self).__init__()
        self.d = d

    @coroutine
    def read(self, name):
        return self.d['files'][name]['content'].encode('utf-8')
