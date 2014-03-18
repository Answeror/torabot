from .. import mods
from .spy import spy


def mod(name):
    return Mod(getattr(mods, name))


class Mod(object):

    def __init__(self, mod):
        self.mod = mod

    @property
    def name(self):
        return self.mod.__name__.split('.')[-1]

    @property
    def kind(self):
        return self.name

    def spy(self, query):
        return spy(self.name, query)
