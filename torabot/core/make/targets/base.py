import os
import pkgutil
import importlib
from uuid import uuid4
from nose.tools import assert_is_instance


none = object()


class Base(object):

    @classmethod
    def run(cls, env, conf):
        if isinstance(conf, dict):
            conf = {key: cls.run(env, conf[key]) for key in conf}

            for symbol, kind in [
                ('&', 'use'),
                ('[]', 'item'),
                ('<', 'read'),
                ('text<', 'read_text'),
            ] + [('@' + kind, kind) for kind in target_types()]:
                parse_shortcut(conf, symbol, kind)

            kind = conf.get('@', none)
            if kind is not none:
                if '.' in kind:
                    raise Exception('unknown target type: %s' % kind)
                target = targetcls(kind)(env=env, name=conf.get('name'))
                args = conf.get('args', [])
                assert_is_instance(args, list)
                arg = conf.get('arg', none)
                if arg is not none:
                    args = [arg] + args
                kargs = conf.get('kargs', {})
                assert_is_instance(kargs, dict)
                result = target(*args, **kargs)
                env.result[target.name] = result
                return result
        elif isinstance(conf, list):
            return [cls.run(env, item) for item in conf]
        return conf

    def __init__(self, env, name=None):
        self.env = env
        self.name = str(uuid4()) if name is None else name


def parse_shortcut(conf, symbol, kind):
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
