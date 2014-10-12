import os
from .conf import init_conf


class Local(object):

    def __init__(self, conf='toraconf'):
        self._conf = conf

    @property
    def conf(self):
        try:
            from flask import current_app
            return current_app.config
        except:
            if isinstance(self._conf, str):
                from flask import Config
                conf = Config(os.getcwd())
                init_conf(conf, self._conf)
                self._conf = conf
            return self._conf

    @property
    def secret_key(self):
        try:
            from flask import current_app
            return current_app.secret_key
        except:
            return self.conf['SECRET_KEY']

    @property
    def redis(self):
        value = getattr(self, '_redis', None)
        if value is None:
            from redis import StrictRedis
            self._redis = value = StrictRedis(
                host=self.conf.get('TORABOT_REDIS_HOST', 'localhost'),
                port=self.conf.get('TORABOT_REDIS_PORT', 6379)
            )
        return value


local = Local()
