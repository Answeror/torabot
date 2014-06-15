from ...ut.bunch import bunchr, bunchset, bunchdel
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
    description = '订阅喜欢的画师和各种榜单(日榜, 月榜, R18等...), 邮件通知里包含新作的缩略图.'
    normal_search_prompt = '画师主页/名字/id'

    @property
    def carousel(self):
        from flask import url_for
        return url_for("main.example_search", kind=name, method="ranking", mode="daily", limit=10)

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
            'username': self.user_arts_changes,
        }[new.query.method](old, new)

    def user_arts_changes(self, old, new):
        oldmap = {art.uri: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            if art.uri not in oldmap:
                yield bunchr(kind='user_art.new', art=art)

    def ranking_changes(self, old, new):
        oldmap = {art.illust_id: art for art in getattr(old, 'arts', [])}
        arts = []
        for art in new.arts:
            if art.illust_id not in oldmap:
                arts.append(art)
        if arts:
            yield bunchr(kind='ranking', mode=new.query.mode, arts=arts)

    def spy(self, query, timeout):
        from .query import parse
        query = parse(query)
        return {
            'ranking': self.spy_ranking,
        }.get(query.method, self.spy_default)(query, timeout)

    def spy_default(self, query, timeout):
        from .query import regular
        return super(Pixiv, self).spy(regular(query), timeout)

    def spy_ranking(self, query, timeout):
        from .translate import modemap
        if query.mode not in modemap():
            raise Exception('unknown mode: %s' % query.mode)
        if 'limit' in query:
            return self.spy_limited_ranking(query, timeout)
        return self.spy_default(query, timeout)

    def spy_limited_ranking(self, query, timeout):
        from ..query import query as search
        from .query import regular
        limit = int(query.limit)
        result = search(
            self.name,
            regular(bunchdel(query, 'limit')),
            timeout
        )
        del result.arts[limit:]
        result.query = query
        return result


def parse_result(d):
    if d and 'query' in d:
        from .query import parse
        return bunchset(d, query=parse(d['query']))
    return bunchr(d)
