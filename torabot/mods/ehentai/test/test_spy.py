from nose.tools import assert_greater
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name


@need_scrapyd
def test_spy_query():
    app = make()
    with app.app_context():
        d = mod(name).spy('language:chinese', 60)
        assert_greater(len(d.posts), 0)
        d = mod(name).spy('http://g.e-hentai.org/?f_search=language%3Achinese', 60)
        assert_greater(len(d.posts), 0)
