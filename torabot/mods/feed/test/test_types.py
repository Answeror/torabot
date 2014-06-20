import os
import feedparser
from ..types import Feed


CURRENT_PATH = os.path.dirname(__file__)


def test_best_content_text():
    with open(os.path.join(CURRENT_PATH, 'yandere.xml'), 'rb') as f:
        feed = Feed(feedparser.parse(f.read()))
    assert feed.entries[0].best_content_text
