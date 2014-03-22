from contextlib import contextmanager
from ..ut.connection import ccontext
from ..db import (
    get_or_add_query_bi_kind_and_text,
    add_one_query_changes,
    set_query_result,
    touch_query_bi_id,
)
from .mod import mod


def sync(kind, text, timeout, **kargs):
    result = mod(kind).spy(text, timeout)
    with context(**kargs) as conn:
        query = get_or_add_query_bi_kind_and_text(conn, kind, text)
        if query.result == result:
            touch_query_bi_id(conn, query.id)
        else:
            add_one_query_changes(
                conn,
                query.id,
                mod(kind).changes(query.result, result)
            )
            set_query_result(conn, query.id, result)


@contextmanager
def context(**kargs):
    if 'conn' in kargs:
        yield kargs['conn']
    elif 'engine' in kargs:
        with ccontext(commit=True, engine=kargs['engine']) as conn:
            yield conn
    else:
        assert False, 'must provide conn or engine'
