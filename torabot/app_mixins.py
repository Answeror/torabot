from .core.log import RedisPub


class RedisPubMixin(object):

    @property
    def config(self):
        try:
            from flask import Flask
            if isinstance(self, Flask):
                return super(RedisPubMixin, self).config
        except:
            pass

        try:
            from celery import Celery
            if isinstance(self, Celery):
                return super(RedisPubMixin, self).conf
        except:
            pass

    @property
    def redispub(self):
        if not hasattr(self, '_redispub'):
            self._redispub = RedisPub(
                bubble=self.config['TORABOT_BUBBLE_LOG']
            )
        return self._redispub
