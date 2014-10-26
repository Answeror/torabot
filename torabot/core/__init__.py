import importlib
from .facade import Core


core = Core()

for name in ['email', 'modo', 'mod', 'sync', 'user', 'notice']:
    importlib.import_module('.' + name, __name__)


__all__ = ['core']
