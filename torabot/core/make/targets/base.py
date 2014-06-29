import importlib
from uuid import uuid4
from nose.tools import assert_is_instance


class Base(object):

    @classmethod
    def run(cls, env, conf):
        none = object()
        if isinstance(conf, dict):
            conf = {key: cls.run(env, conf[key]) for key in conf}

            use = conf.get('&', none)
            if use is not none:
                del conf['&']
                conf.update({
                    '@': 'use',
                    'args': [use]
                })

            item = conf.get('[]', none)
            if item is not none:
                del conf['[]']
                conf.update({
                    '@': 'item',
                    {
                        list: 'args',
                        dict: 'kargs'
                    }[type(item)]: item
                })

            kind = conf.get('@', none)
            if kind is not none:
                if '.' in kind:
                    raise Exception('unknown target type: %s' % kind)
                lib = importlib.import_module('..' + kind, __name__)
                target = lib.Target(env=env, name=conf.get('name'))
                args = conf.get('args', [])
                assert_is_instance(args, list)
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
