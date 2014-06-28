from uuid import uuid4


class Base(object):

    @property
    def name(self):
        key = '_name'
        value = getattr(self, key, None)
        if value is None:
            value = str(uuid4())
            setattr(self, key, value)
        return value

    def __init__(self, env, options=None):
        self.env = env
        self.options = {} if options is None else options

    def read(self, name):
        return self.env.read(name)

    def read_text(self, name):
        return self.read(name).decode('utf-8')
