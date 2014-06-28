import jsonpickle
from .base import Base


class Target(Base):

    def __call__(self, name):
        return jsonpickle.decode(self.read(name).decode('utf-8'))
