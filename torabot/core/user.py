from ..core.connection import autoccontext
from .. import db


def get_user_id_bi_openid(openid):
    with autoccontext(commit=False) as conn:
        return db.get_user_id_bi_openid(conn, openid)


def get_user_name_bi_openid(openid):
    with autoccontext(commit=False) as conn:
        return db.get_user_name_bi_openid(conn, openid)


def check_openid(openid):
    with autoccontext(commit=False) as conn:
        return db.has_user_bi_openid(conn, openid)
