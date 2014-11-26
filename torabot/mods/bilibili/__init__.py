from asyncio import coroutine
from ...core.mod import (
    Mod,
    ViewMixin,
    field_guess_name_mixin
)


class Bilibili(
    ViewMixin,
    field_guess_name_mixin('title', 'user_id', 'username', 'query'),
    Mod
):

    name = 'bilibili'
    display_name = 'bilibili'
    description = '订阅新番和up主, 更新时会收到邮件通知.'
    has_advanced_search = True
    has_normal_search = False
    no_empty_query = True

    @coroutine
    def changes(self, old, new):
        from .changes import changes
        return (yield from changes(old, new))

    @coroutine
    def source(self, *args, **kargs):
        from .source import source
        return (yield from source(*args, **kargs))

    @coroutine
    def sync_on_expire(self, query):
        from .query import parse
        return parse(query.text).method != 'bangumi'

    @coroutine
    def regular(self, query):
        from .query import regular
        return self.name, regular(query)

    @coroutine
    def parse(self, query):
        from .query import parse
        return parse(query)

    def _query_method_from_result(self, result):
        if 'kind' in result:
            return result['kind']
        return result['query']['method']


bilibili = Bilibili()


__all__ = ['bilibili']
