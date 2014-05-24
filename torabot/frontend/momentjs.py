from jinja2 import Markup
from datetime import datetime
import time


class Momentjs(object):

    def __init__(self, timestamp):
        self.timestamp = time_to_datetime(timestamp) if isinstance(timestamp, time.struct_time) else timestamp

    def render(self, format):
        return Markup("<span class=momentjs data-format='%s'>%s</span>" % (
            format,
            self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z")
        ))

    def format(self, fmt):
        return self.render(fmt)

    def calendar(self):
        return self.render("calendar")

    def fromnow(self):
        return self.render("fromnow")


def momentjs(timestamp):
    return Momentjs(timestamp)


def time_to_datetime(t):
    return datetime.fromtimestamp(time.mktime(t))
