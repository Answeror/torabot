from .sync import sync, has_query
from sqlalchemy.orm import joinedload


def query(text, session):
    if not has_query(text=text, session=session):
        return sync(text, session=session)
    return (
        session.query(Query)
        .filter_by(text=text)
        .options(joinedload(Query.result))
        .one()
    ).arts
