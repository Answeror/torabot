from .mod import mod
from ..db import get_watches_bi_user_id as _get_watches_bi_user_id
from ..ut.bunch import Bunch


def get_watches_bi_user_id(conn, user_id):
    return [transform(w) for w in _get_watches_bi_user_id(conn, user_id)]


def transform(watch):
    watch = Bunch(**watch)
    watch.what = mod(watch.query_kind).format_query_text('web', watch.query_text)
    return watch
