from werkzeug.local import LocalProxy
from flask import g, session, request
from .. import db
from ..ut.local import local


def get_current_conf():
    return local.conf


def get_is_user():
    name = '_is_user'
    value = getattr(g, name, None)
    if value is None:
        value = 'user_id' in session
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
        value = 'user_id' in session and check_admin_id(session['user_id'])
        setattr(g, name, value)
    return value


def check_admin_id(id):
    return id in local.conf['TORABOT_ADMIN_IDS']


is_admin = LocalProxy(get_is_admin)


def get_current_user():
    name = '_current_user'
    value = getattr(g, name, None)
    if value is None:
        from .user import get_user_detail_bi_id
        value = get_user_detail_bi_id(session['user_id'])
        setattr(g, name, value)
        if value:
            g.current_user_loaded = True
    return value


current_user = LocalProxy(get_current_user)


def get_current_user_id():
    none = object()
    value = getattr(g, '_current_user_id', none)
    if value is none:
        g._current_user_id = value = session.get('user_id')
    return value


current_user_id = LocalProxy(get_current_user_id)


def get_current_username():
    none = object()
    value = getattr(g, '_current_username', none)
    if value is none:
        if 'user_id' not in session:
            value = None
        else:
            if g.get('current_user_loaded', False):
                value = current_user.name
            else:
                from .user import get_user_name_bi_id
                value = get_user_name_bi_id(session['user_id'])
        g._current_username = value
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
