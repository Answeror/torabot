from .. import db


def get_notices_bi_user_id(user_id, session):
    return db.get_notices_bi_user_id(
        session.connection(),
        user_id=user_id
    )


def get_pending_notices_bi_user_id(user_id, session):
    return db.get_pending_notices_bi_user_id(
        session.connection(),
        user_id=user_id
    )
