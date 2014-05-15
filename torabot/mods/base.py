import abc
from .spy import spy


class Mod(object, metaclass=abc.ABCMeta):

    has_advanced_search = False
    has_normal_search = True
    normal_search_prompt = ''
    description = ''
    allow_empty_query = False

    def __init__(self, conf={}):
        self.conf = conf

    @abc.abstractproperty
    def name(self):
        pass

    def display_name(self):
        return self.name

    @abc.abstractmethod
    def changes(self, old, new):
        pass

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

    def spy(self, query, timeout, options={}):
        return spy(
            self.name,
            query,
            timeout=timeout,
            slaves=self.conf.get('TORABOT_SPY_SLAVES', 1),
            options=options,
        )
