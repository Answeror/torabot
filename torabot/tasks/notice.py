from .engine import make as make_engine
from ..ut.connection import ccontext
from ..ut.guard import timeguard
from .. import db
from ..core.notice import send_notice


@timeguard
def notice_all(conf):
    engine = make_engine(conf)

    with ccontext(engine=engine) as conn:
        notices = db.get_pending_notices(conn)

    for notice in notices:
        with ccontext(commit=True, engine=engine) as conn:
            if db.user_activated_bi_id(notice.user_id):
                send_notice(
                    conf=conf,
                    notice=notice,
                    conn=conn,
                )
