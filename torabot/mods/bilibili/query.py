import json
from ...ut.bunch import bunchr
from ...core.local import get_current_conf
from ..query import query, parse_json, parse_dict, make_parse_and_regular
from . import name


def get_bangumi():
    return query(
        kind=name,
        text=json.dumps(dict(method='bangumi')),
        timeout=get_current_conf()['TORABOT_SPY_TIMEOUT'],
    ).content


def parse_title(query):
    if isinstance(query, str):
        return bunchr(method='sp', title=query)


parse, regular = make_parse_and_regular([
    parse_dict,
    parse_json,
    parse_title,
])
