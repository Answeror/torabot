from logbook import Logger
from itertools import chain
from .. import db
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


def send_notices_email(conf, target, notices):
    notices = list(notices)
    limit = conf['TORABOT_NOTICE_ACCUMULATION_LIMIT']
    if len(notices) > limit:
        append_bodies = [
            '您有%d条通知, 这里仅列出其中%d条. 更多通知请上torabot查看. '
            '关于为什么只列出了部分通知: http://torabot.com/faq#faq-notice-accumulation-limit'
            % (len(notices), limit)
        ]
        notices = notices[:limit]
    send_email(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
        [target],
        conf['TORABOT_EMAIL_HEAD'],
        '\n\n---\n\n'.join([mod(no.kind).format_notice_body('email', no) for no in notices] + append_bodies),
        list(chain(*[mod(no.kind).notice_attachments('email', no) for no in notices])),
        host=conf['TORABOT_EMAIL_HOST'],
        port=conf['TORABOT_EMAIL_PORT'],
    )


def one_email(notices):
    emails = [no.email for no in notices]
    assert(len(set(emails)) == 1)
    return emails[0]


def send_notices(notices, conf, conn):
    email = one_email(notices)
    log.info(
        'send notices {} to {}',
        [no.id for no in notices],
        email
    )
    try:
        send_notices_email(conf, email, notices)
    except:
        log.exception(
            'send notices {} to {} failed',
            [no.id for no in notices],
            email
        )
        return False

    for notice in notices:
        db.mark_notice_sent(conn, notice.id)
    return True


def send_notice(notice, conf, conn):
    assert notice.email
    log.info('send notice {} to {}', notice.id, notice.email)
    try:
        send_notice_email(conf, notice.email, notice)
    except:
        log.exception('send notice {} to {} failed', notice.id, notice.email)
        return False

    db.mark_notice_sent(conn, notice.id)
    return True


def get_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, db.get_notices_bi_user_id(conn, user_id, **kargs)))


def get_pending_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, db.get_pending_notices_bi_user_id(conn, user_id, **kargs)))


if __name__ == '__main__':
    import json
    from ..ut.bunch import bunchr
    from .. import make
    app = make()
    conf = app.config
    notice = bunchr(dict(
        kind='pixiv',
        change=dict(
            kind='user_art.new',
            art=json.loads('''{
                "title": "\u3069\u3046\u3057\u3088\u3046\u3082\u306a\u3044\u50d5\u306b\u5929\u4f7f\u304c\u964d\u308a\u3066\u304d\u305f",
                "uri": "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=42459959",
                "thumbnail_uri": "http://i2.pixiv.net/img-inf/img/2014/03/25/16/19/01/42459959_s.png",
                "author": "\u516b\u795e\uff20\uff7b\uff9d\uff78\uff98J21b"
            }''')
        )
    ))
    send_notices_email(
        conf,
        'answeror@gmail.com',
        [notice, notice]
    )
