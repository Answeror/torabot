import os
from . import const


def create_all(conn):
    conn.execute(load_text('schema.sql'))


def load_text(name):
    with open(os.path.join(const.PACKAGE_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')
