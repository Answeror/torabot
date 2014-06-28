import abc


class Base(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read(self, name):
        pass
