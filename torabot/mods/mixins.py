import abc
import json
from ..ut.bunch import Bunch
from ..core.kanji import translate


class ViewMixin(object):

    @abc.abstractmethod
    def view(self, name):
        pass

    def format_notice_status(self, view, notice):
        return self.view(view).format_notice_status(notice)

    def format_notice_body(self, view, notice):
        return self.view(view).format_notice_body(notice)

    def format_query_text(self, view, text):
        return self.view(view).format_query_text(text)

    def format_query_result(self, view, query):
        return self.view(view).format_query_result(query)

    def format_advanced_search(self, view, **kargs):
        return self.view(view).format_advanced_search(**kargs)

    def format_help_page(self):
        f = getattr(self.view('web'), 'format_help_page', None)
        if f is None:
            return super(ViewMixin, self).format_help_page()
        return f()

    def notice_attachments(self, view, notice):
        f = getattr(self.view(view), 'notice_attachments', None)
        if f is None:
            return super(ViewMixin, self).notice_attachments(view, notice)
        return f(notice)


class NoEmptyQueryMixin(object):

    def spy(self, query, timeout):
        if not query:
            return Bunch(
                query=query,
                uri='',
                total=0,
                arts=[],
            )
        return super(NoEmptyQueryMixin, self).spy(query, timeout)


class KanjiMixin(object):

    def translate_kanji(self, text):
        if self.conf.get('TORABOT_MOD_%s_TRANSLATE_KANJI' % self.name, True):
            return _translate(text)
        return text

    def spy(self, query, timeout):
        return super(KanjiMixin, self).spy(self.translate_kanji(query), timeout)


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
