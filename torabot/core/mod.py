from stevedore.driver import DriverManager
from stevedore.extension import ExtensionManager
from .local import get_current_conf


def mod(name):
    return DriverManager(
        'torabot.mods',
        name,
        invoke_on_load=True,
        invoke_args=(get_current_conf(),),
    ).driver


def mods():
    return [e.obj for e in ExtensionManager(
        'torabot.mods',
        invoke_on_load=True,
        invoke_args=(get_current_conf(),)
    )]
