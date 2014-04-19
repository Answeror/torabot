import json
from ...ut.bunch import bunchr


BASE_URL = 'http://www.pixiv.net/'
USER_URL = 'http://www.pixiv.net/member.php'
RANKING_URL = 'http://www.pixiv.net/ranking.php'
USER_ILLUSTRATIONS_URL = 'http://www.pixiv.net/member_illust.php'


def illegal(query):
    assert False, 'illegal query: %s' % query


def loads(query):
    try:
        return bunchr(json.loads(query))
    except:
        illegal(query)


def parse(query):
    if isinstance(query, str):
        if query.startswith(USER_URL):
            query = bunchr(method='user_uri', uri=query)
        elif query.startswith(USER_ILLUSTRATIONS_URL):
            query = bunchr(method='user_illustrations_uri', uri=query)
        elif query.startswith(RANKING_URL):
            query = bunchr(method='ranking', uri=query)
        else:
            query = loads(query)

    assert isinstance(query, dict), 'unknown query type: %s' % str(type(query))

    if 'method' not in query:
        if 'user_id' in query:
            query['method'] = 'user_id'
        elif 'user_uri' in query:
            query['method'] = 'user_uri'
        else:
            illegal(query)
    return query


def regular(query):
    return json.dumps(parse(query), sort_keys=True)
