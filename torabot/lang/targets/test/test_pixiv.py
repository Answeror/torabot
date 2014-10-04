import json
from ....ut.async_local import local
from ....ut.async_test_tools import with_event_loop
from .. import Target
from nose.tools import assert_equal
from .ut import make_fs_env


@with_event_loop
def test_pixiv():
    result = yield from Target.run(
        make_fs_env(),
        {
            '@eval': {
                '@js': [
                    {'text<': 'pixiv.js'},
                    [
                        local.conf['TORABOT_TEST_PIXIV_USERNAME'],
                        local.conf['TORABOT_TEST_PIXIV_PASSWORD']
                    ]
                ]
            }
        }
    )
    assert_equal(len(json.loads(result)['arts']), 20)
    query = {
        'text': 'pixiv',
        'mtime': 0,
        'result': {
            'arts': json.loads(result)['arts'][:13]
        }
    }
    result = {
        'arts': json.loads(result)['arts'][10:]
    }
    changes = yield from Target.run(
        make_fs_env(),
        {
            '@js': {
                'code': {'text<': 'pixiv_changes.js'},
                'func': 'changes',
                'args': [query, result]
            }
        }
    )
    assert_equal(len(changes), 7)
