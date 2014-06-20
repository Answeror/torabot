from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import (
    ViewMixin,
    make_blueprint_mixin,
    IdentityGuessNameMixin,
    make_field_guess_name_mixin
)


name = 'ehentai'


class Ehentai(
    ViewMixin,
    make_blueprint_mixin(__name__),
    make_field_guess_name_mixin('uri', 'query'),
    IdentityGuessNameMixin,
    Mod
):
    name = name
    display_name = 'e-hentai'
    has_advanced_search = True
    description = '绅(hen)士(tai)图站(g.e-hentai.org)订阅(需登陆后使用)'
    normal_search_prompt = '查询条件或网址'
    allow_empty_query = True
    public = False

    @property
    def carousel(self):
        from flask import url_for
        return url_for("main.example_search", kind=name, q="language:chinese")

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email
        }[name]

    def changes(self, old, new):
        seen = {post.uri: post for post in old.get('posts', [])}
        for post in new.posts:
            if post.uri not in seen:
                yield bunchr(kind='post.new', query=new.query, post=post)

    def spy(self, query, timeout):
        from .query import regular
        return super(Ehentai, self).spy(regular(query), timeout)
