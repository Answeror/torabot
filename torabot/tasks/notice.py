from datetime import timedelta
from logbook import Logger
from itertools import groupby
from .engine import make as make_engine
from ..ut.connection import ccontext
from ..ut.guard import timeguard
from .. import db
from ..core.notice import send_notices


log = Logger(__name__)


@timeguard
def notice_all(conf):
    engine = make_engine(conf)

    with ccontext(engine=engine) as conn:
        notices = db.get_pending_notices(conn)

    for user_id in {no.user_id for no in notices}:
        notice_one_user(
            user_id,
            [no for no in notices if no.user_id == user_id],
            engine,
            conf,
        )


def notice_one_user(user_id, notices, engine, conf):
    with ccontext(engine=engine) as conn:
        recent = db.count_recent_notice_bi_user_id(
            conn,
            user_id=user_id,
            interval=timedelta(days=1)
        )

    if need_accumulate(recent, conf) > len(notices):
        log.info(
            '{} need accumulate {} notices, accumulated {}',
            user_id,
            need_accumulate(recent, conf),
            len(notices)
        )
        return

    with ccontext(commit=True, engine=engine) as conn:
        notices = sorted(notices, key=lambda n: n.email)
        for email, subset in groupby(notices, lambda n: n.email):
            send_notices(
                conf=conf,
                notices=list(subset),
                conn=conn,
            )


def need_accumulate(recent, conf):
    return max(1, round(recent / conf['TORABOT_DESIRE_RECENT_NOTICE_COUNT']))
