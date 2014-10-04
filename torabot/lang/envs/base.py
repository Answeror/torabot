import abc
from uuid import uuid4


class Base(metaclass=abc.ABCMeta):

    def __init__(self):
        self.result = {}
        self.context = {}
        self.name = str(uuid4())

    @abc.abstractmethod
    def read(self, name):
        pass
