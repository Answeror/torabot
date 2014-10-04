import os
import pkgutil
import importlib
from asyncio import coroutine
from uuid import uuid4
from nose.tools import assert_is_instance
from ..errors import LangError


none = object()


class Base(object):

    @classmethod
    @coroutine
    def run(cls, env, conf):
        if isinstance(conf, list):
            #return list((yield from cls.run(env, item)) for item in conf)
            d = []
            for item in conf:
                d.append((yield from cls.run(env, item)))
            return d
        elif isinstance(conf, dict):
            #conf = dict(
                #(key, (yield from cls.run(env, conf[key])))
                #for key in conf
            #)
            d = {}
            for key in conf:
                d[key] = yield from cls.run(env, conf[key])
            conf = d

            for symbol, kind in [
                ('&', 'use'),
                ('[]', 'item'),
                ('<', 'read'),
                ('text<', 'read_text'),
            ] + [('@' + kind, kind) for kind in target_types()]:
                expand_shortcut(conf, symbol, kind)

            kind = conf.get('@', none)
            if kind is not none:
                if '.' in kind:
                    raise LangError('Unknown target type: %s' % kind)
                target = targetcls(kind)(env=env, name=conf.get('name'))
                args = conf.get('args', [])
                assert_is_instance(args, list)
                arg = conf.get('arg', none)
                if arg is not none:
                    args = [arg] + args
                kargs = conf.get('kargs', {})
                assert_is_instance(kargs, dict)
                result = yield from target(*args, **kargs)
                env.result[target.name] = result
                return result
        return conf

    def __init__(self, env, name=None):
        self.env = env
        self.name = random_name() if name is None else name

    def regular_context(self, name):
        if name is None:
            name = 'default'
        return self.__module__.split('.')[-1] + '.' + name


def random_name():
    return str(uuid4())


def expand_shortcut(conf, symbol, kind):
    item = conf.get(symbol, none)
    if item is not none:
        del conf[symbol]
        conf.update({
            '@': kind,
            'arg' if targetcls(kind).unary else {
                list: 'args',
                dict: 'kargs'
            }.get(type(item), 'arg'): item
        })


def targetcls(name):
    lib = importlib.import_module('..' + name, __name__)
    return lib.Target


def target_types():
    root = os.path.dirname(__file__)
    return [
        name for _, name, _ in pkgutil.iter_modules([root])
        if name not in ('base', 'test')
    ]
