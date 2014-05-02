import json
from ...ut.bunch import bunchr


def parse_json(query):
    if isinstance(query, str):
        try:
            query = json.loads(query)
            if not isinstance(query, dict):
                raise Exception('not standard')
            return query
        except:
            pass


def parse_rss_uri(query):
    if isinstance(query, str) and query.startswith('http://www.yyets.com/rss'):
        return bunchr(method='rss', uri=query)


def parse_dict(query):
    if isinstance(query, dict):
        return query


def parse(query):
    for f in [
        parse_dict,
        parse_rss_uri,
        parse_json,
    ]:
        ret = f(query)
        if ret is not None:
            return ret
    assert False, 'invalid query: %s' % str(query)


def regular(query):
    return json.dumps(parse(query), sort_keys=True)
