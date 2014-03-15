from nose.tools import assert_equal
from ..sync import strict
from ...db.art import art_count
from ...db.query import query_count
from .spider import UsotukiyaSpider as Spider
from . import g
from sqlalchemy.orm import sessionmaker


def sync(makesession):
    strict('大嘘', 32, spider=Spider(), makesession=makesession)


def test_sync():
    with g.connection.begin_nested() as trans:
        makesession = sessionmaker(bind=g.connection)
        sync(makesession)
        assert_equal(art_count(g.connection), 8)
        assert_equal(query_count(g.connection), 1)
        trans.rollback()


#def test_sync_twice(self):
    #s = Session()
    #self.sync(s)
    #self.sync(s)
    #s.commit()
    #assert_equal(s.query(Art).count(), 8)
    #assert_equal(s.query(Change).filter(Change.what == Change.NEW).count(), 8)
    #assert_equal(s.query(Query).count(), 1)
