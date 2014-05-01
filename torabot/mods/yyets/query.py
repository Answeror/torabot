import json
from ...ut.bunch import bunchr


def parse(query):
    if isinstance(query, str):
        return bunchr(method='rss', uri=query)
    return query


def regular(query):
    return json.dumps(parse(query), sort_keys=True)
