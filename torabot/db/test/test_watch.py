from nose.tools import assert_raises
from ..user import add_user
from ..watch import watch
from ..query import add_query
from . import g


def test_maxwatch():
    with g.connection.begin_nested() as trans:
        user_id = add_user(
            g.connection,
            name='answeror',
            email='answeror+torabot@gmail.com',
            openid='whatever',
        )

        query_ids = []
        for i in range(43):
            query_ids.append(add_query(
                g.connection,
                text=str(i)
            ))

        for query_id in query_ids[:-1]:
            watch(g.connection, user_id=user_id, query_id=query_id)

        assert_raises(Exception, watch, g.connection, user_id, query_ids[-1])
        trans.rollback()
