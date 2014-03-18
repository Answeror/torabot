from .mod import mod
from ..db import get_watches_bi_user_id as _get_watches_bi_user_id


def get_watches_bi_user_id(conn, user_id):
    return [transform(w) for w in _get_watches_bi_user_id(conn, user_id)]


def transform(watch):
    return mod(watch.query_text).views.web.format_query_text(watch.query_text)
