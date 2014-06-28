from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import (
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin,
    Jinja2Mixin,
    IdentityGuessNameMixin,
    make_field_guess_name_mixin
)


name = 'feed'


class Feed(
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin(__name__),
    Jinja2Mixin,
    make_field_guess_name_mixin('uri'),
    IdentityGuessNameMixin,
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
        from .ut import entry_id
        seen = {entry_id(entry): entry for entry in old.get('data', {}).get('entries', [])}
        for i, entry in enumerate(new.get('data', {}).get('entries', [])):
            if entry_id(entry) not in seen:
                yield bunchr(kind='feed.new', query=new.query, entry=entry)

    def spy(self, query, timeout):
        from .query import parse, regular
        query = parse(query)
        return super(Feed, self).spy(regular(query), timeout)

    def format_notice_status(self, view, notice):
        from .types import Notice
        return super(Feed, self).format_notice_status(view, Notice(notice))

    def format_notice_body(self, view, notice):
        from .types import Notice
        return super(Feed, self).format_notice_body(view, Notice(notice))

    def format_query_result(self, view, query):
        from .types import Query
        return super(Feed, self).format_query_result(view, Query(query))

    def notice_attachments(self, view, notice):
        f = getattr(self.view(view), 'notice_attachments', None)
        if f is None:
            from .types import Notice
            return super(Feed, self).notice_attachments(view, Notice(notice))
        return f(notice)
