from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import SEARCH_QUERY_RESULT


def test_format_notice():
    for notice in [
        bunchr({
            'change': {
                'kind': 'post.new',
                'post': SEARCH_QUERY_RESULT['posts'][0],
                'query': SEARCH_QUERY_RESULT['query']
            }
        })
    ]:
        app = make()
        with app.app_context():
            assert mod(name).format_notice_body('web', notice)
        assert mod(name).format_notice_body('email', notice)


def test_notice_attachments():
    app = make()
    with app.app_context():
        assert_equal(len(mod(name).notice_attachments('email', bunchr({
            'change': {
                'kind': 'post.new',
                'post': SEARCH_QUERY_RESULT['posts'][0],
                'query': SEARCH_QUERY_RESULT['query']
            }
        }))), 1)
