from stevedore.extension import ExtensionManager
from logbook import Logger
from .local import get_current_conf


log = Logger(__name__)


class Mod(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

        self.manager = ExtensionManager(
            'torabot.mods',
            invoke_on_load=True,
            invoke_args=(get_current_conf(),)
        )

    def init_app(self, app):
        self.register_mod_blueprints(app)
        self.register_standalone_blueprints(app)

    def register_mod_blueprints(self, app):
        with app.app_context():
            for m in mods():
                log.info('load mod {}', m.name)
                bp = getattr(m, 'blueprint', None)
                if bp is not None:
                    app.register_blueprint(bp)

    def register_standalone_blueprints(self, app):
        from ..mods.booru.blueprint import bp
        app.register_blueprint(bp)

    @property
    def values(self):
        name = '_values'
        value = getattr(self, name, None)
        if value is None:
            value = sorted([e.obj for e in self.manager], key=lambda o: o.name)
            setattr(self, name, value)
        return value

    def __call__(self, name):
        return self.manager[name].obj

    def __iter__(self):
        return iter(self.items())

    def __getitem__(self, index):
        return self.values


mod = Mod()


def mods():
    return mod.values


def make(app):
    mod.init_app(app)
