import os
import feedparser
from ..ut import entry_id


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def test_entry_id():
    feed = feedparser.parse(os.path.join(CURRENT_PATH, 'itokoo.xml'))
    for e in feed.entries:
        assert entry_id(e)
