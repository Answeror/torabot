from jinja2 import Markup


class Momentjs(object):

    def __init__(self, timestamp):
        self.timestamp = timestamp

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
