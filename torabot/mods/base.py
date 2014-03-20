import abc


class Mod(object, metaclass=abc.ABCMeta):

    def __init__(self, conf={}):
        self.conf = conf

    @abc.abstractmethod
    def changes(self, old, new):
        pass

    @abc.abstractmethod
    def format_notice_status(self, view, notice):
        pass

    @abc.abstractmethod
    def format_notice_body(self, view, notice):
        pass

    @abc.abstractmethod
    def format_query_text(self, view, text):
        pass

    @abc.abstractmethod
    def format_query_result(self, view, result):
        pass
