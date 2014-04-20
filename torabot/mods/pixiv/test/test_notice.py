from nose.tools import assert_is_not_none, assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import USER_ARTS, RANKING_ARTS


def check_format_notice(view, notice):
    app = make()
    with app.test_client():
        assert_is_not_none(mod(name).format_notice_body(view, notice))


def test_format_notice():
    for notice in [
        bunchr({
            'change': {
                'kind': 'user_art.new',
                'art': USER_ARTS[0]
            }
        }),
        bunchr({
            'change': {
                'kind': 'ranking',
                'mode': 'daily',
                'arts': RANKING_ARTS
            }
        })
    ]:
        yield check_format_notice, 'web', notice
        yield check_format_notice, 'email', notice


def test_notice_attachments():
    app = make()
    with app.test_client():
        assert_equal(len(mod(name).notice_attachments('email', bunchr({
            'change': {
                'kind': 'ranking',
                'mode': 'daily',
                'arts': RANKING_ARTS
            }
        }))), 3)
