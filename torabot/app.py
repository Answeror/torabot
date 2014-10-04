from flask import Flask
from .app_mixins import RedisPubMixin
from .ut.conf import init_conf


class App(RedisPubMixin, Flask):

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
        init_conf(self.config, 'toraconf')
        if config is not None:
            self.config.update(config)

    def _init_parts(self):
        from . import frontend
        from .core import mod

        for part in [frontend, mod]:
            part.make(self)

    def __call__(self, *args, **kargs):
        with self.redispub.applicationbound():
            return super(App, self).__call__(*args, **kargs)
