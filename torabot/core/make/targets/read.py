import jsonpickle
from .base import Base


class Target(Base):

    def __call__(self, name, type):
        return {
            'blob': self.read,
            'text': self.read_text,
            'json': self.read_json,
        }[type](name)

    def read(self, name):
        return self.env.read(name)

    def read_text(self, name):
        return self.read(name).decode('utf-8')

    def read_json(self, name):
        return jsonpickle.decode(self.read_text(name))
