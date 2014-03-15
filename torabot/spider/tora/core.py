import requests
from urllib.parse import urlencode, urljoin
import re
from fn.iters import take
from logbook import Logger
from collections import OrderedDict
from bs4 import BeautifulSoup as BS
from datetime import datetime
from time import sleep
from hashlib import md5
from functools import partial
import concurrent.futures
from nose.tools import assert_greater_equal
from ...ut.time import tokyo_to_utc
from ...ut.bunch import Bunch


QUERY_URL = 'http://www.toranoana.jp/cgi-bin/R2/allsearch.cgi'
ROOM = 20
log = Logger(__name__)


class Busy(object):
    pass


busy = Busy()


def make_query_uri(query, start):
    return QUERY_URL + '?' + urlencode(OrderedDict([
        ('item_kind', '0401'),
        ('bl_fg', '0'),
        ('search', query.encode('Shift_JIS')),
        ('ps', start + 1),
    ]))


def fetch_list(query, start, session):
    return fetch(
        make_query_uri(query, start),
        headers={'Referer': QUERY_URL},
        session=session,
    )


def fetch(uri, session, headers={}):
    hd = {'Cookie': 'afg=0'}
    hd.update(headers)
    r = session.get(uri, headers=hd)
    return r.content


def parse_list(soup, text, session):
    total, begin, end = parse_status(soup, text)
    return Bunch(
        total=total,
        begin=begin,
        end=end,
        arts=parse_arts(soup, text, session)
    )


def parse_status(soup, text):
    m = re.search(r'（ (\d+) 件 のうち (\d+) 〜 (\d+) 件表示）', text)
    if not m:
        total, begin, end = 0, 0, 0
    else:
        total, begin, end = [int(m.group(i)) for i in range(1, 4)]
        # start from zero
        begin -= 1
    return total, begin, end


def parse_arts(soup, text, session):
    base = 'http://www.toranoana.jp/'
    trs = soup.select('table.FixFrame tr')
    if len(trs) <= 3:
        return []
    return fill_detail(list(map(lambda tr: Bunch(
        title=str(tr.select('td.c1 a')[0].string),
        author=str(tr.select('td.c2 a')[0].string),
        company=str(tr.select('td.c3 a')[0].string),
        uri=str(urljoin(base, tr.select('td.c1 a')[0]['href'])),
        status='reserve' if '予' in tr.select('td.c7')[0].get_text() else 'other'
    ), trs[2:-1:2])), session)


def get(session, uri):
    return longrun(partial(
        safe,
        partial(fetch, uri),
        parse_detail,
        session,
    ))


def fill_detail(arts, session):
    with concurrent.futures.ThreadPoolExecutor(max_workers=ROOM) as ex:
        for art, d in zip(arts, ex.map(partial(get, session), [art['uri'] for art in arts])):
            art.update(d)
    return arts


def parse_detail(soup, text):
    return Bunch(
        ptime=parse_ptime(soup, text),
        hash=makehash(soup, text),
    )


def safe(fetch, parse, session):
    text = fetch(session=session).decode('Shift_JIS')
    # 100M memory comsume...
    soup = BS(text, 'lxml')
    if check_busy(soup, text):
        return busy
    return parse(soup, text)


def makehash(soup, text):
    tags = soup.select('table[summary="Details"]')
    assert tags
    return md5(tags[0].get_text().encode('utf-8')).hexdigest()


def check_busy(soup, text):
    return '大変混み合っています' in text


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


def first_n_arts_safe(query, n, return_total, session=None):
    try:
        return first_n_arts(query, n, return_total, session)
    except:
        log.exception('guard')
        return [0] if return_total else []


def first_n_arts(query, n, return_total, session=None):
    if session is None:
        session = makesession()
    return list(take(
        n,
        gen_arts(
            query,
            begin=0,
            return_total=return_total,
            session=session
        )
    ))


def makesession():
    session = requests.Session()
    # http://stackoverflow.com/a/18845952/238472
    session.mount(
        'http://',
        requests.adapters.HTTPAdapter(
            pool_connections=ROOM + 1,
            pool_maxsize=ROOM + 1
        )
    )
    return session


def gen_arts(query, begin=0, return_total=False, session=None):
    if session is None:
        session = makesession()

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


def parse_ptime_tokyo(soup, text):
    for td in soup.select('td.DetailData_R'):
        if td.string:
            try:
                return datetime.strptime(td.string.strip(), r'%Y/%m/%d')
            except:
                pass


def parse_ptime(soup, text):
    dt = parse_ptime_tokyo(soup, text)
    return None if dt is None else tokyo_to_utc(dt)
