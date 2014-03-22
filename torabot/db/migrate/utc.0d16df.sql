alter table query alter column ctime set default (now() at time zone 'utc');
alter table "user" alter column ctime set default (now() at time zone 'utc');
alter table watch alter column ctime set default (now() at time zone 'utc');
alter table change alter column ctime set default (now() at time zone 'utc');
alter table notice alter column ctime set default (now() at time zone 'utc');

create or replace function update_query_mtime() returns trigger as $$
begin
    NEW.mtime = (now() at time zone 'utc');
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists update_query_mtime on query;
create trigger update_query_mtime
    before update on query
    for each row
    execute procedure update_query_mtime();
