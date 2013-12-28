from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Index
from .tora import order_uri_from_toraid, toraid_from_order_uri
from . import state


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

    @declared_attr
    def __table_args__(cls):
        return (Index('%s_idx_toraid_state' % cls.__tablename__, 'toraid', 'state'),)

    @property
    def uri(self):
        return order_uri_from_toraid(self.toraid)

    @uri.setter
    def uri(self, value):
        return toraid_from_order_uri(value)

    @property
    def reserve(self):
        return self.state == state.RESERVE
