from ..db import (
    get_query_bi_kind_and_text,
    has_query_bi_kind_and_text,
)
from .sync import sync


def from_remote(conn, kind, text):
    return get_query_bi_kind_and_text(conn, kind, text)


def query(conn, kind, text, timeout):
    if not has_query_bi_kind_and_text(conn, kind, text):
        sync(kind, text, timeout, conn=conn)
    return get_query_bi_kind_and_text(conn, kind, text)
