import json
from ..base import Mod as Base
from ..mixins import (
    ViewMixin,
    make_blueprint_mixin,
    IdentityGuessNameMixin
)


class Mod(
    make_module_view_mixin(__name__),
    make_blueprint_mixin(__name__),
    IdentityGuessNameMixin,
    Base
):
    name = 'pic'
    display_name = 'pic'
    has_advanced_search = True
    has_normal_search = False
    description = '任意图站的图片订阅'
    public = True

    def _parse_query(self, text):
        d = json.loads(text)
        return d['source'], d['changes']

    def changes_v2(self, query, result):
        from ...core.backends.redis import Redis
        from ...core.mod import mod
        _, changes = self._parse_query(query.text)
        q = mod('onereq').search(
            json.dumps({
                'uri': 'http://%s/api/changes/%s' % (
                    self.conf['TORABOT_DOMAIN'],
                    changes
                )
            }),
            timeout=30,
            sync_on_expire=False,
            backend=Redis()
        )
        if not q:
            raise Exception('detect changes failed')
        return q.result

    def spy(self, query_text, timeout):
        from ...core.backends.redis import Redis
        from ...core.mod import mod
        source, _ = self._parse_query(query_text)
        q = mod('onereq').search(
            json.dumps({
                'uri': 'http://%s/api/source/%s' % (
                    self.conf['TORABOT_DOMAIN'],
                    source
                )
            }),
            timeout=30,
            sync_on_expire=False,
            backend=Redis()
        )
        if not q:
            raise Exception('fetch source failed')
        return q.result

    def regular(self, query_text):
        source, changes = self._parse_query(query_text)
        if not source or not changes:
            raise Exception('illegal query: %s' % query_text)
        return query_text
