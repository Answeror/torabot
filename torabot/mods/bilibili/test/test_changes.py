from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .ut import need_scrapyd


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


@need_scrapyd
def test_no_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(kind='sp', sp=dict(lastupdate=1397091797, lastupdate_at='2014-04-10 09:03', **BASE)),
            bunchr(kind='sp', sp=dict(lastupdate=1397091797, lastupdate_at='2014-04-10 09:03', **BASE)),
        ))
        assert_equal(len(changes), 0)


@need_scrapyd
def test_one_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(kind='sp', sp=dict(lastupdate=1397091797, lastupdate_at='2014-04-10 09:03', **BASE)),
            bunchr(kind='sp', sp=dict(lastupdate=1397091798, lastupdate_at='2014-04-10 09:04', **BASE)),
        ))
        assert_equal(len(changes), 1)
        assert_equal(changes[0].kind, 'sp_update')
