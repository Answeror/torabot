from functools import partial
from ...ut.bunch import bunchr
from ..query import parse_json, parse_dict, try_parse, try_regular


def parse_posts_uri(query):
    if isinstance(query, str) and query.startswith('https://yande.re/post'):
        return bunchr(method='posts_uri', uri=query)


CANDIDATES = [
    parse_dict,
    parse_posts_uri,
    parse_json,
]


parse = partial(try_parse, candidates=CANDIDATES)
regular = partial(try_regular, candidates=CANDIDATES)
