import re
import json
from flask import current_app
from asyncio import coroutine, gather
from logbook import Logger
from collections import OrderedDict
from urllib.parse import urljoin, urlencode
from functools import partial
from flask import render_template
from ...ut.bunch import bunchr
from ...ut.kanji import translate_recursive
from ...ut.xml import parse_html
from ...ut.request import request
from ...ut.return_list import return_list
from ...core.mod import (
    Mod,
    ViewMixin,
    field_guess_name_mixin,
    GuessNameFromQueryText
)


CODING = 'Shift_JIS'
BASE_URL = 'http://www.toranoana.jp/'
QUERY_URL = BASE_URL + 'cgi-bin/R2/allsearch.cgi'
COMPLEX_QUERY_URL = BASE_URL + 'cgi-bin/R2/d_search.cgi'
MAX_ARTS = 8

log = Logger(__name__)


class Tora(
    ViewMixin,
    field_guess_name_mixin('nam', 'act', 'com', 'itc'),
    GuessNameFromQueryText,
    Mod
):

    name = 'tora'
    display_name = '虎穴'
    description = '订阅虎穴查询, 新货上架或可预约时第一时间收到邮件通知, 用来抢本子.'
    normal_search_prompt = '关键字或商品链接'
    has_normal_search = True
    has_advanced_search = True
    no_empty_query = False

    def init_app(self, app):
        super().init_app(app)

        app.config.setdefault('TORABOT_MOD_TORA_TRANSLATE', True)
        app.config.setdefault('TORABOT_MOD_TORA_RETRIES', 3)

    @coroutine
    @return_list
    def changes(self, old, new):
        oldmap = {art.uri: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            if art.uri not in oldmap:
                yield bunchr(kind='new', art=art)
            elif (oldmap[art.uri].status, art.status) in self.noticeable():
                yield bunchr(kind='notice', art=art)

    def noticeable(self):
        return [
            (None, 'reserve'),
            ('other', 'reserve'),
        ]

    @coroutine
    def source(self, query, timeout):
        if query.startswith(BASE_URL):
            return (yield from source_art(query, timeout))
        return (yield from source_list(query, timeout))

    @coroutine
    def regular(self, query):
        return self.name, query

    def format_change_kind(self, kind):
        return {
            'new': '已上架',
            'notice': '可预定',
        }[kind]

    def web_format_notice_body(self, notice):
        return "<a href='%s'>%s</a> %s" % (
            notice.change.art.uri,
            notice.change.art.title,
            self.format_change_kind(notice.change.kind),
        )

    def web_format_notice_status(self, notice):
        return {
            'pending': '未发送',
            'sent': '已发送',
        }[notice.status]

    def web_format_query_text(self, text):
        return text

    def web_format_query_result(self, query):
        return render_template('tora/list.html', query=query)

    def web_format_advanced_search(self, **kargs):
        return render_template('tora/advanced_search.html', kind=self.name)

    def web_format_help_page(self):
        return render_template('tora/help.html')

    def format_notice_body(self, notice):
        return '%(title)s %(change)s: %(uri)s' % dict(
            title=notice.change.art.title,
            change=self.format_change_kind(notice.change.kind),
            uri=notice.change.art.uri,
        )


def translate(query):
    if current_app.config['TORABOT_MOD_TORA_TRANSLATE']:
        return json.dumps(
            translate_recursive(json.loads(query)),
            sort_keys=True
        )
    return query


@coroutine
def source_art(uri, timeout):
    data, _ = yield from get(
        uri,
        cookies={'afg': '0'},
        headers={'Referer': QUERY_URL},
        timeout=timeout
    )
    art = yield from parse_html(data, partial(parse_art, uri))
    if art:
        return bunchr(
            query=uri,
            uri=uri,
            total=1,
            arts=[art]
        )


@coroutine
def get(*args, **kargs):
    for epoch in range(current_app.config['TORABOT_MOD_TORA_RETRIES']):
        resp = yield from request.get(*args, **kargs)
        data = yield from resp.read()
        content = data.decode(CODING)
        if not busy(content):
            return data, content
    else:
        log.debug('Tora request {} failed', args[0] if args else kargs['uri'])


def parse_art(uri, root):
    try:
        return bunchr(
            title=str(root.xpath('string(//td[@class="td_title_bar_r1c2"])')),
            author=str(root.xpath('string(//td[@class="DetailData_L"]/a[contains(@href, "author")])')),
            company=str(root.xpath('string(//td[@class="CircleName"]/a[1])')),
            uri=uri,
            status=status_in_art(root),
        )
    except:
        pass


def status_in_art(root):
    try:
        return (
            'reserve' if '予' in root.xpath(
                '//form[@action="/cgi-bin/R4/details.cgi"]'
                '/input[@type="submit"]/@value'
            )[0] else 'other'
        )
    except:
        return 'other'


@coroutine
def source_list(query, timeout):
    try:
        d = json.loads(query)
        if not isinstance(d, dict):
            log.warn('Not standard tora query: {}', query)
            return
        simple = False
    except:
        simple = True

    if simple:
        uri = make_simple_uri(query, 0)
        return (yield from source_simple_list(query, uri, timeout))

    uri = make_complex_uri(d, 0)
    return (yield from source_complex_list(query, uri, timeout))


def make_simple_uri(query, start):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode(CODING)),
        ('ps', start + 1),
    ]))


