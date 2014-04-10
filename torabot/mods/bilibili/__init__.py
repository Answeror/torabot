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

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email,
        }[name]

    def changes(self, old, new):
        if not old:
            yield bunchr(kind='new', data=new)
            return

        assert_equal(old.kind, new.kind)
        yield from {
            'bangumi': self._bangumi_changes,
            'sp': self._sp_changes,
            'user': self._user_changes,
        }[new.kind](old, new)

    def _bangumi_changes(self, old, new):
        return []

    def _sp_changes(self, old, new):
        if new.sp.lastupdate != old.sp.lastupdate:
            yield bunchr(kind='sp_update', data=new)

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
                return bunchr(sp=sp)

    def _user_changes(self, old, new):
        oldmap = {post.uri: post for post in getattr(old, 'posts', [])}
        for post in new.posts:
            if post.uri not in oldmap:
                yield bunchr(kind='user_new_post', post=post)


bp = Bilibili.blueprint

from .views import web
assert web
