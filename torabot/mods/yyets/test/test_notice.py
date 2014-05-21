from ....ut.bunch import bunchr
from ...ut import check_format_notice_body_not_none
from .. import name
from .const import RSS_RESULT


def test_format_notice():
    for notice in [
        bunchr({
            'change': {
                'kind': 'rss.new',
                'art': RSS_RESULT['arts'][0]
            }
        })
    ]:
        for view in ['web', 'email']:
            yield check_format_notice_body_not_none, name, view, notice
