from nose.tools import assert_equal
from httmock import HTTMock, all_requests
from ..spider import fetch_and_parse_all
from . import freeze


@all_requests
def mock(url, req):
    d = freeze.load()
    for key in d:
        print(d[key][0])
    return freeze.load()[freeze.reqmd5(req)][1]


def test_fetch_and_parse_all():
    with HTTMock(mock):
        arts = fetch_and_parse_all('大嘘')
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
