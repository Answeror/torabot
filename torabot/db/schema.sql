-- type
create type art_status as enum ('other', 'reserve');

-- table
create table art (
    id serial primary key,
    title text not null,
    author text,
    company text,
    uri text unique not null,
    status art_status,
    hash char(32),
    ptime timestamp
);

create table query (
    id serial primary key,
    text text unique
);

create table result (
    query_id int references query(id),
    art_id int references art(id),
    rank int not null,
    primary key (query_id, art_id),
    unique (query_id, rank)
);

create table "user" (
    id serial primary key,
    name text unique not null,
    email text unique not null,
    openid text unique not null,
    ctime timestamp default now()
);

create table watch (
    user_id int references "user"(id),
    query_id int references query(id),
    ctime timestamp default now()
);

create table change (
    id serial primary key,
    art_id int references art(id),
    old_status art_status,
    new_status art_status,
    ctime timestamp default now()
);

create table notice (
    id serial primary key,
    user_id int references "user"(id),
    change_id int references change(id),
    ctime timestamp default now()
);

-- trigger
create function insert_snapshot() returns trigger as $$
    begin
        insert into change (art_id, new_status) values (NEW.id, NEW.status);
        return NEW;
    end;
$$ language plpgsql;

create trigger insert_snapshot
    after insert on art
    for each row
    execute procedure insert_snapshot();

create function update_snapshot() returns trigger as $$
    begin
        insert into change (art_id, old_status, new_status) values (NEW.id, OLD.status, NEW.status);
        return NEW;
    end;
$$ language plpgsql;

create trigger update_snapshot
    after update on art
    for each row
    when (OLD.status is distinct from NEW.status and NEW.status != 'other')
    execute procedure update_snapshot();

create function broadcast() returns trigger as $$
    begin
        insert into notice (user_id, change_id)
            select watch.user_id as user_id, related.id as change_id
            from watch, (
                select id, ctime
                from change
                where change.art_id = NEW.art_id and not exists (
                    select *
                    from notice
                    where notice.change_id = change.id and notice.ctime >= change.ctime
                )
            ) as related
            where watch.query_id = NEW.query_id and watch.ctime <= related.ctime;
        return NEW;
    end;
$$ language plpgsql;

create trigger insert_broadcast
    after insert on result
    for each row
    execute procedure broadcast();
