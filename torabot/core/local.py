from werkzeug.local import LocalProxy
from flask import g, session, request
from .. import db


def get_current_conf():
    try:
        from flask import current_app
        return current_app.config
    except:
        try:
            from celery import current_app
            return current_app.conf
        except:
            return {}


def get_is_user():
    name = '_is_user'
    value = getattr(g, name, None)
    if value is None:
        from .user import check_openid
        value = 'openid' in session and check_openid(session['openid'])
        setattr(g, name, value)
    return value


is_user = LocalProxy(get_is_user)


def get_is_user_activated():
    name = '_is_user_activated'
    value = getattr(g, name, None)
    if value is None:
        if not is_user:
            value = False
        else:
            from .connection import autoccontext
            with autoccontext() as conn:
                value = db.user_activated_bi_id(conn, current_user_id._get_current_object())
        setattr(g, name, value)
    return value


is_user_activated = LocalProxy(get_is_user_activated)


def get_is_admin():
    name = '_is_admin'
    value = getattr(g, name, None)
    if value is None:
        value = 'openid' in session and check_admin_openid(session['openid'])
        setattr(g, name, value)
    return value


def check_admin_openid(openid):
    from flask import current_app
    return current_user_id._get_current_object() in current_app.config['TORABOT_ADMIN_IDS']


is_admin = LocalProxy(get_is_admin)


def get_current_user():
    name = '_current_user'
    value = getattr(g, name, None)
    if value is None:
        from .user import get_user_detail_bi_openid
        value = get_user_detail_bi_openid(session['openid'])
        setattr(g, name, value)
        if value:
            g.current_user_loaded = True
    return value


current_user = LocalProxy(get_current_user)


def get_current_user_id():
    name = '_current_user_id'
    if hasattr(g, name):
        value = getattr(g, name)
    else:
        if 'openid' not in session:
            value = None
        else:
            if g.get('current_user_loaded', False):
                value = current_user.id
            else:
                from .user import get_user_id_bi_openid
                value = get_user_id_bi_openid(session['openid'])
        setattr(g, name, value)
    return value


current_user_id = LocalProxy(get_current_user_id)


def get_current_username():
    name = '_current_username'
    if hasattr(g, name):
        value = getattr(g, name)
    else:
        if 'openid' not in session:
            value = None
        else:
            if g.get('current_user_loaded', False):
                value = current_user.name
            else:
                from .user import get_user_name_bi_openid
                value = get_user_name_bi_openid(session['openid'])
        setattr(g, name, value)
    return value


current_username = LocalProxy(get_current_username)


def get_request_values():
    name = '_request_values'
    if hasattr(g, name):
        value = getattr(g, name)
    else:
        if request.json:
            value = request.json
        else:
            value = request.values
        setattr(g, name, value)
    return value


request_values = LocalProxy(get_request_values)


def get_intro():
    name = '_intro'
    value = getattr(g, name, None)
    if value is None:
        value = '1' == request.cookies.get('intro', '1')
        setattr(g, name, value)
    return value


intro = LocalProxy(get_intro)
