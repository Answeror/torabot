from asyncio import coroutine
import execjs
from .. import lang
from .base import Base


class Target(Base):
    '''Execute Javascript using node.js

    TODO: async execute
    '''

    unary = False

    @coroutine
    def __call__(self, *args, **kargs):
        if args and kargs:
            raise lang.LangError('Either args or kargs must be empty')
        if args:
            if len(args) == 1:
                return self._do(args[0], 'main', [])
            if len(args) == 2:
                if isinstance(args[1], str):
                    return self._do(args[0], args[1], [])
                return self._do(args[0], 'main', args[1])
            if len(args) == 3:
                return self._do(*args)
            raise lang.LangError('Too many args')
        if kargs:
            return self._do(
                kargs.get('code'),
                kargs.get('func', 'main'),
                kargs.get('args', [])
            )
        assert False, 'Cannot reach here'

    def _do(self, code, func, args):
        if not isinstance(code, str):
            raise lang.LangError('Argument 1 (code) must be str')
        if not isinstance(func, str):
            raise lang.LangError('Argument 2 (func) must be str')
        if not isinstance(args, list):
            raise lang.LangError('Argument 3 (args) must be list')

        node = execjs.get('Node')
        context = node.compile(code)
        return context.call(func, *args)
