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


def web_transform(notice):
    notice = Bunch(**notice)
    notice.body = mod(notice.kind).format_notice_body('web', notice)
    notice.status = mod(notice.kind).format_notice_status('web', notice)
    return notice


def send_notice(notice, conf, conn):
    email = get_user_email_bi_id(conn, notice.user_id)
    log.info('send notice {} to {}', notice.id, email)
    try:
        send(conf, email, mod(notice.kind).format_notice_body('email', notice))
    except:
        log.exception('send notice {} to {} failed', notice.id, email)
        return

    mark_notice_sent(conn, notice.id)


def get_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, _get_notices_bi_user_id(conn, user_id, **kargs)))


def get_pending_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, _get_pending_notices_bi_user_id(conn, user_id, **kargs)))
