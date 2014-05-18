from ..core.email import send as send_email
from ..core.local import get_current_conf
from ..core.connection import autoccontext
from ..ut.guard import exguard
from .. import db


def get_admin_email():
    with autoccontext() as conn:
        return db.get_user_detail_bi_id(
            conn,
            get_current_conf()['TORABOT_ADMIN_IDS'][0]
        ).email


def tell_admin(text, head='tell admin', attachments=[]):
    conf = get_current_conf()
    send_email(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
        [get_admin_email()],
        head,
        text,
        attachments,
        host=conf['TORABOT_EMAIL_HOST'],
        port=conf['TORABOT_EMAIL_PORT'],
    )


def tell_admin_safe(*args, **kargs):
    return exguard(tell_admin)(*args, **kargs)
