import json
import jinja2
import feedparser
from nose.tools import assert_equal, assert_greater
from ....ut.local import local
from ....ut.async_test_tools import with_event_loop
from .. import Target
from .ut import make_fs_env, read


@with_event_loop
def test_toy():
    assert_equal((yield from Target.run(
        make_fs_env(),
        json.loads(read('toy.json'))
    )), 0)


@with_event_loop
def test_bgm_pm_task():
    result = yield from Target.run(
        make_fs_env(),
        json.loads(jinja2.Template(read('bgm_pm.json')).render(
            chii_auth=local.conf['TORABOT_TEST_CHII_AUTH']
        ))
    )
    feed = feedparser.parse(result)
    assert not feed.bozo
    assert_greater(len(feed.entries), 0)


@with_event_loop
def test_bgm_comments_task():
    result = yield from Target.run(
        make_fs_env(),
        json.loads(jinja2.Template(read('bgm_comments.json')).render(
            path='/group/topic/32268'
        ))
    )
    feed = feedparser.parse(result)
    assert not feed.bozo
    assert_greater(len(feed.entries), 0)


@with_event_loop
def test_bgm_comments_compact_task():
    result = yield from Target.run(
        make_fs_env(),
        json.loads(jinja2.Template(read('bgm_comments_compact.json')).render(
            path='/group/topic/32268'
        ))
    )
    feed = feedparser.parse(result)
    assert not feed.bozo
    assert_greater(len(feed.entries), 0)
