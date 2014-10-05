from asyncio import coroutine
from .read import Target as Read


class Target(Read):

    shortcut_prefix = 'text<'

    @coroutine
    def __call__(self, name):
        return (yield from super(Target, self).__call__(name, 'text'))
