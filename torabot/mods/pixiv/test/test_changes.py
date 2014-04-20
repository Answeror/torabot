from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import USER_ID_QUERY, USER_ARTS, RANKING_QUERY, RANKING_ARTS


def test_user_id_no_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(query=USER_ID_QUERY, arts=USER_ARTS),
            bunchr(query=USER_ID_QUERY, arts=USER_ARTS),
        ))
        assert_equal(len(changes), 0)


def test_user_id_new_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(query=USER_ID_QUERY, arts=USER_ARTS[1:]),
            bunchr(query=USER_ID_QUERY, arts=USER_ARTS),
        ))
        assert_equal(len(changes), 1)


def test_ranking_arts_no_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(query=RANKING_QUERY, arts=RANKING_ARTS),
            bunchr(query=RANKING_QUERY, arts=RANKING_ARTS),
        ))
        assert_equal(len(changes), 0)


def test_ranking_arts_new_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(query=RANKING_QUERY, arts=RANKING_ARTS[:-1]),
            bunchr(query=RANKING_QUERY, arts=RANKING_ARTS[1:]),
        ))
        assert_equal(len(changes), 1)
        assert_equal(len(changes[0].arts), 1)
