from datetime import timedelta
from ... import db
from .base import Backend


class PostgreSQL(Backend):

    def __init__(self, conn):
        self.conn = conn

    def has_query_bi_kind_and_text(self, kind, text):
        return db.has_query_bi_kind_and_text(self.conn, kind, text)

    def get_query_bi_kind_and_text(self, kind, text):
        return db.get_query_bi_kind_and_text(self.conn, kind, text)

    def set_next_sync_time_bi_kind_and_text(self, kind, text, time):
        return db.set_next_sync_time_bi_kind_and_text(self.conn, kind, text, time)

    def get_or_add_query_bi_kind_and_text(self, kind, text):
        return db.get_or_add_query_bi_kind_and_text(self.conn, kind, text)

    def touch_query_bi_id(self, id):
        return db.touch_query_bi_id(self.conn, id)

    def add_one_query_changes(self, id, changes):
        return db.add_one_query_changes_unique(
            self.conn,
            id,
            changes,
            timedelta(days=1)
        )

    def set_query_result(self, id, result):
        return db.set_query_result(self.conn, id, result)

    def is_query_active_bi_id(self, id):
        return db.is_query_active_bi_id(self.conn, id)

    def set_next_sync_time(self, id, time):
        return db.set_next_sync_time(self.conn, id, time)

    def get_query_bi_id(self, id):
        return db.get_query_bi_id(self.conn, id)
