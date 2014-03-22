import json
from ...ut.bunch import Bunch
from ...core.kanji import translate
from ..base import Mod
from .change import changes
from .views import web, email


class Tora(Mod):

    name = 'tora'
    display_name = '虎穴'

    def view(self, name):
        return {
            'web': web,
            'email': email,
        }[name]

    def changes(self, old, new):
        return changes(old, new)

    def format_notice_status(self, view, notice):
        return self.view(view).format_notice_status(notice)

    def format_notice_body(self, view, notice):
        return self.view(view).format_notice_body(notice)

    def format_query_text(self, view, text):
        return self.view(view).format_query_text(text)

    def format_query_result(self, view, query):
        return self.view(view).format_query_result(query)

    def format_advanced_search(self, view, query):
        return self.view(view).format_advanced_search(self.name, query)

    def spy(self, query, timeout):
        if not query:
            return Bunch(
                query=query,
                uri='',
                total=0,
                arts=[],
            )
        return Mod.spy(self, self.translate(query), timeout)

    def translate(self, text):
        if self.conf.get('TORABOT_MOD_TORA_TRANSLATE', True):
            return _translate(text)
        return text


def _translate(query):
    try:
        query = json.loads(query)
        return json.dumps(translate_recursive(query), sort_keys=True)
    except:
        return translate(query)


def translate_recursive(d):
    if isinstance(d, dict):
        return {key: translate_recursive(value) for key, value in d.items()}
    if isinstance(d, list):
        return [translate_recursive(e) for e in d]
    return translate(d)
