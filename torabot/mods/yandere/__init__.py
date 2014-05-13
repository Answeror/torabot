from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import (
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin
)


name = 'yandere'


class Yandere(
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin(__name__),
    Mod
):
    name = name
    display_name = 'yande.re'
    has_advanced_search = False
    description = '二次元高清图站, 直接订阅诸如 https://yande.re/post?tags=pantyhose 的链接.'
    normal_search_prompt = '订阅地址'

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email
        }[name]

    def changes(self, old, new):
        oldmap = {post.id: post for post in getattr(old, 'posts', [])}
        for post in new.posts:
            if post.id not in oldmap:
                yield bunchr(
                    kind='post.new',
                    post=post,
                    query_text=new.query.uri
                )

    def spy(self, query, timeout):
        from .query import parse, regular
        query = parse(query)
        return super(Yandere, self).spy(regular(query), timeout)
