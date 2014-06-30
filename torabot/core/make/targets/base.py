import importlib
from uuid import uuid4
from nose.tools import assert_is_instance


none = object()


class Base(object):

    @classmethod
    def run(cls, env, conf):
        if isinstance(conf, dict):
            conf = {key: cls.run(env, conf[key]) for key in conf}

            for symbol, kind, unary in [
                ('&', 'use', True),
                ('[]', 'item', False),
                ('<', 'read', False),
            ]:
                parse_shortcut(conf, symbol, kind, unary)

            kind = conf.get('@', none)
            if kind is not none:
                if '.' in kind:
                    raise Exception('unknown target type: %s' % kind)
                lib = importlib.import_module('..' + kind, __name__)
                target = lib.Target(env=env, name=conf.get('name'))
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


def parse_shortcut(conf, symbol, kind, unary):
    item = conf.get(symbol, none)
    if item is not none:
        del conf[symbol]
        conf.update({
            '@': kind,
            'arg' if unary else {
                list: 'args',
                dict: 'kargs'
            }[type(item)]: item
        })
