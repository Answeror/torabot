from requests import Session
from urllib.parse import urlencode, urljoin
import re
from logbook import Logger
from collections import OrderedDict
from bs4 import BeautifulSoup as BS
from datetime import datetime
from time import sleep
from hashlib import md5
from functools import partial
import concurrent.futures
from nose.tools import assert_greater_equal
from fn.iters import take, drop, head
from ..ut.time import tokyo_to_utc
from ..ut.memo import memo, gemo


ROOM = 20
log = Logger(__name__)


class Busy(object):
    pass


busy = Busy()


def fetch_list(query, start, session=Session()):
    base = 'http://www.toranoana.jp/cgi-bin/R2/allsearch.cgi'
    return fetch(
        base + '?' + urlencode(OrderedDict([
            ('item_kind', '0401'),
            ('bl_fg', '0'),
            ('search', query.encode('Shift_JIS')),
            ('ps', start + 1),
        ])),
        headers={'Referer': base},
        session=session,
    )


def fetch(uri, headers={}, session=Session()):
    hd = {'Cookie': 'afg=0'}
    hd.update(headers)
    r = session.get(uri, headers=hd)
    return r.content


def parse_list(soup, session):
    total, begin, end = parse_stats(soup)
    return {
        'total': total,
        'begin': begin,
        'end': end,
        'arts': parse_arts(soup, session)
    }


def parse_stats(soup):
    m = re.search(r'（ (\d+) 件 のうち (\d+) 〜 (\d+) 件表示）', soup.get_text())
    if not m:
        total, begin, end = 0, 0, 0
    else:
        total, begin, end = [int(m.group(i)) for i in range(1, 4)]
        # start from zero
        begin -= 1
    return total, begin, end


def parse_arts(soup, session):
    base = 'http://www.toranoana.jp/'
    trs = soup.select('table.FixFrame tr')
    if len(trs) <= 3:
        return []
    return fill_detail(list(map(lambda tr: {
        'title': tr.select('td.c1 a')[0].string,
        'author': tr.select('td.c2 a')[0].string,
        'company': tr.select('td.c3 a')[0].string,
        'uri': urljoin(base, tr.select('td.c1 a')[0]['href']),
        'reserve': '予' in tr.select('td.c7')[0].get_text(),
    }, trs[2:-1:2])), session)


def fill_detail(arts, session):
    get = lambda art: longrun(partial(
        safe,
        partial(fetch, art['uri']),
        parse_detail,
        session,
    ))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for art, d in zip(arts, ex.map(get, arts)):
            art.update(d)
    return arts


def parse_detail(soup):
    return {
        'ptime': parse_ptime(soup),
        'hash': makehash(soup),
    }


def safe(fetch, parse, session=Session()):
    soup = BS(fetch(session=session), 'html5lib')
    if check_busy(soup):
        return busy
    return parse(soup)


def makehash(soup):
    tags = soup.select('table[summary="Details"]')
    assert tags
    return md5(tags[0].get_text().encode('utf-8')).hexdigest()


def check_busy(soup):
    return re.search(r'大変混み合っています', soup.get_text()) is not None


def longrun(f):
    seconds = 1

    def check_too_long():
        if seconds >= 60:
            raise Exception('too long busy wait')

    while True:
        try:
            d = f()
            if d == busy:
                check_too_long()
                log.debug('longrun busy, sleep {} seconds', seconds)
                sleep(seconds)
                seconds += seconds
            else:
                return d
        except:
            log.exception('longrun exception')
            check_too_long()
            log.debug('longrun exception, sleep {} seconds', seconds)
            sleep(seconds)
            seconds += seconds


def list_one_safe(query, start, session):
    return longrun(partial(
        safe,
        partial(fetch_list, query, start),
        partial(parse_list, session=session),
        session,
    ))


def gen_arts(query, begin=0, return_total=False, session=Session()):
    assert_greater_equal(begin, 0)
    d = list_one_safe(query, begin, session)
    total = d['total']
    if return_total:
        yield total
    yield from d['arts']
    while d['end'] < d['total']:
        log.debug('fetch start from {}', d['end'])
        d = list_one_safe(query, d['end'], session)
        if d['total'] != total:
            raise Exception(
                'total arts changed: {} -> {}'.format(d['total'], total)
            )
        yield from d['arts']


def total(query, session=Session()):
    return list_one_safe(query, 0, session)['total']


def parse_ptime_tokyo(soup):
    for td in soup.select('td.DetailData_R'):
        if td.string:
            try:
                return datetime.strptime(td.string.strip(), r'%Y/%m/%d')
            except:
                pass


def parse_ptime(soup):
    dt = parse_ptime_tokyo(soup)
    return None if dt is None else tokyo_to_utc(dt)


def ptime(uri, session=Session()):
    return longrun(partial(safe, partial(fetch, uri), parse_ptime, session))


class Spider(object):

    def __init__(self):
        self.session = Session()

    def art_n(self, query, n):
        return head(drop(n, self.gen_arts_from_head(query, n + 1)))

    def gen_arts_from_head(self, query, n, return_total=False):
        yield from take(n, gen_arts(
            query,
            begin=0,
            return_total=return_total,
            session=self.session,
        ))


class FrozenSpider(object):

    def __init__(self, base=Spider()):
        self.base = base
        self._art_n = memo(base.art_n)
        self._gen_arts_from_head = gemo(base.gen_arts_from_head)

    def art_n(self, query, n):
        return self._art_n(query, n)

    def gen_arts_from_head(self, query, n, return_total=None):
        yield from self._gen_arts_from_head(
            query,
            n,
            **({} if return_total is None else {'return_total': return_total})
        )
