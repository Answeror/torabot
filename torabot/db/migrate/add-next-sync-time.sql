alter table query add column next_sync_time timestamp without time zone;
create index idx_query_next_sync_time on query (next_sync_time);
