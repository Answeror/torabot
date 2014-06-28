import jsonpickle
from jinja2 import Environment, PackageLoader
from ..base import Base


jinja2_env = Environment(loader=PackageLoader(
    'torabot.core.make.targets.jinja2',
    'templates'
))
jinja2_env.filters['tojson'] = jsonpickle.encode


class Target(Base):

    def __call__(self, args):
        args = jsonpickle.decode(args)
        return self.template.render(args=args, **self.options['kargs'])

    @property
    def template(self):
        try:
            return jinja2_env.get_template(self.options['name'])
        except:
            return jinja2_env.Template(self.read_text(self.options['name']))
