alter table "user" alter column openid drop not null;
alter table "user" add column password_hash text;
