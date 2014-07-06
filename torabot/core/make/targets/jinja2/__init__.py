import jsonpickle
from datetime import datetime
from jinja2 import Environment, PackageLoader
from ..base import Base


class Target(Base):

    unary = False

    def __init__(self, *args, **kargs):
        super(Target, self).__init__(*args, **kargs)
        self.jinja2_env = Environment(loader=PackageLoader(
            'torabot.core.make.targets.jinja2',
            'templates'
        ))
        self.jinja2_env.filters['tojson'] = jsonpickle.encode
        self.jinja2_env.globals['datetime'] = datetime

    def __call__(self, template, kargs):
        return self.get_template_content(template).render(**kargs)

    def get_template_content(self, name_or_content):
        if isinstance(name_or_content, str):
            return self.jinja2_env.from_string(name_or_content)
        assert isinstance(name_or_content, dict), 'unknown type: {}'.format(type(name_or_content))
        name = name_or_content['name']
        return self.jinja2_env.get_template(name)
