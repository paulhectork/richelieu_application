--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

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

DROP DATABASE IF EXISTS "richelieu_db";
--
-- Name: richelieu_db; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE "richelieu_db" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'fr_FR.UTF-8';


\connect "richelieu_db"

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

SET default_tablespace = '';

SET default_table_access_method = "heap";

--
-- Name: actor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."actor" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL
);


--
-- Name: actor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."actor_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."actor_id_seq" OWNED BY "public"."actor"."id";


--
-- Name: address; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."address" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "address" "text" NOT NULL,
    "city" "text" NOT NULL,
    "country" "text" NOT NULL,
    "source" "text" NOT NULL,
    "date" "int4range" NOT NULL
);


--
-- Name: address_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."address_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."address_id_seq" OWNED BY "public"."address"."id";


--
-- Name: admin_person; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."admin_person" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "first_name" "text" NOT NULL,
    "last_name" "text" NOT NULL,
    "id_persistent" "text"
);


--
-- Name: admin_person_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."admin_person_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: admin_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."admin_person_id_seq" OWNED BY "public"."admin_person"."id";


--
-- Name: annotation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."annotation" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "content" "json" NOT NULL,
    "id_iconography" integer NOT NULL
);


--
-- Name: annotation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."annotation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: annotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."annotation_id_seq" OWNED BY "public"."annotation"."id";


--
-- Name: cartography; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."cartography" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "source_url" "text",
    "title" "text",
    "date_source" "text",
    "inventory_number" "text",
    "date" "int4range",
    "vector" "json" NOT NULL,
    "crs_epsg" integer NOT NULL,
    "granularity" "text" NOT NULL,
    "map_source" "text" NOT NULL,
    "id_licence" integer NOT NULL
);


--
-- Name: cartography_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."cartography_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cartography_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."cartography_id_seq" OWNED BY "public"."cartography"."id";


--
-- Name: directory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."directory" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "gallica_ark" "text" NOT NULL,
    "gallica_page" "text" NOT NULL,
    "gallica_row" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "occupation" "text" NOT NULL,
    "date" "int4range" NOT NULL,
    "tags" "text"[],
    "id_address" integer NOT NULL,
    "id_licence" integer NOT NULL
);


--
-- Name: directory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."directory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: directory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."directory_id_seq" OWNED BY "public"."directory"."id";


--
-- Name: filename; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."filename" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "url" "text" NOT NULL,
    "latlngbounds" double precision[],
    "id_licence" integer,
    "id_iconography" integer,
    "id_cartography" integer
);


--
-- Name: filename_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."filename_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: filename_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."filename_id_seq" OWNED BY "public"."filename"."id";


--
-- Name: iconography; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."iconography" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_richelieu" "text" NOT NULL,
    "iiif_url" "text",
    "iiif_folio" integer[],
    "source_url" "text",
    "date_source" "text",
    "date_corr" "text",
    "date" "int4range",
    "technique" "text"[],
    "description" "text",
    "inscription" "text",
    "corpus" "text",
    "inventory_number" "text",
    "produced" boolean,
    "represents" boolean,
    "id_licence" integer NOT NULL
);


--
-- Name: iconography_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."iconography_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: iconography_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."iconography_id_seq" OWNED BY "public"."iconography"."id";


--
-- Name: institution; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."institution" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "description" "text"
);


--
-- Name: institution_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."institution_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: institution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."institution_id_seq" OWNED BY "public"."institution"."id";


--
-- Name: licence; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."licence" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "description" "text"
);


--
-- Name: licence_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."licence_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: licence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."licence_id_seq" OWNED BY "public"."licence"."id";


--
-- Name: named_entity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."named_entity" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "description" "text",
    "category" "text" NOT NULL,
    "category_slug" "text"
);


--
-- Name: named_entity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."named_entity_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: named_entity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."named_entity_id_seq" OWNED BY "public"."named_entity"."id";


--
-- Name: place; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."place" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_richelieu" "text" NOT NULL,
    "date" "int4range" NOT NULL,
    "centroid" "json",
    "vector" "json",
    "vector_source" "text" NOT NULL,
    "crs_epsg" integer NOT NULL,
    "id_place_group" integer
);


--
-- Name: place_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."place_group" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "description" "text"
);


--
-- Name: place_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."place_group_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: place_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."place_group_id_seq" OWNED BY "public"."place_group"."id";


--
-- Name: place_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."place_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."place_id_seq" OWNED BY "public"."place"."id";


--
-- Name: r_address_place; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_address_place" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_address" integer NOT NULL,
    "id_place" integer NOT NULL
);


--
-- Name: r_address_place_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_address_place_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_address_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_address_place_id_seq" OWNED BY "public"."r_address_place"."id";


