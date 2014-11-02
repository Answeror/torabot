import os
import re
import json
import pkgutil
import importlib
from functools import partial
from logbook import Logger
from asyncio import coroutine, gather
from uuid import uuid4
from nose.tools import assert_is_instance
from ...ut.redis import redis
from .. import lang


log = Logger(__name__)
none = object()
NAME_RE = re.compile(r'\S\[([_\w][_\w\d]*)\]')
PUBSUB_CHANNEL_TEMPLATE = 'torabot:lang:env:{}:{}'


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
        sub = yield from redis.start_subscribe()
        yield from sub.subscribe([
            PUBSUB_CHANNEL_TEMPLATE.format(self.env.name, channel)
        ])
        return sub

    @coroutine
    def pub(self, message):
        channel = self.name
        return (yield from redis.publish(
            PUBSUB_CHANNEL_TEMPLATE.format(self.env.name, channel),
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
        # print(json.dumps(conf, indent=4))
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
        self.__args, self.__kargs, self._depend_subs = yield from gather(
            trans_list(args, partial(bind, env)),
            trans_dict(kargs, partial(bind, env)),
            trans_dict(dict(zip(self.depends, self.depends)), self.sub)
        )
        return self

    @coroutine
    def _eval(self):
        self.__args, self.__kargs, self.depend_result = yield from gather(
            trans_list(self.__args, eval),
            trans_dict(self.__kargs, eval),
            trans_dict(self._depend_subs, next_result)
            # Can't use lambda here, don't know why
            # trans_dict(
                # self._depend_subs,
                # coroutine(lambda sub: json.loads(
                    # (yield from sub.next_published()).value
                # ))
            # )
        )
        if '@' in self.__kargs:
            raise lang.LangError(
                'Wrong arg of @{}[{}]. Maybe missing a [ ] outside?'.format(
                    self.kind,
                    self.name
                )
            )
        result = yield from self(*self.__args, **self.__kargs)
        yield from self.pub(result)
        return result

    @classmethod
    def try_expand_shortcut(cls, key, value):
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
            raise lang.LangError('Unknown target type: %s' % name)
        lib = importlib.import_module('..' + name, __name__)
        return lib.Target
    except Exception as e:
        raise lang.LangError('Unknown target: ' + name) from e


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
    return (yield from gather(*[func(item) for item in conf]))


@coroutine
def trans_dict(conf, func):
    return dict(zip(
        conf,
        (yield from gather(*[func(conf[key]) for key in conf]))
    ))


def try_expand_shortcut(conf):
    if len(conf) != 1:
        return conf

    key = next(iter(conf))

    for cls in map(targetcls, sorted(target_types(), reverse=True)):
        basic_prefix = '@' + cls.kind
        if re.search('^' + basic_prefix + '[^_\w\d]', key + '$'):
            expanded = cls._expand_prefix_shortcut(key, conf[key], basic_prefix)
        else:
            expanded = cls.try_expand_shortcut(key, conf[key])
        if expanded is not None:
            expanded['@'] = cls.kind
            name_match = NAME_RE.search(key)
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


@coroutine
def next_result(sub):
    return json.loads((yield from sub.next_published()).value)
