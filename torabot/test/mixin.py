from .g import g
from ..model import Base, Session
from ..redis import redis


class ModelMixin(object):

    @classmethod
    def setup_class(cls):
        cls._transaction = g.connection.begin_nested()
        Base.metadata.create_all(g.connection)
        Session.configure(bind=g.connection)

    @classmethod
    def teardown_class(cls):
        cls._transaction.rollback()

    def setup(self):
        self.transaction = g.connection.begin_nested()
        redis.delete('change')
        redis.delete('notice')

    def teardown(self):
        redis.delete('notice')
        redis.delete('change')
        self.transaction.rollback()
