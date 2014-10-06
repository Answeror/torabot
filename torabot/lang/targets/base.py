import os
import re
import json
import pkgutil
import importlib
from functools import partial
from logbook import Logger
from asyncio import coroutine
from uuid import uuid4
from nose.tools import assert_is_instance
from ...ut.async_local import local
from ..errors import LangError


log = Logger(__name__)
none = object()
name_re = re.compile(r'\S\[([_\w][_\w\d]*)\]')
pubsub_channel_template = 'torabot:lang:env:{}:{}'


class Meta(type):

    def __new__(cls, name, bases, attrs):
        attrs['kind'] = attrs['__module__'].split('.')[-1]
        return super(Meta, cls).__new__(cls, name, bases, attrs)


class Base(metaclass=Meta):

    unary = False
    shortcut_prefix = None

    def __init__(self, env, name=None, depends=[]):
        self.env = env
        self.name = random_name() if name is None else name
        self.depends = depends

    def regular_context(self, name):
        if name is None:
            name = 'default'
        return self.kind + '.' + name

    @coroutine
    def sub(self, channel):
        redis = yield from local.redis
        sub = yield from redis.start_subscribe()
        yield from sub.subscribe([
            pubsub_channel_template.format(self.env.name, channel)
        ])
        return sub

    @coroutine
    def pub(self, message):
        channel = self.name
        redis = yield from local.redis
        return (yield from redis.publish(
            pubsub_channel_template.format(self.env.name, channel),
            json.dumps(message)
        ))

    @coroutine
    def stateless(self, *args, **kargs):
        return False

    @classmethod
    @coroutine
    def run(cls, env, conf):
        conf = yield from cls._parse(env, conf)
        return (yield from eval(conf))

    @classmethod
    @coroutine
    def _expand(cls, conf):
        if isinstance(conf, list):
            conf = yield from trans_list(conf, cls._expand)
        elif isinstance(conf, dict):
            conf = yield from trans_dict(conf, cls._expand)
            conf = try_expand_conf(conf)
        return conf

    @classmethod
    @coroutine
    def _parse(cls, env, conf):
        conf = yield from cls._expand(conf)
        print(json.dumps(conf, indent=4))
        conf = yield from bind(env, conf)
        return conf

    @coroutine
    def _bind(self, env, conf):
        args = conf.get('args', [])
        assert_is_instance(args, list)
        arg = conf.get('arg', none)
        if arg is not none:
            args = [arg] + args
        kargs = conf.get('kargs', {})
        assert_is_instance(kargs, dict)
        self.__args = yield from trans_list(args, partial(bind, env))
        self.__kargs = yield from trans_dict(kargs, partial(bind, env))
        self._depend_subs = {}
        for dep in self.depends:
            self._depend_subs[dep] = yield from self.sub(dep)
        return self

    @coroutine
    def _eval(self):
        self.__args = yield from trans_list(self.__args, eval)
        self.__kargs = yield from trans_dict(self.__kargs, eval)
        self.depend_result = {}
        for dep, sub in self._depend_subs.items():
            self.depend_result[dep] = json.loads(
                (yield from sub.next_published()).value
            )
        result = yield from self(*self.__args, **self.__kargs)
        yield from self.pub(result)
        return result

    @classmethod
    def _try_expand_shortcut(cls, key, value):
        if cls.shortcut_prefix and key.startswith(cls.shortcut_prefix):
            return cls._expand_prefix_shortcut(key, value, cls.shortcut_prefix)

    @classmethod
    def _postprocess_conf(cls, conf):
        return conf

    @classmethod
    def _expand_prefix_shortcut(cls, key, value, prefix):
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


@coroutine
def bind(env, conf):
    if isinstance(conf, list):
        conf = yield from trans_list(conf, partial(bind, env))
    elif isinstance(conf, dict):
        kind = conf.get('@', none)
        if kind is none:
            conf = yield from trans_dict(conf, partial(bind, env))
        else:
            target = targetcls(kind)(
                env=env,
                name=conf.get('name'),
                depends=conf.get('depends', [])
            )
            conf = yield from target._bind(env, conf)
    return conf


@coroutine
def eval(conf):
    if isinstance(conf, list):
        return (yield from trans_list(conf, eval))
    if isinstance(conf, dict):
        return (yield from trans_dict(conf, eval))
    if isinstance(conf, Base):
        return (yield from conf._eval())
    return conf


@coroutine
def trans_list(conf, func):
    expanded = []
    for item in conf:
        expanded.append((yield from func(item)))
    return expanded


@coroutine
def trans_dict(conf, func):
    expanded = {}
    for key in conf:
        expanded[key] = yield from func(conf[key])
    return expanded


def try_expand_shortcut(conf):
    if len(conf) != 1:
        return conf

    key = next(iter(conf))

    for cls in map(targetcls, sorted(target_types(), reverse=True)):
        basic_prefix = '@' + cls.kind
        if key.startswith(basic_prefix):
            expanded = cls._expand_prefix_shortcut(key, conf[key], basic_prefix)
        else:
            expanded = cls._try_expand_shortcut(key, conf[key])
        if expanded is not None:
            expanded['@'] = cls.kind
            name_match = name_re.search(key)
            if name_match:
                expanded['name'] = name_match.group(1)
            expanded['depends'] = key.split('/')[1:]
            return expanded

    return conf


def try_expand_conf(conf):
    conf = try_expand_shortcut(conf)
    kind = conf.get('@', none)
    if kind is not none:
        conf = targetcls(kind)._postprocess_conf(conf)
    return conf
