import os
import re
import pkgutil
import importlib
from ..ut.facade import Facade as Base
from . import core


NAME_RE = re.compile('^[_\w][_\d\w]*$')


class Modo(Base):

    def init_app(self, app):
        super().init_app(app)

        app.config.setdefault('TORABOT_SPY_TIMEOUT', 30)

        for mod in self.all():
            mod.init_app(app)

    def get(self, name):
        if not NAME_RE.match(name):
            raise core.CoreError('Illegal mod name: ' + name)
        try:
            lib = importlib.import_module('...mods.' + name, __name__)
        except Exception as e:
            raise core.CoreError('Unknown mod: ' + name) from e
        if not hasattr(lib, name):
            raise core.CoreError("Mod %s haven't facade" % name)
        return getattr(lib, name)

    def all(self):
        root = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '..',
            'mods'
        ))
        return [
            self.get(name) for _, name, _ in pkgutil.iter_modules([root])
            if name in ['bilibili']
        ]


@core.initializer
def init_app(app):
    modo.init_app(app)


modo = Modo()


__all__ = ['Modo', 'modo']
