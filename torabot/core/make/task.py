import jinja2
import jsonpickle
import importlib
from uuid import uuid4
from .envs.dict import Env as DictEnv


class Task(object):

    def __init__(self, env, get, target_confs):
        self.env = env
        self.get = get
        self.target_confs = target_confs
        self.result = {}

    @classmethod
    def from_string(cls, text, make_env=DictEnv):
        get = {}
        text = jinja2.Template(text).render(target=Mock(get))
        d = jsonpickle.decode(text)
        env = make_env(d)
        return cls(env, get, d['targets'])

    def __call__(self):
        for conf in self.target_confs:
            self.fill(conf)
            target = self.make_target(conf['type'], self.env, conf.get('options'))
            self.result[conf['name']] = target(**conf.get('input'))
        else:
            return self.result[conf['name']]

    def fill(self, conf):
        if not isinstance(conf, dict):
            return

        for key in list(conf):
            if isinstance(conf[key], str):
                if conf[key] in self.get:
                    conf[key] = self.get[conf[key]](self.result)
            else:
                self.fill(conf[key])

    def make_target(self, name, *args, **kargs):
        lib = importlib.import_module('..targets.' + name, __name__)
        return lib.Target(*args, **kargs)


class Mock(object):

    def __init__(self, get, parent=None, field=None):
        self.get = get
        self.id = str(uuid4())
        self.parent = parent
        self.field = field
        self.get[self.id] = self

    def __call__(self, d):
        if not self.parent:
            return d
        d = self.parent.get[self.parent.id](d)
        if isinstance(d, str):
            d = jsonpickle.decode(d)
        return d[self.field]

    def __getattr__(self, key):
        return Mock(self.get, parent=self, field=key)

    def __getitem__(self, key):
        return Mock(self.get, parent=self, field=key)

    def __str__(self):
        return self.id
