--
-- PostgreSQL database cluster dump
--

-- Started on 2020-11-02 02:13:54 UTC

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgredoc;
ALTER ROLE postgredoc WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md5fc0f9f22ff385651df41da948121475b';






--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Debian 12.3-1.pgdg100+1)
-- Dumped by pg_dump version 12.2

-- Started on 2020-11-02 02:13:54 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2020-11-02 02:14:01 UTC

--
-- PostgreSQL database dump complete
--

--
-- Database "postgredoc" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Debian 12.3-1.pgdg100+1)
-- Dumped by pg_dump version 12.2

-- Started on 2020-11-02 02:14:01 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3439 (class 1262 OID 16384)
-- Name: postgredoc; Type: DATABASE; Schema: -; Owner: postgredoc
--

CREATE DATABASE postgredoc WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE postgredoc OWNER TO postgredoc;

\connect postgredoc

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


--
-- TOC entry 244 (class 1259 OID 24614)
-- Name: tbl_course; Type: TABLE; Schema: public; Owner: postgredoc
--

-- "hash_val",
-- "filename",
-- "converted_filename",
-- "timestamp",
-- "status",
-- "doc_stat",

CREATE TABLE public.tbl_cv (
    uuid uuid DEFAULT public.gen_random_uuid() NOT NULL,
    hash_val character varying(191) NOT NULL,

    filename text NOT NULL,
    converted_filename text NOT NULL,
    addtime text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    status text NOT NULL,
    doc_stat jsonb NOT NULL
);


ALTER TABLE public.tbl_cv OWNER TO postgredoc;


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Debian 12.3-1.pgdg100+1)
-- Dumped by pg_dump version 12.2

-- Started on 2020-11-02 02:14:06 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2020-11-02 02:14:08 UTC

--
-- PostgreSQL database dump complete
--

-- Completed on 2020-11-02 02:14:08 UTC

--
-- PostgreSQL database cluster dump complete
--

