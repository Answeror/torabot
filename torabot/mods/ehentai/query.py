from functools import partial
from ...ut.bunch import bunchr
from ..query import parse_json, parse_dict, try_parse, try_regular


def parse_uri(query):
    if isinstance(query, str) and query.startswith('http://g.e-hentai.org'):
        return bunchr(method='uri', uri=query)


def parse_query(query):
    if isinstance(query, str):
        return bunchr(method='query', query=query)


CANDIDATES = [
    parse_dict,
    parse_json,
    parse_uri,
    parse_query,
]

parse = partial(try_parse, candidates=CANDIDATES)
regular = partial(try_regular, candidates=CANDIDATES)
