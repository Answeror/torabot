import requests
from bs4 import BeautifulSoup as BS
import json


def gen(soup):
    for tr in soup.select('tr'):
        tds = tr.select('td.tdR4')
        if len(tds) == 6:
            yield tds[2].string, tds[3].string


uri = 'http://www.kishugiken.co.jp/cn/code10d.html'
soup = BS(requests.get(uri).content, 'html5lib')

d = {}
for hanzi, kanji in gen(soup):
    a = d.get(hanzi, [])
    a.append(kanji)
    d[hanzi] = a

print(json.dumps(d, indent=4))
