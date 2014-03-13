from nose.tools import assert_equal
import re


def order_uri_from_toraid(id):
    assert_equal(len(id), 12)
    base = 'http://www.toranoana.jp/mailorder/article/%s/%s/%s/%s/%s.html'
    return base % (id[:2], id[2:6], id[6:8], id[8:10], id)


def toraid_from_order_uri(uri):
    m = re.search(r'.*/(\d{12})\.html', uri)
    return None if m is None else m.group(1)
