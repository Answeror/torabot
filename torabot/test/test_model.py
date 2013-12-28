from .g import g
from ..model import Base, Session, Art
from .. import state
from nose.tools import assert_equal


class TestModel(object):

    @classmethod
    def setup_class(cls):
        cls._transaction = g.connection.begin()
        Base.metadata.create_all(g.connection)
        Session.configure(bind=g.connection)

    @classmethod
    def teardown_class(cls):
        cls._transaction.rollback()

    def setup(self):
        self.transaction = g.connection.begin()

    def teardown(self):
        self.transaction.rollback()

    def test_add_art(self):
        s = Session()
        s.add(Art(
            title='foo',
            author='bar',
            comp='foobar',
            toraid='123456789012',
            state=state.RESERVE,
        ))
        s.commit()
        assert_equal(s.query(Art).count(), 1)
