import os
from ...envs.fs import Env


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def make_fs_env():
    return Env(CURRENT_PATH)


def read(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')
