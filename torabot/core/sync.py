from ..db import (
    get_or_add_query_bi_kind_and_text,
    add_one_query_changes,
    set_query_result,
    touch_query_bi_id,
)
from .mod import mod


def sync(conn, kind, text, timeout):
    query = get_or_add_query_bi_kind_and_text(conn, kind, text)
    result = mod(kind).spy(text, timeout)
    if query.result == result:
        touch_query_bi_id(conn, query.id)
    else:
        add_one_query_changes(
            conn,
            query.id,
            mod(kind).changes(query.result, result)
        )
        set_query_result(conn, query.id, result)
