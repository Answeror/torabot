from ..db import (
    get_or_add_query_bi_kind_and_text,
    add_one_query_changes,
    set_query_result,
)
from .mod import mod


def sync(conn, kind, text):
    query = get_or_add_query_bi_kind_and_text(conn, kind, text)
    result = mod(kind).spy(text)
    add_one_query_changes(
        conn,
        query.id,
        mod(kind).changes(query.result, result)
    )
    set_query_result(conn, query.id, result)
