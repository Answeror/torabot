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


from urllib.parse import urlparse, urlunparse, ParseResult, urlencode
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
from itsdangerous import BadSignature
from ... import db
from ...ut.session import makeappsession as makesession
from . import bp
from logbook import Logger
from ...core.local import is_user
from ...core.connection import autoccontext
from ...core.user import send_activation_email, get_serializer, check_openid


oid = OpenID()
log = Logger(__name__)


@bp.route('/activate/<payload>')
def activate_user(payload):
    s = get_serializer()
    try:
        email_id, next_uri = s.loads(payload)
    except BadSignature:
        abort(404)

    with autoccontext(commit=True) as conn:
        db.activate_email_bi_id(conn, email_id)

    return redirect(next_uri)


@bp.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if is_user:
        return redirect(get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            domain = current_app.config.get('TORABOT_DOMAIN', '')
            if domain:
                request.host_url = 'http://%s/' % domain
                request.base_url = 'http://%s/login' % domain
            return oid.try_login(
                openid,
                ask_for=['email', 'fullname', 'nickname']
            )
    abort(404)


def netloc(uri):
    return urlparse(uri).netloc


def replace_netloc(uri, netloc):
    parts = list(urlparse(uri))
    parts[1] = netloc
    return urlunparse(parts)


def get_next_url():
    uri = oid.get_next_url()
    if next_netloc() != netloc(request.host_url):
        query = dict(next=uri)
        if 'openid' in flask_session:
            query['openid'] = flask_session['openid']
        uri = urlunparse(ParseResult(
            scheme=urlparse(uri).scheme,
            netloc=netloc(uri),
            path=url_for('.next'),
            params='',
            query=urlencode(query),
            fragment=''
        ))
    return uri


def next_netloc():
    return netloc(oid.get_next_url())


@bp.route('/next')
def next():
    openid = request.values.get('openid', '')
    log.info('got next with openid: {}', openid)
    flask_session['openid'] = openid
    return redirect(get_next_url())


@oid.after_login
def create_or_login(resp):
    log.info('create or login, next netloc: {}', next_netloc())

    flask_session['openid'] = resp.identity_url

    if check_openid(resp.identity_url):
        return redirect(get_next_url())

    parts = list(urlparse(url_for(
        '.prof',
        next=oid.get_next_url(),
        name=resp.fullname or resp.nickname,
        email=resp.email,
        openid=resp.identity_url,
        _external=True
    )))
    parts[1] = next_netloc()
    return redirect(urlunparse(parts))


@bp.route('/prof', methods=['GET', 'POST'])
def prof():
    if is_user or 'openid' not in request.values:
        return redirect(url_for("main.index"))

    flask_session['openid'] = request.values['openid']

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
                user = db.get_user_detail_bi_id(session.connection(), user_id)
            send_activation_email(
                email_id=user.emails[0].id,
                email_text=email,
                username=name,
                next_uri=get_next_url()
            )
            return render_template(
                'message.html',
                ok=True,
                message='账户激活邮件已发送至 %s , 请根据邮件中的提示完成注册.' % email
            )
    return render_template(
        'prof.html',
        next_url=get_next_url()
    )


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_session.pop('openid', None)
    flash('You were signed out')
    return redirect(get_next_url())
