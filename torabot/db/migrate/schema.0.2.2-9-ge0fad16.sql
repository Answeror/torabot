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
-- Name: broadcast(); Type: FUNCTION; Schema: public; Owner: answeror
--

CREATE FUNCTION broadcast() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    begin
        insert into notice (user_id, change_id)
            select watch.user_id as user_id, NEW.id as change_id
            from watch
            where watch.query_id = NEW.query_id and watch.ctime <= NEW.ctime;
        return NEW;
    end;
$$;


ALTER FUNCTION public.broadcast() OWNER TO answeror;

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
    mtime timestamp without time zone DEFAULT timezone('utc'::text, now())
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
-- Name: change; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE change (
    id integer NOT NULL,
    query_id integer,
    data json DEFAULT '{}'::json NOT NULL,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now())
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
-- Name: notice; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE notice (
    id integer NOT NULL,
    user_id integer,
    change_id integer,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    status notice_status DEFAULT 'pending'::notice_status
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
    activated boolean DEFAULT true
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
-- Name: watch; Type: TABLE; Schema: public; Owner: answeror; Tablespace: 
--

CREATE TABLE watch (
    user_id integer,
    query_id integer,
    ctime timestamp without time zone DEFAULT timezone('utc'::text, now()),
    name text
);


ALTER TABLE public.watch OWNER TO answeror;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY change ALTER COLUMN id SET DEFAULT nextval('change_id_seq'::regclass);


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
-- Name: idx_user_openid; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_user_openid ON "user" USING btree (openid);


--
-- Name: idx_watch_ctime; Type: INDEX; Schema: public; Owner: answeror; Tablespace: 
--

CREATE INDEX idx_watch_ctime ON watch USING btree (ctime);


--
-- Name: check_maxwatch; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER check_maxwatch BEFORE INSERT ON watch FOR EACH ROW EXECUTE PROCEDURE check_maxwatch();


--
-- Name: insert_broadcast; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER insert_broadcast AFTER INSERT ON change FOR EACH ROW EXECUTE PROCEDURE broadcast();


--
-- Name: update_query_mtime; Type: TRIGGER; Schema: public; Owner: answeror
--

CREATE TRIGGER update_query_mtime BEFORE UPDATE ON query FOR EACH ROW EXECUTE PROCEDURE update_query_mtime();


--
-- Name: change_query_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY change
    ADD CONSTRAINT change_query_id_fkey FOREIGN KEY (query_id) REFERENCES query(id);


--
-- Name: notice_change_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY notice
    ADD CONSTRAINT notice_change_id_fkey FOREIGN KEY (change_id) REFERENCES change(id);


--
-- Name: notice_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY notice
    ADD CONSTRAINT notice_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: watch_query_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY watch
    ADD CONSTRAINT watch_query_id_fkey FOREIGN KEY (query_id) REFERENCES query(id);


--
-- Name: watch_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: answeror
--

ALTER TABLE ONLY watch
    ADD CONSTRAINT watch_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

