from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from ...ut import check_format_notice_body_not_empty
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
        for view in ['web', 'email']:
            yield check_format_notice_body_not_empty, name, view, notice


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
