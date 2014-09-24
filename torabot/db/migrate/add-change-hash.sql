alter table change add column hash text;
create index idx_change_hash on change (hash);
