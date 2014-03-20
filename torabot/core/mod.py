from stevedore.driver import DriverManager
from .spy import spy


def mod(name):
    return Mod(DriverManager(
        'torabot.mods',
        name,
        invoke_on_load=True,
    ).driver)


class Mod(object):

    def __init__(self, driver):
        self.driver = driver

    def spy(self, query, timeout, **kargs):
        return spy(self.name, query, timeout, **kargs)

    def __getattr__(self, name):
        return getattr(self.driver, name)
