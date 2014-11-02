from asyncio import coroutine
from ..ut.facade import Facade
from ..ut.request import request


class Lang(Facade):

    class LangError(Exception):
        pass

    def init_app(self, app):
        super().init_app(app)
        request.init_app(app)

    @coroutine
    def run_json_gist(self, id, options):
        from .targets import Target
        from .envs.gist import Env as GistEnv
        env = GistEnv(id)
        return (yield from Target.run(
            env,
            {
                '@eval': {
                    '@json_decode': {
                        '@jinja2': {
                            'template': {'text<': 'main.json'},
                            'kargs': options
                        }
                    }
                }
            }
        ))

    @coroutine
    def run_dict(self, conf):
        from .targets import Target
        from .envs.dict import Env as DictEnv
        env = DictEnv(conf)
        return (yield from Target.run(
            env,
            {
                '@eval': {
                    'json<': 'main.json'
                }
            }
        ))
