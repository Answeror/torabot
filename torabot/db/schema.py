import os
from sqlalchemy.sql import text
from . import const


def create_all(conn):
    conn.execute(text(load_text('schema.sql')))


def load_text(name):
    with open(os.path.join(const.PACKAGE_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')
