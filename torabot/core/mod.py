from stevedore.driver import DriverManager
from .local import get_current_conf


def mod(name):
    return DriverManager(
        'torabot.mods',
        name,
        invoke_on_load=True,
        invoke_args=(dict(**get_current_conf()),),
    ).driver
