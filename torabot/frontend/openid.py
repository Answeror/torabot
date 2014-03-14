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
from ..db import get_user_id_bi_openid, add_user
from ..ut.session import makeappsession as makesession
from . import bp


oid = OpenID()


def get_userid(openid):
    with makesession() as session:
        return get_user_id_bi_openid(session.connection(), openid)


@bp.before_request
def lookup_current_user():
    if 'openid' in flask_session and 'userid' not in flask_session:
        userid = get_userid(flask_session['openid'])
        if userid is not None:
            flask_session['userid'] = userid


@bp.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if 'userid' in flask_session:
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
    flask_session['openid'] = resp.identity_url
    userid = get_userid(flask_session['openid'])
    if userid is not None:
        flash('Successfully signed in')
        flask_session['userid'] = userid
        return redirect(oid.get_next_url())
    return redirect(url_for(
        '.prof',
        next=oid.get_next_url(),
        name=resp.fullname or resp.nickname,
        email=resp.email
    ))


@bp.route('/prof', methods=['GET', 'POST'])
def prof():
    if 'userid' in flask_session or 'openid' not in flask_session:
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


@bp.route('/logout', methods=['POST'])
def logout():
    flask_session.pop('openid', None)
    flask_session.pop('userid', None)
    flash('You were signed out')
    return redirect(oid.get_next_url())
