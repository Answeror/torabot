import base64
from .base import Base


class Env(Base):

    def __init__(self, d):
        self.d = d

    def read(self, name):
        for f in self.d['files']:
            if f['name'] == name:
                return base64.b64decode(f.content)
        raise Exception('no file named %s' % name)
