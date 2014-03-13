from nose.tools import assert_is_not_none
from . import g
from ..user import add_user


def test_add_user():
    with g.connection.begin_nested() as trans:
        assert_is_not_none(add_user(
            g.connection,
            name='answeror',
            email='answeror+torabot@gmail.com',
            openid='whatever',
        ))
        trans.rollback()
