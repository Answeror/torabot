from nose.tools import assert_equal
from fn.iters import take, head, drop
from datetime import datetime


class UsotukiyaSpider(object):

    def gen_arts_from_head(self, query, n, return_total=False):
        assert_equal(query, '大嘘')
        arts = [
            {
                'title': '47〜大嘘忠臣蔵',
                'company': 'GENETRIX',
                'status': 'reserve',
                'hash': '3db64c747b73b2bf9db8c1a5337e7f01',
                'author': 'GEN',
                'ptime': datetime(2011, 8, 13, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0020/01/59/040020015900.html'
            },
            {
                'title': 'ぬえちゃん靴下本[サウナ編]',
                'company': '嘘つき屋',
                'status': 'reserve',
                'hash': '2ef6266e3b51c18b2ab81d4a31993c11',
                'author': '大嘘',
                'ptime': datetime(2013, 12, 29, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
            },
            {
                'title': 'SketchBook',
                'company': '嘘つき屋',
                'status': 'other',
                'hash': 'a4c8bb2d6b2322a81027f8afbc838cb9',
                'author': '大嘘',
                'ptime': datetime(2013, 8, 17, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/78/040030147860.html'
            },
            {
                'title': 'こいしちゃん靴下本',
                'company': '嘘つき屋',
                'status': 'other',
                'hash': 'f1525b9611526cd386d2b955e581cde5',
                'author': '大嘘',
                'ptime': datetime(2013, 8, 11, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/13/51/040030135186.html'
            },
            {
                'title': '猫の居る生活',
                'company': '大嘘吐き',
                'status': 'other',
                'hash': '542c8bfe346f39906a72fc66f78d845d',
                'author': 'サユル',
                'ptime': datetime(2013, 7, 27, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140055.html'
            },
            {
                'title': '運命の人',
                'company': '大嘘吐き',
                'status': 'other',
                'hash': '5e9f4310ff801794f4bc0c205455cca2',
                'author': 'サユル',
                'ptime': datetime(2013, 7, 27, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/14/00/040030140059.html'
            },
            {
                'title': 'とらのあなオリジナルTシャツ No.046 大嘘',
                'company': '株式会社虎の穴',
                'status': 'other',
                'hash': 'f8f6d7f41100fbe1e8211f8774eb4997',
                'author': '大嘘',
                'ptime': datetime(2012, 12, 31, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/09/50/040030095070.html'
            },
            {
                'title': 'The Grimoire of Alice',
                'company': 'SideNine',
                'status': 'other',
                'hash': '1bcc75adc3336e48c22cbf9e58f1959c',
                'author': 'Nine、77gl、大嘘、他',
                'ptime': datetime(2012, 12, 29, 15, 0),
                'uri': 'http://www.toranoana.jp/mailorder/article/04/0030/08/48/040030084860.html'
            }
        ]
        if return_total:
            yield len(arts)
        yield from take(n, arts)

    def art_n(self, query, n):
        return head(drop(n, self.gen_arts_from_head(query, n + 1)))
