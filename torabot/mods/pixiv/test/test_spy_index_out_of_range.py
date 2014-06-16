import json
from nose.tools import assert_greater
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name


@need_scrapyd
def test_spy_list_index_out_of_range():
    app = make()
    with app.app_context():
        d = mod(name).spy(
            json.dumps(dict(
                method='user_id',
                user_id='55320'
            )), 60
        )
        assert_greater(len(d.arts), 0)
