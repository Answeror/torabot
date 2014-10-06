from time import time
from nose.tools import assert_equal, assert_less
from ....ut.async_local import local
from ....ut.async_test_tools import with_event_loop
from .. import Target
from .ut import make_fs_env


@with_event_loop
def test_pixiv_download_top_10():
    start = time()
    result = yield from Target.run(
        make_fs_env(),
        {
            '@eval': {
                '@js': [
                    {'text<': 'pixiv_download_top_10.js'},
                    [
                        local.conf['TORABOT_TEST_PIXIV_USERNAME'],
                        local.conf['TORABOT_TEST_PIXIV_PASSWORD'],
                        "download_arts_parallel"
                    ]
                ]
            }
        }
    )
    assert_equal(len(result), 10)
    parallel_time = time() - start

    start = time()
    result = yield from Target.run(
        make_fs_env(),
        {
            '@eval': {
                '@js': [
                    {'text<': 'pixiv_download_top_10.js'},
                    [
                        local.conf['TORABOT_TEST_PIXIV_USERNAME'],
                        local.conf['TORABOT_TEST_PIXIV_PASSWORD'],
                        "download_arts_sequence"
                    ]
                ]
            }
        }
    )
    assert_equal(len(result), 10)
    sequence_time = time() - start

    assert_less(parallel_time + 1, sequence_time)
