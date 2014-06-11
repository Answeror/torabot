from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import USERNAME_QUERY_RESULT, QUERY_RESULT


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


def test_no_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(kind='sp', sp=dict(lastupdate=1397091797, lastupdate_at='2014-04-10 09:03', **BASE)),
            bunchr(kind='sp', sp=dict(lastupdate=1397091797, lastupdate_at='2014-04-10 09:03', **BASE)),
        ))
        assert_equal(len(changes), 0)


def test_one_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(kind='sp', sp=dict(lastupdate=1397091797, lastupdate_at='2014-04-10 09:03', **BASE)),
            bunchr(kind='sp', sp=dict(lastupdate=1397091798, lastupdate_at='2014-04-10 09:04', **BASE)),
        ))
        assert_equal(len(changes), 1)
        assert_equal(changes[0].kind, 'sp_update')


def test_username_query_no_change():
    app = make()
    with app.app_context():
        changes = list(mod(name).changes(
            bunchr(USERNAME_QUERY_RESULT),
            bunchr(USERNAME_QUERY_RESULT)
        ))
        assert_equal(len(changes), 0)


def test_username_query_change():
    app = make()
    with app.app_context():
        r = USERNAME_QUERY_RESULT
        changes = list(mod(name).changes(
            bunchr(query=r['query'], posts=r['posts'][1:]),
            bunchr(query=r['query'], posts=r['posts'])
        ))
        assert_equal(len(changes), 1)


def test_query_no_change():
    app = make()
    with app.app_context():
        changes = list(mod(name).changes(
            bunchr(QUERY_RESULT),
            bunchr(QUERY_RESULT)
        ))
        assert_equal(len(changes), 0)


def test_query_change():
    app = make()
    with app.app_context():
        r = QUERY_RESULT
        changes = list(mod(name).changes(
            bunchr(query=r['query'], posts=r['posts'][1:]),
            bunchr(query=r['query'], posts=r['posts'])
        ))
        assert_equal(len(changes), 1)
