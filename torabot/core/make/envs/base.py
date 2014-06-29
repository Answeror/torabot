import abc


class Base(metaclass=abc.ABCMeta):

    def __init__(self):
        self.result = {}

    @abc.abstractmethod
    def read(self, name):
        pass
