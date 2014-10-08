from logbook import Logger
from flask import url_for, render_template
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature,
)
from passlib.apps import custom_app_context as pwd_context
from ..ut.bunch import Bunch
from .. import db
from .. import celery
from .connection import autoccontext
from .email import send as send_email
from ..ut.local import local
from .errors import DuplicateUsernameError, DuplicateEmailError


log = Logger(__name__)


class User(Bunch):

    @property
    def has_not_activated_email(self):
        return bool([e for e in self.emails if not e.activated])


def get_user_name_bi_id(id):
    with autoccontext(commit=False) as conn:
        return db.get_user_name_bi_id(conn, id)


def get_user_detail_bi_id(id):
    with autoccontext(commit=False) as conn:
        ret = db.get_user_detail_bi_id(conn, id)
        return None if ret is None else User(ret)


def activate_email(id):
    with autoccontext(commit=False) as conn:
        user = db.get_user_detail_bi_email_id(conn, id)

    send_activation_email(
        email_id=id,
        email_text=[e for e in user.emails if e.id == id][0].text,
        username=user.name,
        next_uri=url_for("main.index")
    )


def update_email(user_id, email_id, email, label):
    '''return email changed'''
    with autoccontext(commit=True) as conn:
        orig = db.get_email_bi_id(conn, email_id).text
        db.update_email_bi_id(conn, id=email_id, email=email, label=label)
        if email != orig:
            log.info('user {} email change: {} -> {}', user_id, orig, email)
            db.inactivate_email_bi_id(conn, email_id)
        username = db.get_user_name_bi_id(conn, user_id)

    if email != orig:
        send_activation_email(
            email_id=email_id,
            email_text=email,
            username=username,
            next_uri=url_for("main.index")
        )

    return email != orig


def add_email(user_id, email, label):
    with autoccontext(commit=True) as conn:
        email_id = db.add_email_bi_user_id(
            conn,
            email=email,
            label=label,
            id=user_id,
        )
        db.inactivate_email_bi_id(conn, email_id)
        username = db.get_user_name_bi_id(conn, user_id)

    send_activation_email(
        email_id=email_id,
        email_text=email,
        username=username,
        next_uri=url_for("main.index")
    )


def send_activation_email(email_id, email_text, username, next_uri):
    send_email(
        local.conf['TORABOT_EMAIL_USERNAME'],
        local.conf['TORABOT_EMAIL_PASSWORD'],
        [email_text],
        'Torabot用户邮件验证',
        render_template(
            'activation_email.txt',
            name=username,
            email=email_text,
            site=url_for('main.index', _external=True),
            activation_uri=get_activation_link(email_id, next_uri),
        ),
        [],
        host=local.conf['TORABOT_EMAIL_HOST'],
        port=local.conf['TORABOT_EMAIL_PORT'],
    )


def send_password_reset_email(email):
    send_email(
        local.conf['TORABOT_EMAIL_USERNAME'],
        local.conf['TORABOT_EMAIL_PASSWORD'],
        [email],
        'Torabot密码重置',
        render_template(
            'password_reset_email.txt',
            email=email,
            site=url_for('main.index', _external=True),
            activation_uri=get_password_reset_link(email),
        ),
        [],
        host=local.conf['TORABOT_EMAIL_HOST'],
        port=local.conf['TORABOT_EMAIL_PORT'],
    )


def get_activation_link(email_id, next_uri):
    s = get_serializer(expires_in=local.conf['TORABOT_ACTIVATION_LINK_LIFE'])
    payload = s.dumps((email_id, next_uri))
    return url_for('.activate_user', payload=payload, _external=True)


def get_password_reset_link(email):
    s = get_serializer(expires_in=local.conf['TORABOT_PASSWORD_RESET_LINK_LIFE'])
    payload = s.dumps(email)
    return url_for('.reset_password', payload=payload, _external=True)


def get_password_reset_email(payload):
    s = get_serializer()
    try:
        return s.loads(payload)
    except (BadSignature, SignatureExpired):
        pass


def activate_user_and_get_next_uri(payload):
    s = get_serializer()
    try:
        email_id, next_uri = s.loads(payload)
    except (BadSignature, SignatureExpired):
        return

    with autoccontext(commit=True) as conn:
        db.activate_email_bi_id(conn, email_id)

    return next_uri


def get_serializer(**kargs):
    return Serializer(local.secret_key, **kargs)


def add_user(name, email, password, next_uri):
    try:
        with autoccontext(commit=True) as conn:
            user_id = db.add_user(
                conn,
                name=name,
                email=email,
                password_hash=pwd_context.encrypt(password),
            )
            user = db.get_user_detail_bi_id(conn, user_id)
            send_activation_email(
                email_id=user.emails[0].id,
                email_text=email,
                username=name,
                next_uri=next_uri
            )
    except db.UniqueConstraintError as e:
        if 'Key (name)' in str(e):
            raise DuplicateUsernameError from e
        elif 'Key (email)' in str(e):
            raise DuplicateEmailError from e
        raise

    if local.conf.get('TORABOT_TELL_ADMIN_NEW_USER'):
        celery.tell_admin_safe.delay(text=render_template('user.txt', user=user))

    return user


def set_password_bi_email(email, password):
    with autoccontext(commit=True) as conn:
        db.set_password_hash_bi_email(
            conn,
            email,
            pwd_context.encrypt(password)
        )


def verity_password_bi_email(email, password):
    with autoccontext(commit=False) as conn:
        password_hash = db.get_password_hash_bi_email(conn, email)
        return password_hash and pwd_context.verify(password, password_hash)


def get_user_id_bi_email(email):
    with autoccontext(commit=False) as conn:
        return db.get_user_id_bi_email(conn, email)


def has_email(email):
    with autoccontext(commit=False) as conn:
        return db.has_email(conn, email)
