from nose.tools import assert_equal
from httmock import HTTMock
from ..spider import list_all, fetch_ptime
from .mock import mockrequests
from datetime import datetime
from ..time import tokyo_to_utc
from mock import patch


def test_list_all():
    with HTTMock(mockrequests):
        arts = list(list_all('大嘘'))

    for art in arts:
        del art['ptime']
        del art['timestamp']

    assert_equal(arts, [
        {
            'author': 'GEN',
            'comp': 'GENETRIX',
            'reserve': True,
            'title': '47〜大嘘忠臣蔵',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0020/01/59/040020015900.html'
        },
        {
            'author': '大嘘',
            'comp': '嘘つき屋',
            'reserve': True,
            'title': 'ぬえちゃん靴下本[サウナ編]',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
        },
        {
            'author': '大嘘',
            'comp': '嘘つき屋',
            'reserve': False,
            'title': 'SketchBook',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/78/040030147860.html'
        },
        {
            'author': '大嘘',
            'comp': '嘘つき屋',
            'reserve': False,
            'title': 'こいしちゃん靴下本',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/13/51/040030135186.html'
        },
        {
            'author': 'サユル',
            'comp': '大嘘吐き',
            'reserve': False,
            'title': '猫の居る生活',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140055.html'
        },
        {
            'author': 'サユル',
            'comp': '大嘘吐き',
            'reserve': False,
            'title': '運命の人',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140059.html'
        },
        {
            'author': '大嘘',
            'comp': '株式会社虎の穴',
            'reserve': False,
            'title': 'とらのあなオリジナルTシャツ No.046 大嘘',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/09/50/040030095070.html'
        },
        {
            'author': 'Nine、77gl、大嘘、他',
            'comp': 'SideNine',
            'reserve': False,
            'title': 'The Grimoire of Alice',
            'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/08/48/040030084860.html'
        }
    ])


def test_fetch_ptime():
    with HTTMock(mockrequests):
        ptime = fetch_ptime('http://www.toranoana.jp/mailorder/article/04/0030/16/24/040030162479.html')

    assert_equal(ptime, tokyo_to_utc(datetime(year=2013, month=12, day=31)))


#def test_fetch_and_parse_all_future():
    #with patch('torabot.spider.utcnow') as now:
        #now.return_value = tokyo_to_utc(datetime(year=2013, month=12, day=31))
        #with HTTMock(mockrequests):
            #arts = list(fetch_and_parse_all_future('a'))
        #now.assert_called_with()

    #assert_equal(len(arts), 94)
