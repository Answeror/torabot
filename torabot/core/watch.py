from .. import db


def watch(user_id, query_id, session):
    return db.watch(
        session.connection(),
        user_id=user_id,
        query_id=query_id
    )


def unwatch(user_id, query_id, session):
    return db.unwatch(
        session.connection(),
        user_id=user_id,
        query_id=query_id
    )


def watching(user_id, query_id, session):
    return db.watching(
        session.connection(),
        user_id=user_id,
        query_id=query_id
    )


def get_watches_bi_user_id(user_id, session):
    return db.get_watches_bi_user_id(
        session.connection(),
        user_id=user_id
    )
