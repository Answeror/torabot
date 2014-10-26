from asyncio import coroutine
from flask import current_app
from ..ut.exception_guard import exception_guard
from ..celery import celery
from ..db import db
from .email import send as send_email
from . import core


@coroutine
@db.with_optional_connection
def get_admin_email(conn):
    return db.get_user_detail_bi_id(
        conn,
        current_app.config['TORABOT_ADMIN_IDS'][0]
    ).email


@coroutine
def tell_admin(text, head='tell admin', attachments=[]):
    yield from core.run_in_executor(
        send_email,
        recipient_addrs=[get_admin_email()],
        subject=head,
        text=text,
        attachments=attachments
    )


@celery.async_task
def tell_admin_safe(*args, **kargs):
    return exception_guard(tell_admin)(*args, **kargs)
