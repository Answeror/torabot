from .model import Query, Subscription
from logbook import Logger
from sqlalchemy.sql import exists, and_, join, delete, select, tuple_
from sqlalchemy.exc import IntegrityError


log = Logger(__name__)


def sub(user_id, query_text, session):
    query_id = session.query(Query.id).filter_by(text=query_text).scalar()
    session.add(Subscription(user_id=user_id, query_id=query_id))
    try:
        session.flush()
    except IntegrityError as e:
        if 'duplicate' in str(e):
            log.warning('subscription ({}, {}) exists', user_id, query_id)
            # must rollback here
            # otherwise further commit will fail
            session.rollback()
            pass


def unsub(user_id, query_text, session):
    session.execute(
        delete(Subscription.__table__)
        .where(
            # composite primary key in clause
            # https://groups.google.com/forum/#!topic/sqlalchemy/dsZkChpgQI4
            tuple_(Subscription.user_id, Subscription.query_id)
            .in_(
                select([Subscription.user_id, Subscription.query_id])
                .select_from(join(
                    Subscription,
                    Query,
                    Subscription.query_id == Query.id
                ))
                .where(Query.text == query_text)
                .alias()
            )
        )
    )


def has_sub(user_id, session, **kargs):
    if 'query_id' in kargs:
        return bool(session.query(exists().where(and_(
            Subscription.user_id == user_id,
            Subscription.query_id == kargs['query_id']
        ))).scalar())
    elif 'query_text' in kargs:
        return bool(session.query(
            exists()
            .select_from(join(
                Subscription.__table__,
                Query.__table__,
                Subscription.query_id == Query.id
            ))
            .where(and_(
                Subscription.user_id == user_id,
                Query.text == kargs['query_text']
            ))
        ).scalar())
    else:
        assert False, 'neither query id nor query text provided'
