import json
from nose.tools import assert_equal
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name
from ..query import parse


@need_scrapyd
def check_spy_contains_query(query):
    app = make()
    with app.test_client():
        d = mod(name).spy(query, 60)
        assert_equal(d.query, parse(query))


def test_spy_contains_query():
    for query in [
        json.dumps(dict(
            method='user_id',
            user_id='511763'
        )),
        json.dumps(dict(
            method='user_uri',
            uri='http://www.pixiv.net/member.php?id=511763'
        )),
        json.dumps(dict(
            method='user_illustrations_uri',
            uri='http://www.pixiv.net/member_illust.php?id=511763'
        )),
        'http://www.pixiv.net/member.php?id=511763',
        'http://www.pixiv.net/member_illust.php?id=511763',
    ]:
        yield check_spy_contains_query, query
