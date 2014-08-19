import json
from functools import partial
from ..ut.bunch import bunchr
from ..core.backends.postgresql import PostgreSQL


def query(kind, text, timeout, make_backend=PostgreSQL, **kargs):
    from ..core.connection import autoccontext
    from ..core.query import query as search
    with autoccontext(commit=True) as conn:
        q = search(
            kind=kind,
            text=text,
            timeout=timeout,
            backend=make_backend(conn=conn),
            **kargs
        )
    return q.result if q else None


def parse_json(query):
    if isinstance(query, str):
        try:
            query = json.loads(query)
            if not isinstance(query, dict):
                raise Exception('not standard')
            return bunchr(query)
        except:
            pass


def parse_dict(query):
    if isinstance(query, dict):
        return bunchr(query)


def illegal(query):
    assert False, 'illegal query: %s' % query


def try_parse(query, candidates):
    for f in candidates:
        ret = f(query)
        if ret is not None:
            return ret
    assert False, 'invalid query: %s' % str(query)


def try_regular(query, candidates):
    return json.dumps(try_parse(query, candidates), sort_keys=True)


def make_parse_and_regular(candidates):
    parse = partial(try_parse, candidates=candidates)
    regular = partial(try_regular, candidates=candidates)
    return parse, regular
