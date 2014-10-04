import logbook
from ..ut.local import local
from .schema import create_all


class DatabaseFixture(object):

    def setup(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()

        # Connect to the database and create the schema within a transaction
        from sqlalchemy import create_engine
        self.engine = create_engine(local.conf['TORABOT_TEST_CONNECTION_STRING'])
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        create_all(self.connection)

    def teardown(self):
        # Roll back the top level transaction and disconnect from the database
        self.transaction.rollback()
        self.connection.close()
        self.engine.dispose()

        self.log_handler.pop_thread()
