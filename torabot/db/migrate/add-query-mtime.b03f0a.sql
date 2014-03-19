alter table query add column mtime timestamp default (now() at time zone 'utc');
