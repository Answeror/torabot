from flask import Flask
from .core.log import RedisPub


class App(Flask):

    def __init__(self, *args, **kargs):
        super(App, self).__init__(
            *args,
            **{name: kargs[name] for name in (
                'instance_path',
                'instance_relative_config',
            ) if name in kargs}
        )
        self._init_conf(kargs.get('config'))
        self._init_parts()

        from .cache import cache
        cache.init_app(self)

    def _init_conf(self, config):
        try:
            import toraconf
            self.config.from_object(toraconf)
        except:
            from . import conf
            self.config_from_object(conf)

        if config is not None:
            self.config.update(config)

    def _init_parts(self):
        from . import frontend
        from . import api
        from .core import mod

        for part in [frontend, api, mod]:
            part.make(self)

    @property
    def redispub(self):
        if not hasattr(self, '_redispub'):
            self._redispub = RedisPub(
                bubble=self.config['TORABOT_BUBBLE_LOG']
            )
        return self._redispub

    def __call__(self, *args, **kargs):
        with self.redispub.threadbound():
            return super(App, self).__call__(*args, **kargs)
