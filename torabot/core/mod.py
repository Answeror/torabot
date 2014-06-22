from stevedore.extension import ExtensionManager


class Mod(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    @property
    def manager(self):
        name = '_manager'
        value = getattr(self, name, None)
        if value is None:
            from .local import get_current_conf
            value = ExtensionManager(
                'torabot.mods',
                invoke_on_load=True,
                invoke_args=(get_current_conf(),)
            )
            setattr(self, name, value)
        return value

    def init_app(self, app):
        self.register_mod_blueprints(app)
        self.register_standalone_blueprints(app)

    def register_mod_blueprints(self, app):
        with app.app_context():
            for m in mods():
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


def frontend_mods():
    from ..mods.base import Frontend
    return [m for m in mod.values if isinstance(m, Frontend)]


def make(app):
    mod.init_app(app)
