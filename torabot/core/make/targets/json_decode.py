import jsonpickle
from .base import Base


class Target(Base):

    def __call__(self, text):
        return jsonpickle.decode(text)
