from sqlalchemy.sql import func, select, insert, join, bindparam
from .model import Change, Notice, Result, Subscription
from .time import utcnow
from sqlalchemy import event
from .redis import redis


def pop_change(session):
    lastq = (
        select([func.max(Change.ctime).label('ctime')])
        .correlate()
        .alias()
    )
    change = (
        session.query(Change)
        .filter(Change.ctime == lastq.c.ctime)
        .first()
    )
    if change:
        notify(change, session)
        session.delete(change)
    return change


def pop_changes(session):
    while True:
        if pop_change(session) is None:
            break


def notify(change, session):
    related_query_id_q = (
        select([Result.query_id.label('id')])
        .where(Result.art_id == change.art_id)
        .alias()
    )
    related_user_id_q = (
        select([Subscription.user_id.label('id')])
        .select_from(join(
            Subscription,
            related_query_id_q,
            Subscription.query_id == related_query_id_q.c.id
        ))
        .where(Subscription.ctime <= change.ctime)
        .group_by(Subscription.user_id)
        .alias()
    )
    insert_q = (
        # use inline to disable implicit returning
        # otherwise empty user id query will result in TypeError
        # http://docs.sqlalchemy.org/en/latest/core/dml.html#sqlalchemy.sql.expression.Insert.from_select
        insert(Notice, inline=True)
        .from_select(
            [Notice.text, Notice.user_id, Notice.ctime],
            select([
                bindparam('b_text'),
                related_user_id_q.c.id,
                bindparam('b_ctime')
            ])
        )
    )
    session.execute(insert_q, {
        'b_text': change.text,
        'b_ctime': utcnow()
    })
    event.listen(session, 'after_commit', after_notice_commit)


def after_notice_commit(session):
    redis.rpush('notice', None)
