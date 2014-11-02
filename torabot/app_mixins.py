from .ut.log import RedisPub


class RedisPubMixin(object):

    def get_conf(self, name, default=None):
        try:
            from flask import Flask
            if isinstance(self, Flask):
                return self.config.get(name, default)
        except ImportError:
            pass

        try:
            from celery import Celery
            if isinstance(self, Celery):
                return self.conf.get(name, default)
        except ImportError:
            pass

        assert False

    @property
    def redispub(self):
        if not hasattr(self, '_redispub'):
            self._redispub = RedisPub(
                bubble=self.get_conf('TORABOT_BUBBLE_LOG', True)
            )
        return self._redispub
