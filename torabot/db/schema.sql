--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: notice_status; Type: TYPE; Schema: public; Owner: answeror
--

CREATE TYPE notice_status AS ENUM (
    'pending',
    'sent'
);


ALTER TYPE public.notice_status OWNER TO answeror;

--
-- Name: add_main_email_on_create_user(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION add_main_email_on_create_user() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    insert into email (text, label, activated, user_id)
        values (NEW.email, 'main', NEW.activated, NEW.id);
    return NEW;
end;
$$;


ALTER FUNCTION public.add_main_email_on_create_user() OWNER TO answeror;

--
-- Name: broadcast(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION broadcast() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    insert into notice (user_id, change_id, email)
        select w0.user_id, NEW.id, w0.email_text
        from activated_watch w0
        where w0.query_id = NEW.query_id and w0.ctime <= NEW.ctime;
    return NEW;
end;
$$;


ALTER FUNCTION public.broadcast() OWNER TO answeror;

--
-- Name: check_main_email(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION check_main_email() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare
    main_email text;
begin
    select email into strict main_email from "user" where id = OLD.user_id;
    if (OLD.text = main_email) then
        raise exception 'cannot delete main email of %', OLD.user_id;
    end if;
    return OLD;
end;
$$;


ALTER FUNCTION public.check_main_email() OWNER TO answeror;

--
-- Name: check_maxemail(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION check_maxemail() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.check_maxemail() OWNER TO answeror;

--
-- Name: check_maxwatch(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION check_maxwatch() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.check_maxwatch() OWNER TO answeror;

--
-- Name: fill_watch_email(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION fill_watch_email() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if (NEW.email_id is null) then
        select id into strict NEW.email_id from email where user_id = NEW.user_id;
        if (NEW.email_id is null) then
            raise exception 'no default email found for user %', NEW.user_id;
        end if;
    end if;
    return NEW;
end;
$$;


ALTER FUNCTION public.fill_watch_email() OWNER TO answeror;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: query; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE query (
    id integer NOT NULL,
    kind text NOT NULL,
    text text NOT NULL,
    result json DEFAULT '{}'::json NOT NULL,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    mtime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    next_sync_time timestamp without time zone
);


ALTER TABLE public.query OWNER TO answeror;

--
-- Name: get_or_add_query_bi_kind_and_text(text, text); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION get_or_add_query_bi_kind_and_text(kind text, text text) RETURNS SETOF query
    LANGUAGE plpgsql
    AS $_$
    begin
        insert into query (kind, text)
        select $1, $2
        where not exists (
            select 1 from query as q
            where q.kind = $1 and q.text = $2
        );
        return query select * from query as q where q.kind = $1 and q.text = $2;
    end
$_$;


ALTER FUNCTION public.get_or_add_query_bi_kind_and_text(kind text, text text) OWNER TO answeror;

--
-- Name: update_main_email(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION update_main_email() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if (OLD.text != NEW.text or OLD.activated != NEW.activated) then
        update "user"
        set email = NEW.text, activated = NEW.activated
        where email = OLD.text;
    end if;
    return NEW;
end;
$$;


ALTER FUNCTION public.update_main_email() OWNER TO answeror;

--
-- Name: update_query_mtime(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION update_query_mtime() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    NEW.mtime = (now() at time zone 'utc');
    return NEW;
end;
$$;


ALTER FUNCTION public.update_query_mtime() OWNER TO answeror;

--
-- Name: update_user_email(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION update_user_email() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if (OLD.email != NEW.email or OLD.activated != NEW.activated) then
        update email
        set text = NEW.email, activated = NEW.activated
        where text = OLD.email;
    end if;
    return NEW;
end;
$$;


ALTER FUNCTION public.update_user_email() OWNER TO answeror;

--
-- Name: email; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE email (
    id integer NOT NULL,
    text text NOT NULL,
    label text,
    activated boolean DEFAULT false NOT NULL,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    user_id integer
);


ALTER TABLE public.email OWNER TO answeror;

--
-- Name: watch; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE watch (
    user_id integer,
    query_id integer NOT NULL,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    name text,
    email_id integer NOT NULL
);


ALTER TABLE public.watch OWNER TO answeror;

--
-- Name: activated_watch; Type: VIEW; Schema: public; Owner: answeror
--

CREATE VIEW activated_watch AS
 SELECT w0.user_id,
    w0.query_id,
    w0.ctime,
    w0.name,
    w0.email_id,
    e0.text AS email_text
   FROM (watch w0
     JOIN email e0 ON ((w0.email_id = e0.id)))
  WHERE (e0.activated = true);


ALTER TABLE public.activated_watch OWNER TO answeror;

--
-- Name: change; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE change (
    id integer NOT NULL,
    query_id integer,
    data json DEFAULT '{}'::json NOT NULL,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    hash text
);


ALTER TABLE public.change OWNER TO answeror;

--
-- Name: change_id_seq; Type: SEQUENCE; Schema: public; Owner: answeror
--

CREATE SEQUENCE change_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.change_id_seq OWNER TO answeror;

--
-- Name: change_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: answeror
--

ALTER SEQUENCE change_id_seq OWNED BY change.id;


--
-- Name: email_id_seq; Type: SEQUENCE; Schema: public; Owner: answeror
--

CREATE SEQUENCE email_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.email_id_seq OWNER TO answeror;

--
-- Name: email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: answeror
--

ALTER SEQUENCE email_id_seq OWNED BY email.id;


--
-- Name: notice; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE notice (
    id integer NOT NULL,
    user_id integer,
    change_id integer,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    status notice_status DEFAULT 'pending'::notice_status,
    email text NOT NULL
);


ALTER TABLE public.notice OWNER TO answeror;

--
-- Name: notice_id_seq; Type: SEQUENCE; Schema: public; Owner: answeror
--

CREATE SEQUENCE notice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notice_id_seq OWNER TO answeror;

--
-- Name: notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: answeror
--

ALTER SEQUENCE notice_id_seq OWNED BY notice.id;


--
-- Name: query_id_seq; Type: SEQUENCE; Schema: public; Owner: answeror
--

CREATE SEQUENCE query_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.query_id_seq OWNER TO answeror;

--
-- Name: query_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: answeror
--

ALTER SEQUENCE query_id_seq OWNED BY query.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE "user" (
    id integer NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    openid text NOT NULL,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    maxwatch integer DEFAULT 42 NOT NULL,
    activated boolean DEFAULT false,
    maxemail integer DEFAULT 3,
    CONSTRAINT user_maxemail_check CHECK ((maxemail > 0))
);


ALTER TABLE public."user" OWNER TO answeror;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: answeror
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO answeror;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: answeror
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY change ALTER COLUMN id SET DEFAULT nextval('change_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY email ALTER COLUMN id SET DEFAULT nextval('email_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY notice ALTER COLUMN id SET DEFAULT nextval('notice_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY query ALTER COLUMN id SET DEFAULT nextval('query_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: change_pkey; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY change
    ADD CONSTRAINT change_pkey PRIMARY KEY (id);


--
-- Name: email_pkey; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY email
    ADD CONSTRAINT email_pkey PRIMARY KEY (id);


--
-- Name: email_text_key; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY email
    ADD CONSTRAINT email_text_key UNIQUE (text);


--
-- Name: notice_pkey; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY notice
    ADD CONSTRAINT notice_pkey PRIMARY KEY (id);


--
-- Name: query_kind_text_key; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY query
    ADD CONSTRAINT query_kind_text_key UNIQUE (kind, text);


--
-- Name: query_pkey; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY query
    ADD CONSTRAINT query_pkey PRIMARY KEY (id);


--
-- Name: user_email_key; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_name_key; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_name_key UNIQUE (name);


--
-- Name: user_openid_key; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_openid_key UNIQUE (openid);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: watch_pkey; Type: CONSTRAINT; Schema: public; Owner: answeror; Tablespace: 
--

ALTER TABLE ONLY watch
    ADD CONSTRAINT watch_pkey PRIMARY KEY (email_id, query_id);


--
-- Name: idx_change_ctime; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_change_ctime ON change USING btree (ctime);


--
-- Name: idx_change_hash; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_change_hash ON change USING btree (hash);


--
-- Name: idx_email_id_activated; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_email_id_activated ON email USING btree (id, activated);


--
-- Name: idx_email_text; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_email_text ON email USING btree (text);


--
-- Name: idx_email_user_id; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_email_user_id ON email USING btree (user_id);


--
-- Name: idx_notice_mix; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_notice_mix ON notice USING btree (user_id, status, change_id, ctime);


--
-- Name: idx_query_ctime; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_query_ctime ON query USING btree (ctime);


--
-- Name: idx_query_kind_text; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_query_kind_text ON query USING btree (kind, text);


--
-- Name: idx_query_next_sync_time; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_query_next_sync_time ON query USING btree (next_sync_time);


--
-- Name: idx_user_openid; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_user_openid ON "user" USING btree (openid);


--
-- Name: idx_watch_user_id_ctime; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_watch_user_id_ctime ON watch USING btree (user_id, ctime);


--
-- Name: idx_watch_user_id_query_id; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_watch_user_id_query_id ON watch USING btree (user_id, query_id);


--
-- Name: add_main_email_on_create_user; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER add_main_email_on_create_user AFTER INSERT ON "user" FOR EACH ROW EXECUTE PROCEDURE add_main_email_on_create_user();


--
-- Name: check_main_email; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER check_main_email BEFORE DELETE ON email FOR EACH ROW EXECUTE PROCEDURE check_main_email();


--
-- Name: check_maxemail; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER check_maxemail BEFORE INSERT ON email FOR EACH ROW EXECUTE PROCEDURE check_maxemail();


--
-- Name: check_maxwatch; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER check_maxwatch BEFORE INSERT ON watch FOR EACH ROW EXECUTE PROCEDURE check_maxwatch();


--
-- Name: fill_watch_email; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER fill_watch_email BEFORE INSERT ON watch FOR EACH ROW EXECUTE PROCEDURE fill_watch_email();


--
-- Name: insert_broadcast; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER insert_broadcast AFTER INSERT ON change FOR EACH ROW EXECUTE PROCEDURE broadcast();


--
-- Name: update_main_email; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER update_main_email AFTER UPDATE OF text, activated ON email FOR EACH ROW EXECUTE PROCEDURE update_main_email();


--
-- Name: update_query_mtime; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER update_query_mtime BEFORE UPDATE OF result ON query FOR EACH ROW EXECUTE PROCEDURE update_query_mtime();


--
-- Name: update_user_email; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER update_user_email AFTER UPDATE OF email, activated ON "user" FOR EACH ROW EXECUTE PROCEDURE update_user_email();


--
-- Name: change_query_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY change
    ADD CONSTRAINT change_query_id_fkey FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE;


--
-- Name: email_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY email
    ADD CONSTRAINT email_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE;


--
-- Name: notice_change_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY notice
    ADD CONSTRAINT notice_change_id_fkey FOREIGN KEY (change_id) REFERENCES change(id) ON DELETE CASCADE;


--
-- Name: notice_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY notice
    ADD CONSTRAINT notice_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE;


--
-- Name: watch_email_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY watch
    ADD CONSTRAINT watch_email_id_fkey FOREIGN KEY (email_id) REFERENCES email(id) ON DELETE CASCADE;


--
-- Name: watch_query_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY watch
    ADD CONSTRAINT watch_query_id_fkey FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE;


--
-- Name: watch_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY watch
    ADD CONSTRAINT watch_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE;
