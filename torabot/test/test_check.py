from nose.tools import assert_equal
from ..check import check_new, check_reserve


arts = [
    {
        'author': 'GEN',
        'comp': 'GENETRIX',
        'reserve': False,
        'title': '47〜大嘘忠臣蔵',
        'uri': 'http://www.toranoana.jp/mailorder/article/04/0020/01/59/040020015900.html'
    },
    {
        'author': '大嘘',
        'comp': '嘘つき屋',
        'reserve': False,
        'title': 'ぬえちゃん靴下本[サウナ編]',
        'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
    },
    {
        'author': '大嘘',
        'comp': '嘘つき屋',
        'reserve': False,
        'title': 'SketchBook',
        'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/78/040030147860.html'
    }
]


def reserveone(art):
    from copy import copy
    art = copy(art)
    art.update({'reserve': True})
    return art


def reserve(arts, indices):
    return [reserveone(art) if i in indices else art for i, art in enumerate(arts)]


def _test_check_new(old, new, ret):
    assert_equal(check_new(old, new), ret)


def test_check_new():
    for i in range(len(arts)):
        yield _test_check_new, arts[i + 1:], arts, arts[:i + 1]


def _test_check_reserve(old, new, ret):
    assert_equal(check_reserve(old, new), ret)


def test_check_reserve():
    for i in range(len(arts)):
        reserved = reserve(arts, range(i + 1))
        yield _test_check_reserve, arts, reserved, reserved[:i + 1]
    for i in range(len(arts)):
        reserved = reserve(arts, range(i + 1))
        yield _test_check_reserve, [], reserved, reserved
