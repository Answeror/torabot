from nose.tools import assert_equal
from .const import USERNAME_QUERY_RESULT, QUERY_RESULT
from ....ut.async_test_tools import with_event_loop
from .. import bilibili
from . import TestSuite


BASE = {
    'area': '日本',
    'areaid': 2,
    'attention': 372,
    'bgmcount': '1',
    'click': 20280,
    'cover': 'http://i1.hdslb.com/sp/ef/ef79722341701e523addad0ff683f622.jpg',
    'mcover': 'http://i1.hdslb.com/sp/ef/ef79722341701e523addad0ff683f622.jpg',
    'new': True,
    'priority': 0,
    'scover': 'http://i1.hdslb.com/sp/ef/ef79722341701e523addad0ff683f622.jpg',
    'spid': 19315,
    'title': '风云维新大将军',
    'typeid': 1,
    'weekday': 4
}


class TestChanges(TestSuite):

    @with_event_loop
    def test_no_change(self):
        changes = yield from bilibili.changes(
            dict(
                kind='sp',
                sp=dict(
                    lastupdate=1397091797,
                    lastupdate_at='2014-04-10 09:03',
                    **BASE
                )
            ),
            dict(
                kind='sp',
                sp=dict(
                    lastupdate=1397091797,
                    lastupdate_at='2014-04-10 09:03',
                    **BASE
                )
            ),
        )
        assert_equal(len(changes), 0)

    @with_event_loop
    def test_one_change(self):
        changes = yield from bilibili.changes(
            dict(
                kind='sp',
                sp=dict(
                    lastupdate=1397091797,
                    lastupdate_at='2014-04-10 09:03',
                    **BASE
                )
            ),
            dict(
                kind='sp',
                sp=dict(
                    lastupdate=1397091798,
                    lastupdate_at='2014-04-10 09:04',
                    **BASE
                )
            ),
        )
        assert_equal(len(changes), 1)
        assert_equal(changes[0].kind, 'sp_update')

    @with_event_loop
    def test_username_query_no_change(self):
        changes = yield from bilibili.changes(
            USERNAME_QUERY_RESULT,
            USERNAME_QUERY_RESULT
        )
        assert_equal(len(changes), 0)

    @with_event_loop
    def test_username_query_change(self):
        r = USERNAME_QUERY_RESULT
        changes = yield from bilibili.changes(
            dict(query=r['query'], posts=r['posts'][1:]),
            dict(query=r['query'], posts=r['posts'])
        )
        assert_equal(len(changes), 1)

    @with_event_loop
    def test_query_no_change(self):
        changes = yield from bilibili.changes(
            QUERY_RESULT,
            QUERY_RESULT
        )
        assert_equal(len(changes), 0)

    @with_event_loop
    def test_query_change(self):
        r = QUERY_RESULT
        changes = yield from bilibili.changes(
            dict(query=r['query'], posts=r['posts'][1:]),
            dict(query=r['query'], posts=r['posts'])
        )
        assert_equal(len(changes), 1)
