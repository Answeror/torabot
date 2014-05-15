import re
from functools import partial
from ...ut.bunch import bunchr
from ..query import parse_json, parse_dict, try_parse, try_regular


# http://stackoverflow.com/a/7160778/238472
url_pattern = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)


def parse_posts_uri(query):
    if isinstance(query, str) and url_pattern.match(query.strip()):
        return bunchr(method='posts_uri', uri=query)


def parse_query(query):
    if isinstance(query, str):
        return bunchr(method='query', query=query)


CANDIDATES = [
    parse_dict,
    parse_json,
    parse_posts_uri,
    parse_query,
]


parse = partial(try_parse, candidates=CANDIDATES)
regular = partial(try_regular, candidates=CANDIDATES)


def get_query_text(query):
    return {
        'posts_uri': lambda: query.uri,
        'query': lambda: query.query,
    }[query.method]()
