from nose.tools import assert_equal
from ....ut.bunch import bunchr
from ...ut import check_format_notice_body_not_none
from .. import name
from .const import URI_QUERY_RESULT, FEED_NOTICE, FEED_NOTICE_EMAIL
from .... import make
from .. import Feed


def test_format_notice():
    for notice in [
        bunchr({
            'change': {
                'kind': 'feed.new',
                'entry': URI_QUERY_RESULT['data']['entries'][0],
                'data': URI_QUERY_RESULT['data'],
                'index': 0,
            }
        })
    ]:
        for view in ['web', 'email']:
            yield check_format_notice_body_not_none, name, view, notice


def test_email_notice():
    for notice, desire in [
        (bunchr(FEED_NOTICE), FEED_NOTICE_EMAIL)
    ]:
        yield check_email_notice, notice, desire


def check_email_notice(notice, desire):
    app = make()
    with app.app_context():
        assert_equal(Feed.instance.format_notice_body('email', notice), desire)
