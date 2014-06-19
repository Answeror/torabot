import os
from .. import empty


CURRENT_PATH = os.path.dirname(__file__)


def test_empty_result():
    '''CLASSIC MILK+PEACE and ALIEN'''
    for name in [
        'classic-milk-peace-and-alien.html',
    ]:
        yield check_empty_result, name


def check_empty_result(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        content = f.read().decode('Shift_JIS')
    assert empty(content)
