from jinja2 import Markup
from datetime import datetime
import time


ISO = '%Y-%m-%dT%H:%M:%S.%fZ'


class Momentjs(object):

    def __init__(self, timestamp):
        if isinstance(timestamp, str):
            self.timestamp = datetime.strptime(timestamp, ISO)
        elif isinstance(timestamp, time.struct_time):
            self.timestamp = time_to_datetime(timestamp)
        else:
            assert isinstance(timestamp, datetime), type(timestamp)
            self.timestamp = timestamp

    def render(self, format):
        return Markup("<span class=momentjs data-format='%s'>%s</span>" % (
            format,
            self.timestamp.strftime(ISO)
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
