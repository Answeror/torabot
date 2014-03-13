import os
import json


CURRENT_PATH = os.path.dirname(__file__)


def kanji():
    if not hasattr(kanji, 'data'):
        with open(os.path.join(CURRENT_PATH, 'kanji.json'), 'rb') as f:
            kanji.data = json.loads(f.read().decode('utf-8'))
    return kanji.data


def translate(s):
    return ''.join(kanji()[c][0] if c in kanji() else c for c in s)
