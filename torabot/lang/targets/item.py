import re
from asyncio import coroutine
from .. import lang
from .base import Base


RE = re.compile(r'^\[([_\w\d]*)\]')


class Target(Base):

    unary = False
    shortcut_prefix = '[]'

    @coroutine
    def __call__(self, cont, key, *args):
        for k in [key] + list(args):
            k = self._conv_key(cont, key)
            if k not in cont:
                raise lang.LangError('{} not in {}'.format(k, cont))
            cont = cont[k]
        return cont

    def _conv_key(self, cont, key):
        if isinstance(cont, dict):
            return str(key)
        if isinstance(cont, list):
            return int(key)
        return key

    @classmethod
    def try_expand_shortcut(cls, key, value):
        expanded = Base.try_expand_shortcut(key, value)
        if expanded is not None:
            return expanded

        ma = RE.search(key)
        if not ma:
            return None
        if ma.group(1):
            return {'args': [value, ma.group(1)]}
        return {'args': value}
