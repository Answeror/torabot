import os
from .. import busy


CURRENT_PATH = os.path.dirname(__file__)


def test_busy():
    for name in [
        'busy.html',
    ]:
        yield busy, name


def check_busy(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        content = f.read().decode('Shift_JIS')
    assert busy(content)
