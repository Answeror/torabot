import os
import base64
from .base import Base


class Env(Base):

    def __init__(self, d, root):
        super(Env, self).__init__()
        self.d = d
        self.root = root

    def read(self, name):
        for f in self.d['files']:
            if f['name'] == name:
                value = f.get('content')
                if value is not None:
                    return base64.decode(f.content)
                with open(os.path.join(self.root, f['path']), 'rb') as o:
                    return o.read()
        raise Exception('no file named %s' % name)
