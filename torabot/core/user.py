from logbook import Logger
from flask import url_for, current_app, render_template
from itsdangerous import URLSafeSerializer
from ..core.connection import autoccontext
from .. import db
from .email import send as send_email


log = Logger(__name__)


def get_user_id_bi_openid(openid):
    with autoccontext(commit=False) as conn:
        return db.get_user_id_bi_openid(conn, openid)


def get_user_name_bi_openid(openid):
    with autoccontext(commit=False) as conn:
        return db.get_user_name_bi_openid(conn, openid)


def check_openid(openid):
    with autoccontext(commit=False) as conn:
        return db.has_user_bi_openid(conn, openid)


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
    conf = current_app.config
    send_email(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
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
        host=conf['TORABOT_EMAIL_HOST'],
        port=conf['TORABOT_EMAIL_PORT'],
    )


def get_activation_link(email_id, next_uri):
    s = get_serializer()
    payload = s.dumps((email_id, next_uri))
    return url_for('.activate_user', payload=payload, _external=True)


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = current_app.secret_key
    return URLSafeSerializer(secret_key)
