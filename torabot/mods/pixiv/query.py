import json


BASE_URL = 'http://www.pixiv.net/'
USER_URL = 'http://www.pixiv.net/member.php'
RANKING_URL = 'http://www.pixiv.net/ranking.php'
USER_ILLUSTRATIONS_URL = 'http://www.pixiv.net/member_illust.php'


def illegal(query):
    assert False, 'illegal query: %s' % query


def loads(query):
    try:
        return json.loads(query)
    except:
        illegal(query)


def parse(query):
    if query.startswith(USER_URL):
        return dict(method='user_uri', uri=query)
    if query.startswith(USER_ILLUSTRATIONS_URL):
        return dict(method='user_illustrations_uri', uri=query)
    if query.startswith(RANKING_URL):
        return dict(method='ranking', uri=query)
    query = loads(query)
    if 'method' not in query:
        if 'user_id' in query:
            query['method'] = 'user_id'
        else:
            illegal(query)
    return query


def regular(query):
    return json.dumps(parse(query), sort_keys=True)
