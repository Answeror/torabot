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
    abort
)
from ...db import add_user
from ...ut.session import makeappsession as makesession
from . import bp
from logbook import Logger
from ...core.local import is_user


oid = OpenID()
log = Logger(__name__)


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
                add_user(
                    session.connection(),
                    name=name,
                    email=email,
                    openid=flask_session['openid'],
                )
            return redirect(oid.get_next_url())
    return render_template(
        'prof.html',
        next_url=oid.get_next_url()
    )


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_session.pop('openid', None)
    flash('You were signed out')
    return redirect(oid.get_next_url())
