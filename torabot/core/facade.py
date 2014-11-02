from flask import url_for, current_app
from asyncio import coroutine
from ..db import db
from ..ut.redis import redis
from ..ut.facade import Facade as Base, blueprint_mixin


class Core(blueprint_mixin(__name__), Base):

    name = 'core'
    activate_user_path = '/activate/%(payload)s'
    reset_password_path = '/reset/%(payload)s'

    class CoreError(Exception):
        pass

    class ExpectedError(CoreError):
        pass

    def init_app(self, app):
        super().init_app(app)

        db.init_app(app)
        redis.init_app(app)

        if not app.config.get('SERVER_NAME'):
            app.config['SERVER_NAME'] = 'rss.moe'

        app.config.setdefault('TORABOT_TELL_ADMIN_NEW_USER', True)
        app.config.setdefault('TORABOT_ADMIN_IDS', [1])

    @property
    def index_uri(self):
        try:
            return url_for('main.index', _external=True)
        except:
            return 'http://' + current_app.config['SERVER_NAME']

    def regular(self, kind, text):
        while True:
            next_kind, next_text = self.mod(kind).regular(text)
            if (next_kind, next_text) == (kind, text):
                break
            kind, text = next_kind, next_text
        return kind, text

    @coroutine
    def search(self, kind, text, **kargs):
        return (yield from self.mod(kind).search(text, **kargs))

    def mod(self, name):
        from .modo import modo
        return modo.get(name)


__all__ = ['Core']
