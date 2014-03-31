from stevedore.driver import DriverManager
from stevedore.extension import ExtensionManager
from .local import get_current_conf
from ..ut.bunch import Bunch


g = Bunch()


def manager():
    m = g.get('manager')
    if m is None:
        m = g['manager'] = ExtensionManager(
            'torabot.mods',
            invoke_on_load=True,
            invoke_args=(get_current_conf(),)
        )
    return m


def mod(name):
    return manager()[name]


def mods():
    return [e.obj for e in manager()]
