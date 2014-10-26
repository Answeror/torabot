from asyncio import coroutine
from logbook import Logger
from itertools import chain
from flask import current_app
from datetime import timedelta
from itertools import groupby
from ..db import db
from ..ut.bunch import Bunch
from .email import send as send_email
from . import core


log = Logger(__name__)


@core.initializer
def init_app(app):
    app.config.setdefault('TORABOT_RECENT_NOTICE_DAYS', 1)
    app.config.setdefault('TORABOT_DESIRE_RECENT_NOTICE_COUNT', 24)
    app.config.setdefault('TORABOT_NOTICE_ACCUMULATION_LIMIT', 8)
    app.config.setdefault('TORABOT_EMAIL_HEAD', 'torabot notice')


def format_notice_status(notice):
    return {
        'pending': '未发送',
        'sent': '已发送',
    }[notice.status]


def web_transform(notice):
    notice = Bunch(**notice)
    notice.body = core.mod(notice.kind).format_notice_body('web', notice)
    notice.status = format_notice_status(notice)
    return notice


@coroutine
def send_notices_email(target, notices):
    notices = list(notices)
    limit = current_app.config['TORABOT_NOTICE_ACCUMULATION_LIMIT']
    if len(notices) > limit:
        append_bodies = [
            '您有%d条通知, 这里仅列出其中%d条. 更多通知请上torabot查看. '
            '关于为什么只列出了部分通知: '
            'http://%s/faq#faq-notice-accumulation-limit'
            % (len(notices), limit, current_app.config['SERVER_NAME'])
        ]
        notices = notices[:limit]
    else:
        append_bodies = []
    return (yield from core.run_in_executor(
        send_email,
        recipient_addrs=[target],
        subject=current_app.config['TORABOT_EMAIL_HEAD'],
        text='\n\n---\n\n'.join([core.mod(no.kind).format_notice_body('email', no) for no in notices] + append_bodies),
        attachments=list(chain(*[core.mod(no.kind).notice_attachments('email', no) for no in notices]))
    ))


def one_email(notices):
    emails = [no.email for no in notices]
    assert(len(set(emails)) == 1)
    return emails[0]


@core.interface
@db.with_optional_bind
@coroutine
def notice_all(bind):
    with db.connection_context(bind=bind) as conn:
        notices = yield from db.get_pending_notices(conn)

    for user_id in {no.user_id for no in notices}:
        yield from notice_one_user(
            user_id,
            [no for no in notices if no.user_id == user_id],
            bind=bind
        )


@coroutine
def notice_one_user(user_id, notices, bind):
    with db.connection_context(bind=bind) as conn:
        recent = yield from db.count_recent_notice_bi_user_id(
            conn,
            user_id=user_id,
            interval=timedelta(
                days=current_app.config['TORABOT_RECENT_NOTICE_DAYS']
            )
        )

    if need_accumulate(recent) > len(notices):
        log.info(
            '{} need accumulate {} notices, accumulated {}',
            user_id,
            need_accumulate(recent),
            len(notices)
        )
        return

    notices = sorted(notices, key=lambda n: n.email)
    for email, subset in groupby(notices, lambda n: n.email):
        yield from send_notices(
            notices=list(subset),
            bind=bind
        )


def need_accumulate(recent):
    return max(1, round(recent / current_app.config['TORABOT_DESIRE_RECENT_NOTICE_COUNT']))


@coroutine
def send_notices(notices, bind):
    email = one_email(notices)
    log.info(
        'send notices {} to {}',
        [no.id for no in notices],
        email
    )

    try:
        yield from send_notices_email(email, notices)
    except:
        log.exception(
            'send notices {} to {} failed',
            [no.id for no in notices],
            email
        )
        return False

    with db.connection_context(commit=True, bind=bind) as conn:
        for notice in notices:
            yield from db.mark_notice_sent(conn, notice.id)

    return True


def get_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, db.get_notices_bi_user_id(conn, user_id, **kargs)))


def get_pending_notices_bi_user_id(conn, user_id, **kargs):
    return list(map(web_transform, db.get_pending_notices_bi_user_id(conn, user_id, **kargs)))


# if __name__ == '__main__':
    # import json
    # from ..ut.bunch import bunchr
    # from .. import make
    # app = make()
    # conf = app.config
    # notice = bunchr(dict(
        # kind='pixiv',
        # change=dict(
            # kind='user_art.new',
            # art=json.loads('''{
                # "title": "\u3069\u3046\u3057\u3088\u3046\u3082\u306a\u3044\u50d5\u306b\u5929\u4f7f\u304c\u964d\u308a\u3066\u304d\u305f",
                # "uri": "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=42459959",
                # "thumbnail_uri": "http://i2.pixiv.net/img-inf/img/2014/03/25/16/19/01/42459959_s.png",
                # "author": "\u516b\u795e\uff20\uff7b\uff9d\uff78\uff98J21b"
            # }''')
        # )
    # ))
    # send_notices_email(
        # conf,
        # 'answeror@gmail.com',
        # [notice, notice]
    # )
