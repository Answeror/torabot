import os
from nose.tools import assert_equal
from ...ut.bunch import Bunch
from ..email import pack, guess_extension


def test_pack():
    assert pack(
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


def test_guess_extension():
    assert_equal(guess_extension('image/png'), '.png')
    assert_equal(guess_extension('image/jpeg'), '.jpeg')
