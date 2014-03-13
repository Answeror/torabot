from .model import Query, Subscription
from logbook import Logger
from sqlalchemy.sql import exists, and_, join, delete, select
from sqlalchemy.exc import IntegrityError


log = Logger(__name__)


def sub(user_id, session, **kargs):
    query_id = kargs.get('query_id')
    if query_id is None:
        query_text = kargs.get('query_text')
        if query_text is None:
            assert False, 'neither query_id nor query_text provided'
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


def unsub(user_id, session, **kargs):
    if 'query_id' in kargs:
        session.execute(
            delete(Subscription)
            .where(and_(
                Subscription.user_id == user_id,
                Subscription.query_id == kargs['query_id']
            ))
        )
    elif 'query_text' in kargs:
        session.execute(
            delete(Subscription)
            .where(and_(
                Subscription.user_id == user_id,
                Subscription.query_id == (
                    select([Query.id])
                    .where(Query.text == kargs['query_text'])
                    # cannot use alias here
                )
            ))
        )
    else:
        assert False, 'neither query_id nor query_text provided'


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
