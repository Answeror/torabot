import json
import inspect
from asyncio import coroutine
from functools import partial
from urllib.parse import urlencode
from ...ut.request import request
from ...ut.xml import parse_html
from . import bilibili


@coroutine
def source(query, timeout=None):
    query = bilibili.parse(query)

    return (yield from {
        'sp': source_sp,
        'bangumi': source_bangumi,
        'user': source_user,
        'username': source_username,
        'query': source_query
    }[query['method']](query))


@coroutine
def source_sp(query):
    for sp in (yield from get_bangumi()):
        if sp['title'] == query['title']:
            return {'kind': 'sp', 'sp': sp}
    return {'kind': 'sp', 'sp': None}


@coroutine
def get_bangumi():
    query = yield from bilibili.search('{"method": "bangumi"}')
    return query.result.content


@coroutine
def source_bangumi(query):
    resp = yield from request.get('http://www.bilibili.tv/index/bangumi.json')
    data = yield from resp.read()
    return {
        'query': query,
        'content': json.loads(data.decode('utf-8'))
    }


@coroutine
def _source_user(query, uri):
    resp = yield from request.get(uri)
    data = yield from resp.read()
    return {
        'query': query,
        'user_uri': uri,
        'posts': (yield from (parse_html(data, parse_user)))
    }


@coroutine
def source_user(query):
    return (yield from _source_user(
        query,
        'http://space.bilibili.tv/' + query['user_id']
    ))


def parse_user(root):
    return [
        parse_post(sub) for sub in
        root.xpath('//div[@class="main_list"]/ul/li')
    ]


def parse_post(root):
    return {
        'title': str(root.xpath('string(.//a[@class="title"])')),
        'uri': str(root.xpath('.//a[@class="title"]/@href')[0]),
        'cover': str(root.xpath('.//img/@src')[0]),
        'kind': str(root.xpath('string(.//a[@class="l"])')),
        'ctime': str(root.xpath('string(.//div[@class="c"])'))[5:],
        'desc': str(root.xpath('string(.//div[@class="q"])'))
    }


@coroutine
def source_username(query):
    resp = yield from request.get(make_username_search_uri(query['username']))
    data = yield from resp.read()
    user_uri_or_recommendations = yield from parse_html(
        data,
        partial(parse_username, query)
    )

    if isinstance(user_uri_or_recommendations, str):
        return (yield from _source_user(query, user_uri_or_recommendations))

    return {
        'query': query,
        'posts': [],
        'recommendations': user_uri_or_recommendations
    }


@coroutine
def source_query(query):
    uri = make_query_uri(query['query'])
    resp = yield from request.get(uri)
    data = yield from resp.read()
    return {
        'query': query,
        'uri': uri,
        'posts': (yield from parse_html(data, parse_query))
    }


def parse_query(root):
    return [
        make_search_post(sub) for sub in
        root.xpath('//ul[@class="result"]/li')
    ]


def parse_username(query, root):
    posts = []
    for li in root.xpath('//ul[@class="result"]/li'):
        post = make_search_post(li)
        if query['username'] == post['upper']:
            return post['user_uri']
        posts.append(post)

    return make_recommendations(posts)


def make_recommendations(posts):
    def gen():
        names = {}
        for p in posts:
            r = make_recommendation(p)
            if r['username'] not in names:
                yield r
                names[r['username']] = 1

    return list(gen())


def make_recommendation(post):
    return {
        'user_uri': post['user_uri'],
        'username': post['upper'],
    }


def make_search_post(root):
    post = eval_optional({
        'title': lambda: str(root.xpath('string(.//div[@class="t"])')),
        'upper': str(root.xpath('string(.//a[@class="upper"])')),
        'kind': lambda: str(root.xpath('string(.//div[@class="t"]/span)')),
        'date': str(root.xpath('string(.//i[@class="date"])')).strip(),
        'intro': str(root.xpath('string(.//i[@class="intro"])')),
        'uri': str(root.xpath('.//a/@href')[0]),
        'user_uri': str(root.xpath('.//a[@class="upper"]/@href')[0]),
        'cover': str(root.xpath('.//a[@class="title"]//img/@src')[0])
    })
    if post.get('title') and post['title'].startswith(post.get('kind', '')):
        post['title'] = post['title'][len(post.get('kind', '')):]
    return post


def make_username_search_uri(username):
    return make_query_uri(u'@author %s' % username)


def make_query_uri(query):
    return 'http://www.bilibili.tv/search?' + urlencode({
        'keyword': query.encode('utf-8'),
        'orderby': 'senddate',
    })


def eval_optional(d):
    def gen():
        for key, value in d.items():
            if inspect.isfunction(value):
                value = value()
            yield key, value
    return dict(gen())
