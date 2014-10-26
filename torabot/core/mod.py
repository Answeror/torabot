from asyncio import coroutine
from logbook import Logger
from datetime import datetime, timedelta
from nose.tools import assert_is_instance
from flask import current_app
import abc
from ..db import db
from . import core


log = Logger(__name__)


@core.initializer
def init_app(app):
    app.config.setdefault('TORABOT_QUERY_EXPIRE', 15 * 60)
    app.config.setdefault('TORABOT_SYNC_ON_EXPIRE', True)


class InstanceField(object):

    def __get__(self, obj, cls):
        if cls is None:
            cls = type(obj)
        return core.mod(cls.name)


@core.setattr
class Mod(metaclass=abc.ABCMeta):

    instance = InstanceField()

    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractmethod
    def changes(self, old, new):
        pass

    @abc.abstractmethod
    def source(self, query, options={}):
        pass

    @abc.abstractmethod
    def regular(self, query_text):
        '''return most standard query kind and text'''
        pass

    @db.with_optional_bind
    @coroutine
    def search(self, text, bind, sync_on_expire=None):
        '''return None means first sync failed'''

        @coroutine
        def get_query():
            with db.connection_context(bind=bind) as conn:
                return (yield from db.get_query_bi_kind_and_text(conn, self.name, text))

        @coroutine
        def sync():
            return (yield from core.sync(kind=self.name, text=text, bind=bind))

        @coroutine
        def has():
            with db.connection_context(bind=bind) as conn:
                query = yield from db.get_query_bi_kind_and_text(conn, self.name, text)
                return bool(query and query.result)

        if not (yield from has()):
            log.info('query {} of {} dosn\'t exist', text, self.name)
            if (yield from sync()):
                query = yield from get_query()
            else:
                query = None
        else:
            query = yield from get_query()
            if (yield from self.expired(query)):
                log.debug('query {} of {} expired', text, self.name)
                if (
                    (yield from self.sync_on_expire(query))
                    if sync_on_expire is None
                    else sync_on_expire
                ):
                    if (yield from sync()):
                        query = yield from get_query()
                    else:
                        log.debug(
                            'sync {} of {} timeout or meet expected error',
                            text,
                            self.name
                        )
                else:
                    log.debug('mark query {} of {} need sync', text, self.name)
                    with db.connection_context(commit=True, bind=bind) as conn:
                        yield from db.set_next_sync_time_bi_kind_and_text(
                            conn,
                            self.name,
                            text,
                            datetime.utcnow()
                        )

        if query is not None and not query.result:
            raise core.CoreError('Invalid query: {}'.format(query))

        return query

    def expired(self, query):
        return query.mtime + timedelta(seconds=self.life(query)) < datetime.utcnow()

    def life(self, query):
        t = current_app.config['TORABOT_QUERY_EXPIRE']
        assert_is_instance(t, int)
        return t

    def sync_on_expire(self, query):
        return current_app.config['TORABOT_SYNC_ON_EXPIRE']


__all__ = ['Mod']
