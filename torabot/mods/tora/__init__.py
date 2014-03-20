from ..base import Mod
from .change import changes
from .views import web, email


class Tora(Mod):

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

    def format_query_result(self, view, result):
        return self.view(view).format_query_result(result)
