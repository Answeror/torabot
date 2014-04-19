from ...ut.bunch import bunchr, set as bset
from ..base import Mod
from ..mixins import (
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin
)


name = 'pixiv'


class Pixiv(
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin(__name__),
    Mod
):

    name = name
    display_name = name
    has_advanced_search = True

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email,
        }[name]

    def changes(self, old, new):
        old = parse_result(old)
        new = parse_result(new)
        return {
            'user_id': self.user_arts_changes,
            'user_uri': self.user_arts_changes,
            'user_illustrations_uri': self.user_arts_changes,
            'ranking': self.ranking_changes,
        }[new.query.method](old, new)

    def user_arts_changes(self, old, new):
        oldmap = {art.uri: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            if art.uri not in oldmap:
                yield bunchr(kind='new', query=new.query, art=art)

    def ranking_changes(self, old, new):
        oldmap = {art.illust_id: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            if art.illust_id not in oldmap:
                yield bunchr(kind='new', query=new.query, art=art)

    def spy(self, query, timeout):
        from .query import regular
        return super(Pixiv, self).spy(regular(query), timeout)


def parse_result(d):
    if d and 'query' in d:
        from .query import parse
        return bset(d, query=parse(d['query']))
    return bunchr(d)
