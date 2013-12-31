from nose.tools import assert_equal
from httmock import HTTMock
from ..spider import list_all, ptime
from .mock import mockrequests
from datetime import datetime
from ..time import tokyo_to_utc
from mock import patch


def test_list_all():
    with HTTMock(mockrequests):
        arts = list(list_all('大嘘'))

    assert_equal(arts, [
        {
            'title': '47〜大嘘忠臣蔵',
            'comp': 'GENETRIX',
            'reserve': True,
            'timestamp': '3db64c747b73b2bf9db8c1a5337e7f01',
            'author': 'GEN',
            'ptime': datetime(2011, 8, 13, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0020/01/59/040020015900.html'
        },
        {
            'title': 'ぬえちゃん靴下本[サウナ編]',
            'comp': '嘘つき屋',
            'reserve': True,
            'timestamp': '2ef6266e3b51c18b2ab81d4a31993c11',
            'author': '大嘘',
            'ptime': datetime(2013, 12, 29, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
        },
        {
            'title': 'SketchBook',
            'comp': '嘘つき屋',
            'reserve': False,
            'timestamp': 'a4c8bb2d6b2322a81027f8afbc838cb9',
            'author': '大嘘',
            'ptime': datetime(2013, 8, 17, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/78/040030147860.html'
        },
        {
            'title': 'こいしちゃん靴下本',
            'comp': '嘘つき屋',
            'reserve': False,
            'timestamp': 'f1525b9611526cd386d2b955e581cde5',
            'author': '大嘘',
            'ptime': datetime(2013, 8, 11, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/13/51/040030135186.html'
        },
        {
            'title': '猫の居る生活',
            'comp': '大嘘吐き',
            'reserve': False,
            'timestamp': '542c8bfe346f39906a72fc66f78d845d',
            'author': 'サユル',
            'ptime': datetime(2013, 7, 27, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140055.html'
        },
        {
            'title': '運命の人',
            'comp': '大嘘吐き',
            'reserve': False,
            'timestamp': '5e9f4310ff801794f4bc0c205455cca2',
            'author': 'サユル',
            'ptime': datetime(2013, 7, 27, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140059.html'
        },
        {
            'title': 'とらのあなオリジナルTシャツ No.046 大嘘',
            'comp': '株式会社虎の穴',
            'reserve': False,
            'timestamp': 'f8f6d7f41100fbe1e8211f8774eb4997',
            'author': '大嘘',
            'ptime': datetime(2012, 12, 31, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/09/50/040030095070.html'
        },
        {
            'title': 'The Grimoire of Alice',
            'comp': 'SideNine',
            'reserve': False,
            'timestamp': '1bcc75adc3336e48c22cbf9e58f1959c',
            'author': 'Nine、77gl、大嘘、他',
            'ptime': datetime(2012, 12, 29, 15, 0),
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/08/48/040030084860.html'
        }
    ])


def test_ptime():
    with HTTMock(mockrequests):
        assert_equal(
            ptime('http://www.toranoana.jp/mailorder/article/04/0030/16/24/040030162479.html'),
            tokyo_to_utc(datetime(year=2013, month=12, day=31))
        )
