from logbook import Logger
from ..db import (
    get_user_email_bi_id,
    mark_notice_sent,
    get_notices_bi_user_id as _get_notices_bi_user_id,
    get_pending_notices_bi_user_id as _get_pending_notices_bi_user_id
)
from .email import send_notice as send
from .render import render_notice


log = Logger(__name__)


def send_notice(notice, conf, conn):
    notice = render_notice(notice)
    email = get_user_email_bi_id(conn, notice.user_id)
    log.info('send notice {} to {}', notice.id, email)
    try:
        send(conf, email, notice.email_body)
    except:
        log.exception('send notice {} to {} failed', notice.id, email)
        return

    mark_notice_sent(conn, notice.id)


def get_notices_bi_user_id(conn, user_id):
    return list(map(render_notice, _get_notices_bi_user_id(conn, user_id)))


def get_pending_notices_bi_user_id(conn, user_id):
    return list(map(render_notice, _get_pending_notices_bi_user_id(conn, user_id)))
