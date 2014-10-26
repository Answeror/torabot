import abc
from .mixins import ScrapyMixin
from ..core import core


class Core(core.Mod):
    '''mod without frontend'''
    pass


class Frontend(ScrapyMixin, Core):
    '''mod with frontend'''

    has_advanced_search = False
    has_normal_search = True
    normal_search_prompt = ''
    description = ''
    allow_empty_query = False
    frontend_need_init = False
    frontend_options = {}
    completion_options = {}
    public = True

    def display_name(self):
        return self.name

    @abc.abstractmethod
    def format_notice_status(self, view, notice):
        pass

    @abc.abstractmethod
    def format_notice_body(self, view, notice):
        pass

    def notice_attachments(self, view, notice):
        return []

    def format_query_text(self, view, text):
        return text

    @abc.abstractmethod
    def format_query_result(self, view, query):
        pass

    @abc.abstractmethod
    def format_advanced_search(self, view, **kargs):
        pass

    def format_help_page(self):
        return ''

    def get(self, arg):
        return {}

    @property
    def carousel(self):
        pass

    def guess_name(self, query):
        pass


# for back compatibility
Mod = Frontend
