from asyncio import coroutine
from ..errors import LangError
from .base import Base


class Target(Base):

    unary = True
    shortcut_prefix = '&'

    @coroutine
    def __call__(self, name):
        none = object()
        value = self.depend_result.get(name, none)
        if value is none:
            raise LangError("Result of %s haven't been computed" % name)
        return value

    @classmethod
    def _postprocess_conf(cls, conf):
        conf = Base._postprocess_conf(conf)
        depends = conf.get('depends', [])
        if 'arg' in conf:
            depends.append(conf['arg'])
        elif 'args' in conf and conf['args']:
            depends.append(conf['args'][0])
        elif 'kargs' in conf and 'name' in conf['kargs']:
            depends.append(conf['kargs']['name'])
        conf['depends'] = depends
        return conf
