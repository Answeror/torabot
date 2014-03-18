from nose.tools import assert_equal
from ...ut.bunch import bunchr
from ...mods import tora


class Mod(object):

    def spy(self, query):
        assert_equal(query, '大嘘')
        return bunchr({
            'arts': [
                {
                    'title': '47〜大嘘忠臣蔵',
                    'company': 'GENETRIX',
                    'status': 'reserve',
                    'author': 'GEN',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0020/01/59/040020015900.html'
                },
                {
                    'title': 'ぬえちゃん靴下本[サウナ編]',
                    'company': '嘘つき屋',
                    'status': 'reserve',
                    'author': '大嘘',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
                },
                {
                    'title': 'SketchBook',
                    'company': '嘘つき屋',
                    'status': 'other',
                    'author': '大嘘',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/78/040030147860.html'
                },
                {
                    'title': 'こいしちゃん靴下本',
                    'company': '嘘つき屋',
                    'status': 'other',
                    'author': '大嘘',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/13/51/040030135186.html'
                },
                {
                    'title': '猫の居る生活',
                    'company': '大嘘吐き',
                    'status': 'other',
                    'author': 'サユル',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140055.html'
                },
                {
                    'title': '運命の人',
                    'company': '大嘘吐き',
                    'status': 'other',
                    'author': 'サユル',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140059.html'
                },
                {
                    'title': 'とらのあなオリジナルTシャツ No.046 大嘘',
                    'company': '株式会社虎の穴',
                    'status': 'other',
                    'author': '大嘘',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/09/50/040030095070.html'
                },
                {
                    'title': 'The Grimoire of Alice',
                    'company': 'SideNine',
                    'status': 'other',
                    'author': 'Nine、77gl、大嘘、他',
                    'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/08/48/040030084860.html'
                }
            ]
        })

    def changes(self, old, new):
        return tora.changes(old, new)
