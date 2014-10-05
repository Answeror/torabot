import os
import re
import pkgutil
import importlib
from logbook import Logger
from asyncio import coroutine
from uuid import uuid4
from nose.tools import assert_is_instance
from ..errors import LangError


log = Logger(__name__)
none = object()
name_re = re.compile(r'\S\[([_\w][_\w\d]*)\]')


class Meta(type):

    def __init__(cls, name, bases, attrs):
        super(Meta, cls).__init__(name, bases, attrs)
        cls.kind = cls.__module__.split('.')[-1]


class Base(metaclass=Meta):

    unary = False
    shortcut_prefix = None

    @coroutine
    def stateless(self, *args, **kargs):
        return False

    @classmethod
    @coroutine
    def run(cls, env, conf):
        if isinstance(conf, list):
            conf = yield from cls._expand_list(env, conf)
        elif isinstance(conf, dict):
            conf = yield from cls._expand_dict(env, conf)
            conf = cls.try_expand_shortcut(conf)
            kind = conf.get('@', none)
            if kind is not none:
                target = targetcls(kind)(env=env, name=conf.get('name'))
                return (yield from target.apply(conf))
        return conf

    @coroutine
    def apply(self, conf):
        args = conf.get('args', [])
        assert_is_instance(args, list)
        arg = conf.get('arg', none)
        if arg is not none:
            args = [arg] + args
        kargs = conf.get('kargs', {})
        assert_is_instance(kargs, dict)
        result = yield from self(*args, **kargs)
        self.env.result[self.name] = result
        return result

    def __init__(self, env, name=None):
        self.env = env
        self.name = random_name() if name is None else name

    def regular_context(self, name):
        if name is None:
            name = 'default'
        return self.kind + '.' + name

    @classmethod
    @coroutine
    def _expand_list(cls, env, conf):
        expanded = []
        for item in conf:
            expanded.append((yield from cls.run(env, item)))
        return expanded

    @classmethod
    @coroutine
    def _expand_dict(cls, env, conf):
        expanded = {}
        for key in conf:
            expanded[key] = yield from cls.run(env, conf[key])
        return expanded

    @classmethod
    def try_expand_shortcut(cls, conf):
        if len(conf) != 1:
            return conf

        key = next(iter(conf))

        for c in map(targetcls, sorted(target_types(), reverse=True)):
            basic_prefix = '@' + c.kind
            if key.startswith(basic_prefix):
                expanded = c.expand_prefix_shortcut(key, conf[key], basic_prefix)
            else:
                expanded = c._try_expand_shortcut(key, conf[key])
            if expanded is not None:
                expanded['@'] = c.kind
                name_match = name_re.search(key)
                if name_match:
                    expanded['name'] = name_match.group(1)
                expanded['depends'] = key.split('/')[1:]
                return expanded

        return conf

    @classmethod
    def _try_expand_shortcut(cls, key, value):
        if cls.shortcut_prefix and key.startswith(cls.shortcut_prefix):
            return cls.expand_prefix_shortcut(key, value, cls.shortcut_prefix)

    @classmethod
    def expand_prefix_shortcut(cls, key, value, prefix):
        assert key.startswith(prefix), (key, prefix)
        expanded = {
            'arg' if cls.unary else {
                list: 'args',
                dict: 'kargs'
            }.get(type(value), 'arg'): value
        }
        return expanded


def random_name():
    return str(uuid4())


def targetcls(name):
    try:
        if '.' in name:
            raise LangError('Unknown target type: %s' % name)
        lib = importlib.import_module('..' + name, __name__)
        return lib.Target
    except Exception as e:
        raise LangError('Unknown target: ' + name) from e


def target_types():
    root = os.path.dirname(__file__)
    return [
        name for _, name, _ in pkgutil.iter_modules([root])
        if name not in ('base', 'test')
    ]