--
-- Name: r_admin_person; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_admin_person" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_iconography" integer,
    "id_cartography" integer,
    "id_directory" integer,
    "id_admin_person" integer NOT NULL
);


--
-- Name: r_admin_person_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_admin_person_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_admin_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_admin_person_id_seq" OWNED BY "public"."r_admin_person"."id";


--
-- Name: r_cartography_place; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_cartography_place" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_cartography" integer NOT NULL,
    "id_place" integer NOT NULL
);


--
-- Name: r_cartography_place_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_cartography_place_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_cartography_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_cartography_place_id_seq" OWNED BY "public"."r_cartography_place"."id";


--
-- Name: r_iconography_actor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_iconography_actor" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_iconography" integer NOT NULL,
    "id_actor" integer NOT NULL,
    "role" "text" NOT NULL,
    "ismain" boolean NOT NULL
);


--
-- Name: r_iconography_actor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_iconography_actor_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_iconography_actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_iconography_actor_id_seq" OWNED BY "public"."r_iconography_actor"."id";


--
-- Name: r_iconography_named_entity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_iconography_named_entity" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_iconography" integer NOT NULL,
    "id_named_entity" integer NOT NULL
);


--
-- Name: r_iconography_named_entity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_iconography_named_entity_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_iconography_named_entity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_iconography_named_entity_id_seq" OWNED BY "public"."r_iconography_named_entity"."id";


--
-- Name: r_iconography_place; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_iconography_place" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_iconography" integer NOT NULL,
    "id_place" integer NOT NULL
);


--
-- Name: r_iconography_place_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_iconography_place_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_iconography_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_iconography_place_id_seq" OWNED BY "public"."r_iconography_place"."id";


--
-- Name: r_iconography_theme; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_iconography_theme" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_iconography" integer NOT NULL,
    "id_theme" integer NOT NULL
);


--
-- Name: r_iconography_theme_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_iconography_theme_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_iconography_theme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_iconography_theme_id_seq" OWNED BY "public"."r_iconography_theme"."id";


--
-- Name: r_institution; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."r_institution" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "id_iconography" integer,
    "id_cartography" integer,
    "id_directory" integer,
    "id_institution" integer NOT NULL
);


--
-- Name: r_institution_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."r_institution_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: r_institution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."r_institution_id_seq" OWNED BY "public"."r_institution"."id";


--
-- Name: theme; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."theme" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "description" "text",
    "category" "text" NOT NULL,
    "category_slug" "text"
);


--
-- Name: theme_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."theme_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: theme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."theme_id_seq" OWNED BY "public"."theme"."id";


--
-- Name: title; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."title" (
    "id" integer NOT NULL,
    "id_uuid" "text" NOT NULL,
    "entry_name" "text" NOT NULL,
    "ismain" boolean NOT NULL,
    "id_iconography" integer NOT NULL
);


--
-- Name: title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."title_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."title_id_seq" OWNED BY "public"."title"."id";


--
-- Name: actor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."actor" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."actor_id_seq"'::"regclass");


--
-- Name: address id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."address" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."address_id_seq"'::"regclass");


--
-- Name: admin_person id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."admin_person" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."admin_person_id_seq"'::"regclass");


--
-- Name: annotation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."annotation" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."annotation_id_seq"'::"regclass");


--
-- Name: cartography id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cartography" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."cartography_id_seq"'::"regclass");


--
-- Name: directory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."directory" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."directory_id_seq"'::"regclass");


--
-- Name: filename id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."filename" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."filename_id_seq"'::"regclass");


--
-- Name: iconography id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."iconography" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."iconography_id_seq"'::"regclass");


--
-- Name: institution id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."institution" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."institution_id_seq"'::"regclass");


--
-- Name: licence id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."licence" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."licence_id_seq"'::"regclass");


--
-- Name: named_entity id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."named_entity" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."named_entity_id_seq"'::"regclass");


--
-- Name: place id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."place" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."place_id_seq"'::"regclass");


--
-- Name: place_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."place_group" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."place_group_id_seq"'::"regclass");


--
-- Name: r_address_place id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_address_place" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_address_place_id_seq"'::"regclass");


--
-- Name: r_admin_person id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_admin_person" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_admin_person_id_seq"'::"regclass");


--
-- Name: r_cartography_place id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_cartography_place" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_cartography_place_id_seq"'::"regclass");


--
-- Name: r_iconography_actor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_actor" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_iconography_actor_id_seq"'::"regclass");


--
-- Name: r_iconography_named_entity id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_named_entity" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_iconography_named_entity_id_seq"'::"regclass");


--
-- Name: r_iconography_place id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_place" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_iconography_place_id_seq"'::"regclass");


--
-- Name: r_iconography_theme id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_theme" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_iconography_theme_id_seq"'::"regclass");