def make_complex_uri(query, start):
    return COMPLEX_QUERY_URL + '?' + urlencode(OrderedDict(
        (key, str(value).encode(CODING)) for key, value in query.items()
    ))


@coroutine
def source_simple_list(query, uri, timeout):
    data, content = yield from get(
        uri,
        cookies={'afg': '0'},
        headers={'Referer': QUERY_URL},
        timeout=timeout
    )
    if empty(content):
        return bunchr(
            query=query,
            uri=uri,
            total=0,
            arts=[]
        )
    return (yield from parse_html(data, partial(parse_simple_list, query, uri)))


def parse_simple_list(query, uri, root):
    try:
        trs = list(root.xpath('//table[@class="FixFrame"]//tr'))
        return bunchr(
            query=query,
            uri=uri,
            total=int(re.search(r'\d+', root.xpath(
                'string(//table[@class="addrtbl"]'
                '//td[@class="DTW_td_l"]/span[2])'
            )).group(0)),
            arts=[
                bunchr(
                    title=str(tr.xpath('stirng(td[@class="c1"]/a)')),
                    author=str(tr.xpath('string(td[@class="c2"]/a)')),
                    company=str(tr.xpath('string(td[@class="c3"]/a)')),
                    uri=urljoin(BASE_URL, str(tr.xpath('td[@class="c1"]/a/@href')[0])),
                    status='reserve' if u'予' in tr.xpath('string(td[@class="c7"])') else 'other',
                ) for tr in trs[2:-1:2][:MAX_ARTS]
            ]
        )
    except:
        pass


@coroutine
def source_complex_list(query, uri, timeout):
    data, content = yield from get(
        uri,
        cookies={'afg': '0'},
        headers={'Referer': COMPLEX_QUERY_URL},
        timeout=timeout
    )
    if empty(content):
        return bunchr(
            query=query,
            uri=uri,
            total=0,
            arts=[]
        )
    return (yield from parse_html(
        data,
        partial(parse_complex_list, query, timeout, uri)
    ))


def parse_complex_list(query, uri, timeout, root):
    try:
        pages = current_app.loop.run_until_complete((yield from gather(
            [
                source_simple_list(query, urljoin(BASE_URL, url), timeout)
                for url in root.xpath(
                    '//tr[@class="TBLdtil"]/td[@class="noi_c2"]/a/@href'
                )[:MAX_ARTS]
            ],
            loop=current_app.loop
        )))
        return bunchr(
            query=query,
            uri=uri,
            total=int(re.search(r'\d+', root.xpath(
                'string(//table[@class="f_tbl_9cf"]/tr/td/span[2])'
            )).group(0)),
            arts=[page['arts'][0] for page in pages]
        )
    except:
        pass


def empty(content):
    for s in [
        '該当する商品が見つかりませんでした。',
        '同時に指定できる検索キーワードは最大３件までです。',
        '検索キーワードを入れて下さい。',
        'での検索はできません。キーワードの変更をお願いします。',
    ]:
        if s in content:
            return True
    return False


def busy(content):
    return '大変混み合っています' in content


tora = Tora()


__all__ = ['Tora', 'tora']
