from werkzeug.local import LocalProxy
from flask import g, session, current_app


def get_current_conf():
    try:
        return current_app.config
    except:
        try:
            from celery import current_app
            return current_app.conf
        except:
            return {}


def get_is_user():
    from .user import check_openid
    name = '_is_user'
    value = getattr(g, name, None)
    if value is None:
        value = 'openid' in session and check_openid(session['openid'])
        setattr(g, name, value)
    return value


is_user = LocalProxy(get_is_user)


def get_is_admin():
    name = '_is_admin'
    value = getattr(g, name, None)
    if value is None:
        value = 'openid' in session and check_admin_openid(session['openid'])
        setattr(g, name, value)
    return value


def check_admin_openid(openid):
    from .user import get_user_id_bi_openid
    user_id = get_user_id_bi_openid(openid)
    return user_id in current_app.config['TORABOT_ADMIN_IDS']


is_admin = LocalProxy(get_is_admin)