--
-- Name: r_institution id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_institution" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."r_institution_id_seq"'::"regclass");


--
-- Name: theme id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."theme" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."theme_id_seq"'::"regclass");


--
-- Name: title id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."title" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."title_id_seq"'::"regclass");


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."actor"
    ADD CONSTRAINT "actor_pkey" PRIMARY KEY ("id");


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."address"
    ADD CONSTRAINT "address_pkey" PRIMARY KEY ("id");


--
-- Name: admin_person admin_person_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."admin_person"
    ADD CONSTRAINT "admin_person_pkey" PRIMARY KEY ("id");


--
-- Name: annotation annotation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."annotation"
    ADD CONSTRAINT "annotation_pkey" PRIMARY KEY ("id");


--
-- Name: cartography cartography_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cartography"
    ADD CONSTRAINT "cartography_pkey" PRIMARY KEY ("id");


--
-- Name: directory directory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."directory"
    ADD CONSTRAINT "directory_pkey" PRIMARY KEY ("id");


--
-- Name: filename filename_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."filename"
    ADD CONSTRAINT "filename_pkey" PRIMARY KEY ("id");


--
-- Name: iconography iconography_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."iconography"
    ADD CONSTRAINT "iconography_pkey" PRIMARY KEY ("id");


--
-- Name: institution institution_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."institution"
    ADD CONSTRAINT "institution_pkey" PRIMARY KEY ("id");


--
-- Name: licence licence_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."licence"
    ADD CONSTRAINT "licence_pkey" PRIMARY KEY ("id");


--
-- Name: named_entity named_entity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."named_entity"
    ADD CONSTRAINT "named_entity_pkey" PRIMARY KEY ("id");


--
-- Name: place_group place_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."place_group"
    ADD CONSTRAINT "place_group_pkey" PRIMARY KEY ("id");


--
-- Name: place place_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."place"
    ADD CONSTRAINT "place_pkey" PRIMARY KEY ("id");


--
-- Name: r_address_place r_address_place_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_address_place"
    ADD CONSTRAINT "r_address_place_pkey" PRIMARY KEY ("id");


--
-- Name: r_admin_person r_admin_person_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_admin_person"
    ADD CONSTRAINT "r_admin_person_pkey" PRIMARY KEY ("id");


--
-- Name: r_cartography_place r_cartography_place_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_cartography_place"
    ADD CONSTRAINT "r_cartography_place_pkey" PRIMARY KEY ("id");


--
-- Name: r_iconography_actor r_iconography_actor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_actor"
    ADD CONSTRAINT "r_iconography_actor_pkey" PRIMARY KEY ("id");


--
-- Name: r_iconography_named_entity r_iconography_named_entity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_named_entity"
    ADD CONSTRAINT "r_iconography_named_entity_pkey" PRIMARY KEY ("id");


--
-- Name: r_iconography_place r_iconography_place_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_place"
    ADD CONSTRAINT "r_iconography_place_pkey" PRIMARY KEY ("id");


--
-- Name: r_iconography_theme r_iconography_theme_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_theme"
    ADD CONSTRAINT "r_iconography_theme_pkey" PRIMARY KEY ("id");


--
-- Name: r_institution r_institution_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_institution"
    ADD CONSTRAINT "r_institution_pkey" PRIMARY KEY ("id");


--
-- Name: theme theme_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."theme"
    ADD CONSTRAINT "theme_pkey" PRIMARY KEY ("id");


--
-- Name: title title_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."title"
    ADD CONSTRAINT "title_pkey" PRIMARY KEY ("id");


--
-- Name: annotation annotation_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."annotation"
    ADD CONSTRAINT "annotation_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: cartography cartography_id_licence_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cartography"
    ADD CONSTRAINT "cartography_id_licence_fkey" FOREIGN KEY ("id_licence") REFERENCES "public"."licence"("id");


--
-- Name: directory directory_id_address_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."directory"
    ADD CONSTRAINT "directory_id_address_fkey" FOREIGN KEY ("id_address") REFERENCES "public"."address"("id");


--
-- Name: directory directory_id_licence_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."directory"
    ADD CONSTRAINT "directory_id_licence_fkey" FOREIGN KEY ("id_licence") REFERENCES "public"."licence"("id");


--
-- Name: filename filename_id_cartography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."filename"
    ADD CONSTRAINT "filename_id_cartography_fkey" FOREIGN KEY ("id_cartography") REFERENCES "public"."cartography"("id");


--
-- Name: filename filename_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."filename"
    ADD CONSTRAINT "filename_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: filename filename_id_licence_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."filename"
    ADD CONSTRAINT "filename_id_licence_fkey" FOREIGN KEY ("id_licence") REFERENCES "public"."licence"("id");


