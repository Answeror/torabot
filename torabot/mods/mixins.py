import json
from flask import Blueprint
import importlib
from ..ut.bunch import bunchr
from ..core.kanji import translate


class BlueprintField(object):

    def __init__(self, import_name):
        self.import_name = import_name

    def __get__(self, obj, cls):
        if cls is None:
            cls = type(obj)
        name = '_blueprint'
        value = getattr(self, name, None)
        if value is None:
            value = Blueprint(
                cls.name,
                self.import_name,
                static_folder='static',
                template_folder='templates',
                static_url_path='/%s/static' % cls.name
            )
            setattr(cls, name, value)
        return value


def make_blueprint_mixin(import_name):
    class BlueprintMixin(object):

        blueprint = BlueprintField(import_name)

    return BlueprintMixin


class ViewMixin(object):

    def format_notice_status(self, view, notice):
        return self.view(view).format_notice_status(notice)

    def format_notice_body(self, view, notice):
        return self.view(view).format_notice_body(notice)

    def format_query_text(self, view, text):
        f = getattr(self.view(view), 'format_query_text', None)
        if f is None:
            return super(ViewMixin, self).format_query_text(view, text)
        return f(text)

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


class ModuleViewMixin(ViewMixin):

    def __init__(self, import_name):
        self.import_name = import_name

    def view(self, name):
        return importlib.import_module('..' + name, self.import_name)


def make_module_view_mixin(import_name):
    return ModuleViewMixin(import_name)


class NoEmptyQueryMixin(object):

    def spy(self, query, timeout):
        for test in getattr(self, 'empty_query_tests', [
            lambda query: not query
        ]):
            if test(query):
                return bunchr(
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


class Jinja2Mixin(object):

    @property
    def jinja2_env(self):
        name = '_jinja2_env'
        value = getattr(self, name, None)
        if value is None:
            from jinja2 import Environment, PackageLoader
            value = Environment(loader=PackageLoader('torabot.mods.' + self.name, 'templates'))
            setattr(self, name, value)
        return value


class IdentityGuessNameMixin(object):

    def guess_name(self, query):
        return query.text


def make_field_guess_name_mixin(field, *args):
    if isinstance(field, str):
        fields = [field]
    else:
        fields = field
    fields.extend(args)

    class FieldGuessNameMixin(object):

        def guess_name(self, query):
            try:
                d = json.loads(query.text)
                if isinstance(d, dict):
                    for name in fields:
                        value = d.get(name, None)
                        if value:
                            return value
            except:
                pass
            return super(FieldGuessNameMixin, self).guess_name(query)

    return FieldGuessNameMixin


class ScrapyMixin(object):

    def spy(self, query, timeout, options={}):
        from .spy import spy
        return spy(
            self.name,
            query,
            timeout=timeout,
            slaves=self.spy_slaves,
            options=options,
            life=self.spy_life
        )

    @property
    def spy_slaves(self):
        return self.conf.get('TORABOT_SPY_SLAVES', 1)

    @property
    def spy_life(self):
        return self.conf.get('TORABOT_SPY_LIFE')


class NoChangeMixin(object):

    def changes(self, old, new, **kargs):
        return []
