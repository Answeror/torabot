from sqlalchemy import create_engine


def make(conf):
    return create_engine(conf['TORABOT_CONNECTION_STRING'])
