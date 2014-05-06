import openid.oidutil


# patch for lxml
# ValueError: Unicode strings with encoding declaration are not supported.
# Please use bytes input or XML fragments without declaration.
openid.oidutil.elementtree_modules = [
    'xml.etree.cElementTree',
    'xml.etree.ElementTree',
    'cElementTree',
    'elementtree.ElementTree',
]


from flask.ext.openid import OpenID
from flask import (
    session as flask_session,
    redirect,
    flash,
    request,
    render_template,
    url_for,
    abort,
    current_app
)
from itsdangerous import URLSafeSerializer, BadSignature
from ... import db
from ...ut.session import makeappsession as makesession
from . import bp
from logbook import Logger
from ...core.local import is_user
from ...core.email import send as send_email
from ...core.connection import autoccontext


oid = OpenID()
log = Logger(__name__)


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = current_app.secret_key
    return URLSafeSerializer(secret_key)


@bp.route('/activate/<payload>')
def activate_user(payload):
    s = get_serializer()
    try:
        user_id, next_uri = s.loads(payload)
    except BadSignature:
        abort(404)

    with autoccontext(commit=True) as conn:
        db.activate_user_bi_id(conn, user_id)

    return redirect(next_uri)


def get_activation_link(user_id, next_uri):
    s = get_serializer()
    payload = s.dumps((user_id, next_uri))
    return url_for('.activate_user', payload=payload, _external=True)


@bp.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if is_user:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(
                openid,
                ask_for=['email', 'fullname', 'nickname']
            )
    abort(404)


@oid.after_login
def create_or_login(resp):
    if is_user:
        return redirect(oid.get_next_url())
    flask_session['openid'] = resp.identity_url
    return redirect(url_for(
        '.prof',
        next=oid.get_next_url(),
        name=resp.fullname or resp.nickname,
        email=resp.email
    ))


def send_activation_email(user_id, user_name, user_email, next_uri):
    conf = current_app.config
    send_email(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
        [user_email],
        'Torabot用户邮件验证',
        render_template(
            'activation_email.txt',
            name=user_name,
            email=user_email,
            site=url_for('main.index', _external=True),
            activation_uri=get_activation_link(user_id, next_uri),
        ),
        [],
        host=conf['TORABOT_EMAIL_HOST'],
        port=conf['TORABOT_EMAIL_PORT'],
    )


@bp.route('/prof', methods=['GET', 'POST'])
def prof():
    if is_user or 'openid' not in flask_session:
        return redirect(url_for('.index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash('Error: you have to provide a name')
        elif '@' not in email:
            flash('Error: you have to enter a valid email address')
        else:
            flash('Profile successfully created')
            with makesession(commit=True) as session:
                user_id = db.add_user(
                    session.connection(),
                    name=name,
                    email=email,
                    openid=flask_session['openid'],
                )
            send_activation_email(user_id, name, email, oid.get_next_url())
            return render_template(
                'message.html',
                ok=True,
                message='账户激活邮件已发送至 %s , 请根据邮件中的提示完成注册.' % email
            )
    return render_template(
        'prof.html',
        next_url=oid.get_next_url()
    )


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_session.pop('openid', None)
    flash('You were signed out')
    return redirect(oid.get_next_url())
