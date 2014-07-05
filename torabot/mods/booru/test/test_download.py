from nose.tools import assert_equal
from ..views.email import download, stringify
from .... import make


def test_download():
    app = make()
    with app.app_context():
        r = download('https://yuno.yande.re/data/preview/d0/94/d094d41d27b75027c48986f1294b3f3a.jpg', 'https://yande.re/')
        assert_equal(stringify(r.headers['Content-Type']), 'image/jpeg')
        assert_equal(r.status, 200)
