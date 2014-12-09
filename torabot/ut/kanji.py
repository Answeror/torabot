import os
import json
from logbook import Logger


CURRENT_PATH = os.path.dirname(__file__)

log = Logger(__name__)


def kanji():
    if not hasattr(kanji, 'data'):
        with open(os.path.join(CURRENT_PATH, 'kanji.json'), 'rb') as f:
            kanji.data = json.loads(f.read().decode('utf-8'))
    return kanji.data


def translate(s):
    t = ''.join(kanji()[c][0] if c in kanji() else c for c in s)
    # log.debug('translate: {} -> {}', s, t)
    return t


def translate_recursive(d):
    if isinstance(d, dict):
        return {key: translate_recursive(value) for key, value in d.items()}
    if isinstance(d, list):
        return [translate_recursive(e) for e in d]
    return translate(d)
