from ..ut.local import local
from ..ut.email import send as send_email
from ..core.connection import autoccontext
from ..ut.guard import exguard
from .. import db


def get_admin_email():
    with autoccontext() as conn:
        return db.get_user_detail_bi_id(
            conn,
            local.conf['TORABOT_ADMIN_IDS'][0]
        ).email


def tell_admin(text, head='tell admin', attachments=[]):
    send_email(
        recipient_addrs=[get_admin_email()],
        subject=head,
        text=text,
        attachments=attachments
    )


def tell_admin_safe(*args, **kargs):
    return exguard(tell_admin)(*args, **kargs)
