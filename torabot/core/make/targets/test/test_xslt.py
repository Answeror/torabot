import os
import feedparser
from nose.tools import assert_greater
from ...envs.fs import Env
from ..xslt import Target as XsltTarget


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')


def test_xslt():
    for html, xslt in [
        ('bgm_pm.html', 'bgm_pm.xslt'),
        ('bgm_blog_51939.html', 'bgm_comments.xslt'),
        ('bgm_group_topic_32268.html', 'bgm_comments.xslt'),
        ('bgm_subject_topic_4369.html', 'bgm_comments.xslt'),
    ]:
        yield check_xslt, html, xslt


def check_xslt(html, xslt):
    env = Env(root=CURRENT_PATH)
    target = XsltTarget(env)
    feed = feedparser.parse(target(
        html=read(html),
        xslt={
            '@type': 'text',
            'name': xslt
        }
    ).encode('utf-8'))
    assert_greater(len(feed.entries), 0)
