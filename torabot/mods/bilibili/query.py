from ...ut.bunch import bunchr
from ..query import parse_json, parse_dict, make_parse_and_regular


def parse_title(query):
    if isinstance(query, str):
        return bunchr(method='sp', title=query)


parse, regular = make_parse_and_regular([
    parse_dict,
    parse_json,
    parse_title,
])
