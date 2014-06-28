import os
import feedparser


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def test_bozo():
    feed = feedparser.parse(os.path.join(CURRENT_PATH, 'hexieshe.xml'))
    assert feed.bozo
