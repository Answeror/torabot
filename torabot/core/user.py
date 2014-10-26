from asyncio import coroutine, async
from logbook import Logger
from flask import render_template, current_app, url_for
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature,
)
from passlib.apps import custom_app_context as pwd_context
from ..ut.bunch import Bunch
from ..db import db
from .email import send as send_email
from .admin import tell_admin_safe
from . import core


log = Logger(__name__)


@core.setattr
class DuplicateUsernameError(core.CoreError):
    pass


@core.setattr
class DuplicateEmailError(core.CoreError):
    pass


class User(Bunch):

    @property
    def has_not_activated_email(self):
        return bool([e for e in self.emails if not e.activated])


@core.initializer
def init_app(app):
    app.config.setdefault('TORABOT_ACTIVATION_LINK_LIFE', 3600)
    app.config.setdefault('TORABOT_PASSWORD_RESET_LINK_LIFE', 3600)


@db.with_optional_connection
@coroutine
def get_user_name_bi_id(conn):
    return (yield from db.get_user_name_bi_id(conn, id))


@db.with_optional_connection
@coroutine
def get_user_detail_bi_id(id, conn):
    ret = yield from db.get_user_detail_bi_id(conn, id)
    return None if ret is None else User(ret)


@db.with_optional_bind
@coroutine
def activate_email(id, bind):
    with db.connection_context(bind=bind) as conn:
        user = yield from db.get_user_detail_bi_email_id(conn, id)

    yield from send_activation_email(
        email_id=id,
        email_text=[e for e in user.emails if e.id == id][0].text,
        username=user.name,
        next_uri=core.index_uri
    )


@db.with_optional_connection(commit=True)
@coroutine
def update_email(user_id, email_id, email, label, conn):
    '''return email changed'''
    orig = yield from db.get_email_bi_id(conn, email_id).text
    yield from db.update_email_bi_id(conn, id=email_id, email=email, label=label)
    if email != orig:
        log.info('user {} email change: {} -> {}', user_id, orig, email)
        yield from db.inactivate_email_bi_id(conn, email_id)
    username = yield from db.get_user_name_bi_id(conn, user_id)

    if email != orig:
        yield from send_activation_email(
            email_id=email_id,
            email_text=email,
            username=username,
            next_uri=core.index_uri
        )

    return email != orig


@db.with_optional_connection(commit=True)
@coroutine
def add_email(user_id, email, label, conn):
    email_id = yield from db.add_email_bi_user_id(
        conn,
        email=email,
        label=label,
        id=user_id,
    )
    yield from db.inactivate_email_bi_id(conn, email_id)
    username = yield from db.get_user_name_bi_id(conn, user_id)

    yield from send_activation_email(
        email_id=email_id,
        email_text=email,
        username=username,
        next_uri=core.index_uri
    )


@coroutine
def send_activation_email(email_id, email_text, username, next_uri):
    return (yield from core.run_in_executor(
        send_email,
        recipient_addrs=[email_text],
        subject='Torabot用户邮件验证',
        text=render_template(
            'core/activation_email.txt',
            name=username,
            email=email_text,
            site=core.index_uri,
            activation_uri=get_activation_link(email_id, next_uri),
        )
    ))


@coroutine
def send_password_reset_email(email):
    return (yield from core.run_in_executor(
        send_email,
        recipient_addrs=[email],
        subject='Torabot密码重置',
        text=render_template(
            'core/password_reset_email.txt',
            email=email,
            site=core.index_uri,
            activation_uri=get_password_reset_link(email),
        )
    ))


def get_activation_link(email_id, next_uri):
    s = get_serializer(
        expires_in=current_app.config['TORABOT_ACTIVATION_LINK_LIFE']
    )
    payload = s.dumps((email_id, next_uri))
    try:
        return url_for('.activate_user', payload=payload, _external=True)
    except:
        return 'http://{}{}'.format(
            current_app.config['SERVER_NAME'],
            core.activate_user_path % {'payload': payload}
        )


def get_password_reset_link(email):
    s = get_serializer(
        expires_in=current_app.config['TORABOT_PASSWORD_RESET_LINK_LIFE']
    )
    payload = s.dumps(email)
    try:
        return url_for('.reset_password', payload=payload, _external=True)
    except:
        return 'http://{}{}'.format(
            current_app.config['SERVER_NAME'],
            core.reset_password_path % {'payload': payload}
        )


def get_password_reset_email(payload):
    s = get_serializer()
    try:
        return s.loads(payload)
    except (BadSignature, SignatureExpired):
        pass


@db.with_optional_connection
@coroutine
def activate_user_and_get_next_uri(payload, conn):
    s = get_serializer()
    try:
        email_id, next_uri = s.loads(payload)
    except (BadSignature, SignatureExpired):
        return

    yield from db.activate_email_bi_id(conn, email_id)
    return next_uri


def get_serializer(**kargs):
    return Serializer(current_app.secret_key, **kargs)


@core.interface
@db.with_optional_connection(commit=True)
@coroutine
def add_user(name, email, password, conn, next_uri=None):
    if next_uri is None:
        next_uri = core.index_uri

    try:
        user_id = yield from db.add_user(
            conn,
            name=name,
            email=email,
            password_hash=pwd_context.encrypt(password),
        )
        user = yield from db.get_user_detail_bi_id(conn, user_id)
        yield from send_activation_email(
            email_id=user.emails[0].id,
            email_text=email,
            username=name,
            next_uri=next_uri
        )
    except db.UniqueConstraintError as e:
        if 'Key (name)' in str(e):
            raise core.DuplicateUsernameError from e
        elif 'Key (email)' in str(e):
            raise core.DuplicateEmailError from e
        raise

    if current_app.config['TORABOT_TELL_ADMIN_NEW_USER']:
        async(
            tell_admin_safe(text=render_template('core/user.txt', user=user)),
            loop=current_app.loop
        )

    return user


@db.with_optional_connection(commit=True)
@coroutine
def set_password_bi_email(email, password, conn):
    yield from db.set_password_hash_bi_email(
        conn,
        email,
        pwd_context.encrypt(password)
    )


@db.with_optional_connection
@coroutine
def verity_password_bi_email(email, password, conn):
    password_hash = yield from db.get_password_hash_bi_email(conn, email)
    return password_hash and pwd_context.verify(password, password_hash)


@db.with_optional_connection
@coroutine
def get_user_id_bi_email(email, conn):
    return (yield from db.get_user_id_bi_email(conn, email))


@db.with_optional_connection
@coroutine
def has_email(email, conn):
    return (yield from db.has_email(conn, email))
