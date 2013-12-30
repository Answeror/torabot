from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Index,
    ForeignKey,
    DateTime,
)
from .tora import order_uri_from_toraid, toraid_from_order_uri
from . import state
from .time import utcnow


Base = declarative_base()
Session = sessionmaker()


class Art(Base):

    __tablename__ = 'art'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    comp = Column(String)
    toraid = Column(String(12), unique=True, index=True)
    state = Column(Integer, index=True)
    ptime = Column(DateTime)
    atime = Column(DateTime, default=utcnow)
    timestamp = Column(String(32))

    @declared_attr
    def __table_args__(cls):
        return (Index('%s_idx_toraid_state' % cls.__tablename__, 'toraid', 'state'),)

    @property
    def uri(self):
        return order_uri_from_toraid(self.toraid)

    @uri.setter
    def uri(self, value):
        self.toraid = toraid_from_order_uri(value)

    @property
    def reserve(self):
        return self.state == state.RESERVE


class Change(Base):

    __tablename__ = 'change'

    id = Column(Integer, primary_key=True)
    art_id = Column(Integer, ForeignKey(Art.id), index=True)
    what = Column(Integer)
    ctime = Column(DateTime, default=utcnow, index=True)

    art = relationship(Art)


class Query(Base):

    __tablename__ = 'query'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    ctime = Column(DateTime, default=utcnow, index=True)

    result = relationship('Result', order_by='Result.rank')

    @property
    def arts(self):
        return map(lambda qa: qa.art, self.result)


class Result(Base):

    __tablename__ = 'result'

    query_id = Column(Integer, ForeignKey(Query.id), primary_key=True, index=True)
    art_id = Column(Integer, ForeignKey(Art.id), primary_key=True)
    rank = Column(Integer, index=True)

    query = relationship(Query)
    art = relationship(Art)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    openid = Column(String, unique=True, index=True)
