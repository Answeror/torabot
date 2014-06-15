from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import (
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin
)


name = 'feed'


class Feed(
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin(__name__),
    Mod
):
    name = name
    display_name = 'feed'
    has_advanced_search = False
    description = 'RSS/Atom订阅'
    normal_search_prompt = 'feed uri'

    @property
    def carousel(self):
        from flask import url_for
        return url_for("main.example_search", kind=name, q="https://yande.re/post/atom?tags=rating:s")

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email
        }[name]

    def changes(self, old, new):
        seen = {entry.id: entry for entry in old.get('data', {}).get('entries', [])}
        for i, entry in enumerate(new.get('data', {}).get('entries', [])):
            if entry.id not in seen:
                yield bunchr(kind='feed.new', entry=entry, data=new, index=i)

    def spy(self, query, timeout):
        from .query import parse, regular
        query = parse(query)
        return super(Feed, self).spy(regular(query), timeout)
