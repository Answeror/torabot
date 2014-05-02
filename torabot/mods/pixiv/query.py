import re
import json
from ...ut.bunch import bunchr
from ..query import parse_json, parse_dict, illegal


BASE_URL = 'http://www.pixiv.net/'
USER_URL = 'http://www.pixiv.net/member.php'
RANKING_URL = 'http://www.pixiv.net/ranking.php'
USER_ILLUSTRATIONS_URL = 'http://www.pixiv.net/member_illust.php'


def loads(query):
    try:
        return bunchr(json.loads(query))
    except:
        illegal(query)


def parse_user_uri(query):
    if isinstance(query, str) and query.startswith(USER_URL):
        return bunchr(method='user_uri', uri=query)


def parse_user_illustrations_uri(query):
    if isinstance(query, str) and query.startswith(USER_ILLUSTRATIONS_URL):
        return bunchr(method='user_illustrations_uri', uri=query)


def parse_ranking_uri(query):
    if isinstance(query, str) and query.startswith(RANKING_URL):
        return bunchr(method='ranking', uri=query)


def parse_user_id(query):
    if isinstance(query, str) and re.match(r'^\d+$', query):
        return bunchr(method='user_id', user_id=query)


def patch(query):
    '''impure'''
    if 'method' not in query:
        if 'user_id' in query:
            query.method = 'user_id'
        elif 'user_uri' in query:
            query.method = 'user_uri'
            query.uri = query.user_uri
            del query['user_uri']
        else:
            illegal(query)


def parse_username(query):
    if isinstance(query, str):
        return bunchr(method='username', username=query)


def parse(query):
    for f in [
        parse_dict,
        parse_user_uri,
        parse_user_illustrations_uri,
        parse_ranking_uri,
        parse_user_id,
        parse_json,
        parse_username,
    ]:
        ret = f(query)
        if ret is not None:
            patch(ret)
            return ret

    illegal(query)


def regular(query):
    return json.dumps(parse(query), sort_keys=True)
