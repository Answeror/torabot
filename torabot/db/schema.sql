-- type
create type notice_status as enum ('pending', 'sent');

-- table
create table if not exists query (
    id serial primary key,
    kind text not null,
    text text not null,
    result json not null default '{}',
    ctime timestamp default now(),
    unique (kind, text)
);

create index idx_query_kind_text on query (kind, text);
create index idx_query_ctime on query (ctime);

create table if not exists "user" (
    id serial primary key,
    name text unique not null,
    email text unique not null,
    openid text unique not null,
    ctime timestamp default now(),
    maxwatch int not null default 42
);

create index idx_user_openid on "user" (openid);

create table if not exists watch (
    user_id int references "user"(id),
    query_id int references query(id),
    ctime timestamp default now()
);

create index idx_watch_ctime on watch (ctime);

create table if not exists change (
    id serial primary key,
    query_id int references query(id),
    data json not null default '{}',
    ctime timestamp default now()
);

create table if not exists notice (
    id serial primary key,
    user_id int references "user"(id),
    change_id int references change(id),
    ctime timestamp default now(),
    status notice_status default 'pending'
);

create index idx_notice_mix on notice (user_id, status, change_id, ctime);

-- function

create or replace function get_or_add_query_bi_kind_and_text(kind text, text text)
    returns setof query
as $$
    begin
        insert into query (kind, text)
        select $1, $2
        where not exists (
            select 1 from query as q
            where q.kind = $1 and q.text = $2
        );
        return query select * from query as q where q.kind = $1 and q.text = $2;
    end
$$ language plpgsql;

-- trigger
create or replace function check_maxwatch() returns trigger as $$
    declare
        maxwatch int;
        watch_count int;
    begin
        select "user".maxwatch into strict maxwatch from "user" where id = NEW.user_id;
        select count(*) into strict watch_count from watch where user_id = NEW.user_id;
        if (watch_count >= maxwatch) then
            raise exception '% watch count reach limit %', NEW.user_id, maxwatch;
        end if;
        return NEW;
    end;
$$ language plpgsql;

drop trigger if exists check_maxwatch on watch;
create trigger check_maxwatch
    before insert on watch
    for each row
    execute procedure check_maxwatch();

create or replace function broadcast() returns trigger as $$
    begin
        insert into notice (user_id, change_id)
            select watch.user_id as user_id, NEW.id as change_id
            from watch
            where watch.query_id = NEW.query_id and watch.ctime <= NEW.ctime;
        return NEW;
    end;
$$ language plpgsql;

drop trigger if exists insert_broadcast on change;
create trigger insert_broadcast
    after insert on change
    for each row
    execute procedure broadcast();