--
-- Name: iconography iconography_id_licence_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."iconography"
    ADD CONSTRAINT "iconography_id_licence_fkey" FOREIGN KEY ("id_licence") REFERENCES "public"."licence"("id");


--
-- Name: place place_id_place_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."place"
    ADD CONSTRAINT "place_id_place_group_fkey" FOREIGN KEY ("id_place_group") REFERENCES "public"."place_group"("id");


--
-- Name: r_address_place r_address_place_id_address_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_address_place"
    ADD CONSTRAINT "r_address_place_id_address_fkey" FOREIGN KEY ("id_address") REFERENCES "public"."address"("id");


--
-- Name: r_address_place r_address_place_id_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_address_place"
    ADD CONSTRAINT "r_address_place_id_place_fkey" FOREIGN KEY ("id_place") REFERENCES "public"."place"("id");


--
-- Name: r_admin_person r_admin_person_id_admin_person_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_admin_person"
    ADD CONSTRAINT "r_admin_person_id_admin_person_fkey" FOREIGN KEY ("id_admin_person") REFERENCES "public"."admin_person"("id");


--
-- Name: r_admin_person r_admin_person_id_cartography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_admin_person"
    ADD CONSTRAINT "r_admin_person_id_cartography_fkey" FOREIGN KEY ("id_cartography") REFERENCES "public"."cartography"("id");


--
-- Name: r_admin_person r_admin_person_id_directory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_admin_person"
    ADD CONSTRAINT "r_admin_person_id_directory_fkey" FOREIGN KEY ("id_directory") REFERENCES "public"."directory"("id");


--
-- Name: r_admin_person r_admin_person_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_admin_person"
    ADD CONSTRAINT "r_admin_person_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: r_cartography_place r_cartography_place_id_cartography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_cartography_place"
    ADD CONSTRAINT "r_cartography_place_id_cartography_fkey" FOREIGN KEY ("id_cartography") REFERENCES "public"."cartography"("id");


--
-- Name: r_cartography_place r_cartography_place_id_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_cartography_place"
    ADD CONSTRAINT "r_cartography_place_id_place_fkey" FOREIGN KEY ("id_place") REFERENCES "public"."place"("id");


--
-- Name: r_iconography_actor r_iconography_actor_id_actor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_actor"
    ADD CONSTRAINT "r_iconography_actor_id_actor_fkey" FOREIGN KEY ("id_actor") REFERENCES "public"."actor"("id");


--
-- Name: r_iconography_actor r_iconography_actor_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_actor"
    ADD CONSTRAINT "r_iconography_actor_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: r_iconography_named_entity r_iconography_named_entity_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_named_entity"
    ADD CONSTRAINT "r_iconography_named_entity_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: r_iconography_named_entity r_iconography_named_entity_id_named_entity_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_named_entity"
    ADD CONSTRAINT "r_iconography_named_entity_id_named_entity_fkey" FOREIGN KEY ("id_named_entity") REFERENCES "public"."named_entity"("id");


--
-- Name: r_iconography_place r_iconography_place_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_place"
    ADD CONSTRAINT "r_iconography_place_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: r_iconography_place r_iconography_place_id_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_place"
    ADD CONSTRAINT "r_iconography_place_id_place_fkey" FOREIGN KEY ("id_place") REFERENCES "public"."place"("id");


--
-- Name: r_iconography_theme r_iconography_theme_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_theme"
    ADD CONSTRAINT "r_iconography_theme_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: r_iconography_theme r_iconography_theme_id_theme_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_iconography_theme"
    ADD CONSTRAINT "r_iconography_theme_id_theme_fkey" FOREIGN KEY ("id_theme") REFERENCES "public"."theme"("id");


--
-- Name: r_institution r_institution_id_cartography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_institution"
    ADD CONSTRAINT "r_institution_id_cartography_fkey" FOREIGN KEY ("id_cartography") REFERENCES "public"."cartography"("id");


--
-- Name: r_institution r_institution_id_directory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_institution"
    ADD CONSTRAINT "r_institution_id_directory_fkey" FOREIGN KEY ("id_directory") REFERENCES "public"."directory"("id");


--
-- Name: r_institution r_institution_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_institution"
    ADD CONSTRAINT "r_institution_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: r_institution r_institution_id_institution_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."r_institution"
    ADD CONSTRAINT "r_institution_id_institution_fkey" FOREIGN KEY ("id_institution") REFERENCES "public"."institution"("id");


--
-- Name: title title_id_iconography_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."title"
    ADD CONSTRAINT "title_id_iconography_fkey" FOREIGN KEY ("id_iconography") REFERENCES "public"."iconography"("id");


--
-- Name: SCHEMA "public"; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA "public" TO "richelieu_dbapi";


--
-- PostgreSQL database dump complete
--

