import os
from nose.tools import assert_in
from ...ut.bunch import Bunch
from ..email import pack


def test_pack():
    s = pack(
        'sender',
        ['answeror@gmail.com'],
        'head',
        'body',
        [Bunch(
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'nerv.png'),
            mime='image/png',
            name='例大祭11カット'
        )],
    ).as_string()
    assert_in('.png', s)
