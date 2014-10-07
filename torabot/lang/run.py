from asyncio import coroutine
from .envs.gist import Env as GistEnv
from .envs.dict import Env as DictEnv
from .targets import Target


@coroutine
def run_json_gist(id, options):
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
def run_dict(conf):
    env = DictEnv(conf)
    return (yield from Target.run(
        env,
        {
            '@eval': {
                'json<': 'main.json'
            }
        }
    ))
