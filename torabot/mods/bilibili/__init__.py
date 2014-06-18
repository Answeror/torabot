from nose.tools import assert_equal
from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import ViewMixin, NoEmptyQueryMixin, make_blueprint_mixin


name = 'bilibili'


class Bilibili(
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin(__name__),
    Mod
):

    name = name
    display_name = name
    has_advanced_search = True
    has_normal_search = False
    description = '订阅新番和up主, 更新时会收到邮件通知.'

    @property
    def carousel(self):
        from flask import url_for
        return url_for("main.example_advanced_search", kind=name)

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email,
        }[name]

    def changes(self, old, new):
        if old:
            assert_equal(
                query_method_from_result(old),
                query_method_from_result(new)
            )
        yield from {
            'bangumi': self._bangumi_changes,
            'sp': self._sp_changes,
            'user': self._user_changes,
            'username': self._user_changes,
            'query': self._query_changes,
        }[query_method_from_result(new)](old, new)

    def _bangumi_changes(self, old, new):
        return []

    def _sp_changes(self, old, new):
        if not old:
            yield bunchr(kind='sp_new', sp=new.sp)
            return
        if not new or not new.sp:
            return
        if new.sp.lastupdate != old.sp.lastupdate:
            yield bunchr(kind='sp_update', sp=new.sp)

    def spy(self, query, timeout):
        from .query import standard_query
        query, d = standard_query(query)
        if d.get('method') == 'sp':
            return self._spy_sp(d['title'])
        return super(Bilibili, self).spy(query, timeout)

    def _spy_sp(self, title):
        from .query import get_bangumi
        for sp in get_bangumi():
            if sp.title == title:
                return bunchr(kind='sp', sp=sp)
        return bunchr(kind='sp', sp=None)

    def _user_changes(self, old, new):
        return self._post_changes('user_new_post', old, new)

    def _query_changes(self, old, new):
        return self._post_changes('query_new_post', old, new)

    def _post_changes(self, kind_prefix, old, new):
        oldmap = {post.uri: post for post in getattr(old, 'posts', [])}
        for post in new.posts:
            if post.uri not in oldmap:
                yield bunchr(kind='user_new_post', post=post)

    def sync_on_expire(self, query):
        from ..booru.query import parse
        return parse(query.text).method != 'bangumi'


def query_method_from_result(result):
    if 'kind' in result:
        return result.kind
    return result.query.method


bp = Bilibili.blueprint

from .views import web
assert web
