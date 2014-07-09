import json
import base64
import jinja2
from logbook import Logger
from celery.exceptions import SoftTimeLimitExceeded
from ..core.local import get_current_conf
from ..core.make.envs.dict import Env
from ..core.make.targets import Target
from ..core.mod import mod
from ..core.backends.redis import Redis
from ..ut.guard import time_logged, func_log_injected
from ..ut.bunch import bunchr


log = Logger(__name__)


def get_conf(files, args):
    for f in files:
        if f['name'] == 'torabot.json':
            return json.loads(jinja2.Template(
                base64.b64decode(f['content']).decode('utf-8')
            ).render(**args))


@func_log_injected
@time_logged
def make_source(gist, args):
    try:
        q = mod('gist').search(
            text=json.dumps(dict(method='id', id=gist)),
            timeout=get_current_conf()['TORABOT_SPY_TIMEOUT'],
            sync_on_expire=True,
            backend=Redis()
        )
        if not q:
            return 502

        conf = get_conf(q.result.files, args)
        if not conf:
            return 404

        return Target.run(Env(bunchr(q.result.files)), conf)
    except SoftTimeLimitExceeded:
        log.warning('make source soft timeout')
        return 502
