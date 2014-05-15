import json
from nose.tools import assert_greater
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name


@need_scrapyd
def test_spy_post_uri():
    app = make()
    with app.test_client():
        uri = 'http://danbooru.donmai.us/posts?tags=pantyhose'
        d = mod(name).spy(json.dumps(dict(method='posts_uri', uri=uri)), 60)
        assert_greater(len(d.posts), 0)
        d = mod(name).spy(uri, 60)
        assert_greater(len(d.posts), 0)


@need_scrapyd
def check_spy_query(query):
    app = make()
    with app.test_client():
        d = mod(name).spy(json.dumps(dict(method='query', query=query)), 60)
        assert_greater(len(d.posts), 0)
        d = mod(name).spy(query, 60)
        assert_greater(len(d.posts), 0)


def test_spy_query():
    for query in [
        'pantyhose feet',
        'pantyhose -feet'
    ]:
        yield check_spy_query, query
