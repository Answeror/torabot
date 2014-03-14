from .engine import make as make_engine
from ..ut.session import makesession
from ..db import get_pending_notices
from ..core.notice import send_notice


def notice_all(conf):
    engine = make_engine(conf)

    with makesession(engine=engine) as session:
        for notice in get_pending_notices(session.connection()):
            send_notice(
                conf=conf,
                notice=notice,
                conn=session.connection(),
            )
            session.commit()
