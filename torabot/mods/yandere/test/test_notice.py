from nose.tools import assert_is_not_none, assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import POSTS_URI_QUERY_RESULT


def check_format_notice(view, notice):
    app = make()
    with app.test_client():
        assert_is_not_none(mod(name).format_notice_body(view, notice))


def test_format_notice():
    for notice in [
        bunchr({
            'change': {
                'kind': 'post.new',
                'post': POSTS_URI_QUERY_RESULT['posts'][0],
                'query_text': 'foo'
            }
        }),
    ]:
        yield check_format_notice, 'web', notice
        yield check_format_notice, 'email', notice


def test_notice_attachments():
    app = make()
    with app.test_client():
        assert_equal(len(mod(name).notice_attachments('email', bunchr({
            'change': {
                'kind': 'post.new',
                'post': POSTS_URI_QUERY_RESULT['posts'][0],
                'query_text': 'foo'
            }
        }))), 1)
