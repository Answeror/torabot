import json
from nose.tools import assert_greater
from ... import make


def test_mods():
    app = make()
    with app.test_client() as c:
        resp = c.get('/api/mods')
        data = json.loads(resp.data.decode('ascii'))
        assert_greater(len(data['result']), 0)
