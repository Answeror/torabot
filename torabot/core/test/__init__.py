import logbook
from ...ut.bunch import Bunch
from ...db.schema import create_all


g = Bunch()


CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-test')
)


def setup_module():
    g.log_handler = logbook.TestHandler()
    g.log_handler.push_thread()

    # Connect to the database and create the schema within a transaction
    from sqlalchemy import create_engine
    g.engine = create_engine(CONNECTION_STRING)
    g.connection = g.engine.connect()
    g.transaction = g.connection.begin()
    create_all(g.connection)


    # If you want to insert fixtures to the DB, do it here


def teardown_module():
    # Roll back the top level transaction and disconnect from the database
    g.transaction.rollback()
    g.connection.close()
    g.engine.dispose()

    g.log_handler.pop_thread()
