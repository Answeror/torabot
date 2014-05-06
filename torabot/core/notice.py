from logbook import Logger
from ..db import (
    get_user_email_bi_id,
    mark_notice_sent,
    get_notices_bi_user_id as _get_notices_bi_user_id,
    get_pending_notices_bi_user_id as _get_pending_notices_bi_user_id
)
from .email import send as send_email
from ..core.mod import mod
from ..ut.bunch import Bunch


log = Logger(__name__)


def format_notice_status(notice):
    return {
        'pending': '未发送',
        'sent': '已发送',
    }[notice.status]


def web_transform(notice):
    notice = Bunch(**notice)
    notice.body = mod(notice.kind).format_notice_body('web', notice)
    notice.status = format_notice_status(notice)
    return notice


def send_notice_email(conf, target, notice):
    send_email(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
        [target],
        conf['TORABOT_EMAIL_HEAD'],
        mod(notice.kind).format_notice_body('email', notice),
        mod(notice.kind).notice_attachments('email', notice),
        host=conf['TORABOT_EMAIL_HOST'],
        port=conf['TORABOT_EMAIL_PORT'],
    )


def send_notice(notice, conf, conn):
    email = get_user_email_bi_id(conn, notice.user_id)
    log.info('send notice {} to {}', notice.id, email)
    try:
        send_notice_email(conf, email, notice)
    except:
        log.exception('send notice {} to {} failed', notice.id, email)
        return

    mark_notice_sent(conn, notice.id)


def get_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, _get_notices_bi_user_id(conn, user_id, **kargs)))


def get_pending_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, _get_pending_notices_bi_user_id(conn, user_id, **kargs)))


if __name__ == '__main__':
    import json
    from ..ut.bunch import bunchr
    from .. import make
    app = make()
    conf = app.config
    send_notice_email(
        conf,
        'answeror@gmail.com',
        bunchr(dict(
            kind='pixiv',
            change=dict(
                art=json.loads('''{
                    "title": "\u3069\u3046\u3057\u3088\u3046\u3082\u306a\u3044\u50d5\u306b\u5929\u4f7f\u304c\u964d\u308a\u3066\u304d\u305f",
                    "uri": "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=42459959",
                    "thumbnail_uri": "http://i2.pixiv.net/img-inf/img/2014/03/25/16/19/01/42459959_s.png",
                    "author": "\u516b\u795e\uff20\uff7b\uff9d\uff78\uff98J21b"
                }''')
            )
        ))
    )
