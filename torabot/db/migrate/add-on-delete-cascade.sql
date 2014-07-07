alter table change
drop constraint change_query_id_fkey,
add constraint change_query_id_fkey
    foreign key (query_id)
    references query(id)
    on delete cascade;

alter table email
drop constraint email_user_id_fkey,
add constraint email_user_id_fkey
    foreign key (user_id)
    references "user"(id)
    on delete cascade;

alter table notice
drop constraint notice_change_id_fkey,
add constraint notice_change_id_fkey
    foreign key (change_id)
    references change(id)
    on delete cascade;

alter table notice
drop constraint notice_user_id_fkey,
add constraint notice_user_id_fkey
    foreign key (user_id)
    references "user"(id)
    on delete cascade;

alter table watch
drop constraint watch_email_id_fkey,
add constraint watch_email_id_fkey
    foreign key (email_id)
    references email(id)
    on delete cascade;

alter table watch
drop constraint watch_query_id_fkey,
add constraint watch_query_id_fkey
    foreign key (query_id)
    references query(id)
    on delete cascade;

alter table watch
drop constraint watch_user_id_fkey,
add constraint watch_user_id_fkey
    foreign key (user_id)
    references "user"(id)
    on delete cascade;
