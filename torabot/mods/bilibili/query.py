import json
from nose.tools import assert_in
from ...core.local import get_current_conf
from ..query import query
from . import name


def get_bangumi():
    return query(
        kind=name,
        text=json.dumps(dict(method='bangumi')),
        timeout=get_current_conf()['TORABOT_SPY_TIMEOUT'],
    ).content


def standard_query(query):
    try:
        d = json.loads(query)
    except:
        d = dict(method='sp', title=query)
        query = json.dumps(d)
    assert_in('method', d)
    return query, d
