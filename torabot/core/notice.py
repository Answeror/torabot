from logbook import Logger
from ..db import (
    get_user_email_bi_id,
    mark_notice_sent,
    get_notices_bi_user_id as _get_notices_bi_user_id,
    get_pending_notices_bi_user_id as _get_pending_notices_bi_user_id
)
from .email import send_notice as send
from ..core.mod import mod
from ..ut.bunch import Bunch


log = Logger(__name__)


def views(notice):
    return mod(notice.kind).views


def web_transform(notice):
    notice = Bunch(**notice)
    notice.body = views(notice).web.format_notice_body(notice)
    notice.status = views(notice).web.format_notice_status(notice)
    return notice


def send_notice(notice, conf, conn):
    email = get_user_email_bi_id(conn, notice.user_id)
    log.info('send notice {} to {}', notice.id, email)
    try:
        send(conf, email, views(notice).email.format_notice_body(notice))
    except:
        log.exception('send notice {} to {} failed', notice.id, email)
        return

    mark_notice_sent(conn, notice.id)


def get_notices_bi_user_id(conn, user_id):
    return list(map(web_transform, _get_notices_bi_user_id(conn, user_id)))


def get_pending_notices_bi_user_id(conn, user_id):
    return list(map(web_transform, _get_pending_notices_bi_user_id(conn, user_id)))
