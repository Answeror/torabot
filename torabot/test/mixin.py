from .g import g
from ..model import Base, Session


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

    def teardown(self):
        self.transaction.rollback()
