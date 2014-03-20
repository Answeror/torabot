from stevedore.driver import DriverManager


def mod(name):
    return DriverManager(
        'torabot.mods',
        name,
        invoke_on_load=True,
    ).driver
