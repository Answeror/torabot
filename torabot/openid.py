from flask.ext.openid import OpenID, COMMON_PROVIDERS
from flask import (
    g,
    session,
    redirect,
    flash,
    request,
    render_template,
    url_for,
    abort
)
from .model import User, Session


def get_userid(openid):
    s = Session()
    try:
        return (
            s.query(User.id)
            .filter_by(openid=openid)
            .scalar()
        )
    except:
        pass
    finally:
        s.close()


def add_user(name, email, openid):
    s = Session()
    try:
        s.add(User(name=name, email=email, openid=openid))
        s.commit()
    except:
        s.rollback()


def make(app):
    oid = OpenID(app, app.instance_path)

    @app.before_request
    def lookup_current_user():
        if 'openid' in session and 'userid' not in session:
            userid = get_userid(session['openid'])
            if userid is not None:
                session['userid'] = userid

    @app.route('/login', methods=['GET', 'POST'])
    @oid.loginhandler
    def login():
        if 'userid' in session:
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
        session['openid'] = resp.identity_url
        userid = get_userid(session['openid'])
        if userid is not None:
            flash('Successfully signed in')
            session['userid'] = userid
            return redirect(oid.get_next_url())
        return redirect(url_for(
            'prof',
            next=oid.get_next_url(),
            name=resp.fullname or resp.nickname,
            email=resp.email
        ))

    @app.route('/prof', methods=['GET', 'POST'])
    def prof():
        if 'userid' in session or 'openid' not in session:
            return redirect(url_for('index'))
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            if not name:
                flash('Error: you have to provide a name')
            elif '@' not in email:
                flash('Error: you have to enter a valid email address')
            else:
                flash('Profile successfully created')
                add_user(name, email, session['openid'])
                return redirect(oid.get_next_url())
        return render_template(
            'prof.html',
            next_url=oid.get_next_url()
        )

    @app.route('/logout')
    def logout():
        session.pop('openid', None)
        session.pop('userid', None)
        flash('You were signed out')
        return redirect(oid.get_next_url())
