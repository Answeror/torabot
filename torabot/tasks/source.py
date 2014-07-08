from ..core.make.envs.dict import Env
from ..core.make.targets import Target
from ..ut.guard import timeguard
from ..ut.bunch import bunchr


@timeguard
def make_source(files, conf):
    return Target.run(Env(bunchr(files)), conf)
