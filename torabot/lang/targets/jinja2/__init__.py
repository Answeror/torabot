import json
from asyncio import coroutine
from datetime import datetime
from jinja2 import Environment, PackageLoader
from hashlib import md5
from ... import lang
from ..base import Base


class Target(Base):

    unary = False

    def _init_jinja2_env(self):
        self.jinja2_env = Environment(loader=PackageLoader(
            self.__module__,
            'templates'
        ))
        self.jinja2_env.filters.update(
            tojson=json.dumps,
            md5=lambda s: md5(s).hexdigest()
        )
        self.jinja2_env.globals.update(
            datetime=datetime
        )

    @coroutine
    def __call__(self, template, kargs={}):
        self._init_jinja2_env()
        return self.get_template_content(template).render(**kargs)

    def get_template_content(self, name_or_content):
        if isinstance(name_or_content, str):
            return self.jinja2_env.from_string(name_or_content)
        if not isinstance(name_or_content, dict):
            raise lang.LangError('Unknown type: {}'.format(type(name_or_content)))
        name = name_or_content['name']
        return self.jinja2_env.get_template(name)
