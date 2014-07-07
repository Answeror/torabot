from logbook import Logger
from ..core.local import get_current_conf
from ..core.connection import autoccontext
from .. import db
from datetime import timedelta, datetime


log = Logger(__name__)


def del_inactive_queries():
    conf = get_current_conf()
    with autoccontext(commit=True) as conn:
        before = db.get_query_count(conn)
        db.del_inactive_queries(
            conn,
            before=datetime.utcnow() - timedelta(days=conf['TORABOT_DELETE_INACTIVE_QUERIES_BEFORE_DAYS']),
            limit=conf['TORABOT_DELETE_INACTIVE_QUERIES_LIMIT']
        )
        after = db.get_query_count(conn)
        log.info('delete inactive queries, from {} to {}, deleted {}', before, after, before - after)
        return before - after


def del_old_changes():
    conf = get_current_conf()
    with autoccontext(commit=True) as conn:
        before = db.get_change_count(conn)
        db.del_old_changes(
            conn,
            before=datetime.utcnow() - timedelta(days=conf['TORABOT_DELETE_OLD_CHANGES_BEFORE_DAYS']),
            limit=conf['TORABOT_DELETE_OLD_CHANGES_LIMIT']
        )
        after = db.get_change_count(conn)
        log.info('delete old changes, from {} to {}, deleted {}', before, after, before - after)
        return before - after
