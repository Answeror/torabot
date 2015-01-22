from nose.tools import assert_equal
from urllib.parse import urlencode
from . import TestSuite, app


class TestThumbnail(TestSuite):

    def test_thumbnail_proxy(self):
        with app.test_client() as c:
            r = c.get('/thumb?' + urlencode({
                'uri': 'http://i1.pixiv.net/img-inf/img/2014/06/07/00/12/24/43932098_s.jpg',
                'referer': 'http://www.pixiv.net/'
            }))
            assert_equal(r.status_code, 200)
