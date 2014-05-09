-- add email table and fill main email

create table if not exists email (
    id serial primary key,
    text text unique not null,
    label text,
    activated boolean not null default FALSE,
    ctime timestamp default (now() at time zone 'utc'),
    user_id int references "user"(id)
);

insert into email (text, label, activated, user_id)
    select email, 'main', activated, id from "user";

create index idx_email_user_id on email (user_id);
create index idx_email_text on email (text);
create index idx_email_id_activated on email (id, activated); -- for activated_watch view

-- add watch email_id field and fill

alter table watch add column email_id int references email(id);

update watch w0
    set email_id = e0.id
    from email as e0
    where w0.user_id = e0.user_id;

-- alter table watch drop constraint watch_pkey;
alter table watch add primary key (email_id, query_id);

drop index idx_watch_ctime;
create index idx_watch_user_id_ctime on watch (user_id, ctime);
create index idx_watch_user_id_query_id on watch (user_id, query_id);

-- add activated_watch view

create view activated_watch as
    select w0.*, e0.text email_text
    from watch w0 inner join email e0 on w0.email_id = e0.id
    where e0.activated = TRUE;

-- add notice email_id field and fill

alter table notice add column email text;

update notice n0
    set email = e0.text
    from email as e0
    where n0.user_id = e0.user_id;

alter table notice alter column email set not null;

-- trigger on update email text field

create or replace function update_main_email() returns trigger as $$
begin
    if (OLD.text != NEW.text or OLD.activated != NEW.activated) then
        update "user"
        set email = NEW.text, activated = NEW.activated
        where email = OLD.text;
    end if;
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists update_main_email on email;
create trigger update_main_email
    after update of text, activated on email
    for each row
    execute procedure update_main_email();

-- trigger on update user email field

create or replace function update_user_email() returns trigger as $$
begin
    if (OLD.email != NEW.email or OLD.activated != NEW.activated) then
        update email
        set text = NEW.email, activated = NEW.activated
        where text = OLD.email;
    end if;
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists update_user_email on "user";
create trigger update_user_email
    after update of email, activated on "user"
    for each row
    execute procedure update_user_email();

-- trigger on add user

create or replace function add_main_email_on_create_user() returns trigger as $$
begin
    insert into email (text, label, activated, user_id)
        values (NEW.email, 'main', NEW.activated, NEW.id);
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists add_main_email_on_create_user on "user";
create trigger add_main_email_on_create_user
    after insert on "user"
    for each row
    execute procedure add_main_email_on_create_user();

-- add user maxemail field

alter table "user" add column maxemail int check(maxemail > 0) default 3;

-- trigger on insert email

create or replace function check_maxemail() returns trigger as $$
declare
    maxemail int;
    email_count int;
begin
    select "user".maxemail into strict maxemail from "user" where id = NEW.user_id;
    select count(*) into strict email_count from email where user_id = NEW.user_id;
    if (email_count >= maxemail) then
        raise exception '% email count reach limit %', NEW.user_id, maxemail;
    end if;
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists check_maxemail on email;
create trigger check_maxemail
    before insert on email
    for each row
    execute procedure check_maxemail();

-- trigger on delete email

create or replace function check_main_email() returns trigger as $$
declare
    main_email text;
begin
    select email into strict main_email from "user" where id = OLD.user_id;
    if (OLD.text = main_email) then
        raise exception 'cannot delete main email of %', OLD.user_id;
    end if;
    return OLD;
end;
$$ language plpgsql;

drop trigger if exists check_main_email on email;
create trigger check_main_email
    before delete on email
    for each row
    execute procedure check_main_email();

-- trigger on insert watch

create or replace function fill_watch_email() returns trigger as $$
begin
    if (NEW.email_id is null) then
        select id into strict NEW.email_id from email where user_id = NEW.user_id;
        if (NEW.email_id is null) then
            raise exception 'no default email found for user %', NEW.user_id;
        end if;
    end if;
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists fill_watch_email on watch;
create trigger fill_watch_email
    before insert on watch
    for each row
    execute procedure fill_watch_email();

-- trigger broadcast

create or replace function broadcast() returns trigger as $$
begin
    insert into notice (user_id, change_id, email)
        select w0.user_id, NEW.id, w0.email_text
        from activated_watch w0
        where w0.query_id = NEW.query_id and w0.ctime <= NEW.ctime;
    return NEW;
end;
$$ language plpgsql;

drop trigger if exists insert_broadcast on change;
create trigger insert_broadcast
    after insert on change
    for each row
    execute procedure broadcast();
