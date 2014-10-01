import os
import jinja2
import feedparser
import jsonpickle
from nose.tools import assert_equal, assert_greater
from ..... import make
from ...envs.fs import Env
from .. import Target


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')


def test_toy():
    assert_equal(Target.run(
        Env(CURRENT_PATH),
        jsonpickle.decode(read('toy.json'))
    ), 0)


def test_bgm_pm_task():
    app = make()
    with app.app_context():
        result = Target.run(
            Env(CURRENT_PATH),
            jsonpickle.decode(jinja2.Template(read('bgm_pm.json')).render(
                chii_auth=read('chii_auth').strip()
            ))
        )
        feed = feedparser.parse(result)
        assert not feed.bozo
        assert_greater(len(feed.entries), 0)


def test_bgm_comments_task():
    app = make()
    with app.app_context():
        result = Target.run(
            Env(CURRENT_PATH),
            jsonpickle.decode(jinja2.Template(read('bgm_comments.json')).render(
                path='/group/topic/32268'
            ))
        )
        feed = feedparser.parse(result)
        assert not feed.bozo
        assert_greater(len(feed.entries), 0)


def test_bgm_comments_compact_task():
    app = make()
    with app.app_context():
        result = Target.run(
            Env(CURRENT_PATH),
            jsonpickle.decode(jinja2.Template(read('bgm_comments_compact.json')).render(
                path='/group/topic/32268'
            ))
        )
        feed = feedparser.parse(result)
        assert not feed.bozo
        assert_greater(len(feed.entries), 0)
