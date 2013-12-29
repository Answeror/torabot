from sqlalchemy.sql import func, select
from .model import Change


def pop_change(session):
    lastq = select([func.max(Change.ctime).label('ctime')]).correlate().alias()
    change = session.query(Change).filter(Change.ctime == lastq.c.ctime).first()
    if change:
        session.delete(change)
    return change
