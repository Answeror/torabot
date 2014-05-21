from ....ut.bunch import bunchr
from ...ut import check_format_notice_body_not_none
from .. import name
from .const import URI_QUERY_RESULT


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
