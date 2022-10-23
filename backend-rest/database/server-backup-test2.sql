--
-- PostgreSQL database cluster dump
--

-- Started on 2022-10-23 10:44:54

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:hmWhdYbGhYw5qUOKK+iSDw==$0YRMrE1nvNHMAHN3q7oZUTCHESbkHWlt+j1YHibnBCw=:N2CT63LQNJLO5TqskDj1MM6g1FjCfrQMFBTRcKXHIlg=';

--
-- User Configurations
--








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

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2022-10-23 10:44:54

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

-- Completed on 2022-10-23 10:44:54

--
-- PostgreSQL database dump complete
--

--
-- Database "RobotRadarAlpha" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2022-10-23 10:44:54

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
-- TOC entry 3389 (class 1262 OID 16399)
-- Name: RobotRadarAlpha; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "RobotRadarAlpha" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';


ALTER DATABASE "RobotRadarAlpha" OWNER TO postgres;

\connect "RobotRadarAlpha"

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
-- TOC entry 855 (class 1247 OID 16428)
-- Name: LogType; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."LogType" AS ENUM (
    'Event',
    'Error'
);


ALTER TYPE public."LogType" OWNER TO postgres;

--
-- TOC entry 843 (class 1247 OID 16401)
-- Name: ObstacleType; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."ObstacleType" AS ENUM (
    'Can',
    'OtherRobot'
);


ALTER TYPE public."ObstacleType" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16406)
-- Name: BoilerPlate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."BoilerPlate" (
    "Id" integer NOT NULL,
    "CreatedAt" timestamp with time zone DEFAULT transaction_timestamp()
);


ALTER TABLE public."BoilerPlate" OWNER TO postgres;

--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE "BoilerPlate"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."BoilerPlate" IS 'This is to have the base columns required for all tables.';


--
-- TOC entry 214 (class 1259 OID 16405)
-- Name: BoilerPlate_Id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."BoilerPlate_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."BoilerPlate_Id_seq" OWNER TO postgres;

--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 214
-- Name: BoilerPlate_Id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."BoilerPlate_Id_seq" OWNED BY public."BoilerPlate"."Id";


--
-- TOC entry 217 (class 1259 OID 16420)
-- Name: Logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Logs" (
    "LogType" public."LogType" NOT NULL,
    "Origin" text,
    "Message" text,
    "StackTrace" text
)
INHERITS (public."BoilerPlate");


ALTER TABLE public."Logs" OWNER TO postgres;

--
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE "Logs"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Logs" IS 'Utility table; store things like event messages and errors.';


--
-- TOC entry 220 (class 1259 OID 16449)
-- Name: Map; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Map" (
)
INHERITS (public."BoilerPlate");
ALTER TABLE ONLY public."Map" ALTER COLUMN "CreatedAt" SET NOT NULL;


ALTER TABLE public."Map" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16435)
-- Name: MapObjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MapObjects" (
    "LocationX" double precision,
    "LocationY" double precision,
    "MapId" integer NOT NULL
)
INHERITS (public."BoilerPlate");


ALTER TABLE public."MapObjects" OWNER TO postgres;

--
-- TOC entry 3393 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE "MapObjects"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."MapObjects" IS 'Includes boilerplate plus LocationX and LocationY columns.  Anything physically represented on the map should inherit from this or a child of this.';


--
-- TOC entry 216 (class 1259 OID 16413)
-- Name: Obstacles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Obstacles" (
    "LocationX" double precision,
    "LocationY" double precision,
    "ObstacleType" public."ObstacleType" NOT NULL
)
INHERITS (public."MapObjects");


ALTER TABLE public."Obstacles" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16440)
-- Name: Robot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Robot" (
    "ServoAngle" double precision
)
INHERITS (public."MapObjects");
ALTER TABLE ONLY public."Robot" ALTER COLUMN "CreatedAt" SET NOT NULL;


ALTER TABLE public."Robot" OWNER TO postgres;

--
-- TOC entry 3394 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE "Robot"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Robot" IS 'Our robot, not the other robot - the other robot is considered an "Obstacle" and has a type dedicated to it.';


--
-- TOC entry 3199 (class 2604 OID 16409)
-- Name: BoilerPlate Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BoilerPlate" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3203 (class 2604 OID 16423)
-- Name: Logs Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3204 (class 2604 OID 16424)
-- Name: Logs CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3209 (class 2604 OID 16452)
-- Name: Map Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3210 (class 2604 OID 16453)
-- Name: Map CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3205 (class 2604 OID 16438)
-- Name: MapObjects Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3206 (class 2604 OID 16439)
-- Name: MapObjects CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3201 (class 2604 OID 16416)
-- Name: Obstacles Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3202 (class 2604 OID 16417)
-- Name: Obstacles CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3207 (class 2604 OID 16443)
-- Name: Robot Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3208 (class 2604 OID 16444)
-- Name: Robot CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3378 (class 0 OID 16406)
-- Dependencies: 215
-- Data for Name: BoilerPlate; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3380 (class 0 OID 16420)
-- Dependencies: 217
-- Data for Name: Logs; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3383 (class 0 OID 16449)
-- Dependencies: 220
-- Data for Name: Map; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3381 (class 0 OID 16435)
-- Dependencies: 218
-- Data for Name: MapObjects; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3379 (class 0 OID 16413)
-- Dependencies: 216
-- Data for Name: Obstacles; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3382 (class 0 OID 16440)
-- Dependencies: 219
-- Data for Name: Robot; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3395 (class 0 OID 0)
-- Dependencies: 214
-- Name: BoilerPlate_Id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."BoilerPlate_Id_seq"', 1, false);


--
-- TOC entry 3212 (class 2606 OID 16412)
-- Name: BoilerPlate BoilerPlate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BoilerPlate"
    ADD CONSTRAINT "BoilerPlate_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3214 (class 2606 OID 16457)
-- Name: BoilerPlate Id_Must_Be_Unique_Boiler; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BoilerPlate"
    ADD CONSTRAINT "Id_Must_Be_Unique_Boiler" UNIQUE ("Id");


--
-- TOC entry 3223 (class 2606 OID 16459)
-- Name: MapObjects Id_Must_Be_Unique_MapObjects; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects"
    ADD CONSTRAINT "Id_Must_Be_Unique_MapObjects" UNIQUE ("Id");


--
-- TOC entry 3216 (class 2606 OID 16461)
-- Name: Obstacles Id_Must_Be_Unique_Obstacles; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Id_Must_Be_Unique_Obstacles" UNIQUE ("Id");


--
-- TOC entry 3227 (class 2606 OID 16463)
-- Name: Robot Id_Must_Be_Unique_Robot; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Id_Must_Be_Unique_Robot" UNIQUE ("Id");


--
-- TOC entry 3221 (class 2606 OID 16426)
-- Name: Logs Logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs"
    ADD CONSTRAINT "Logs_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3225 (class 2606 OID 16448)
-- Name: MapObjects MapObjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects"
    ADD CONSTRAINT "MapObjects_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3232 (class 2606 OID 16455)
-- Name: Map Map_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map"
    ADD CONSTRAINT "Map_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3218 (class 2606 OID 16419)
-- Name: Obstacles Obstacles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Obstacles_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3229 (class 2606 OID 16446)
-- Name: Robot Robot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3219 (class 1259 OID 16469)
-- Name: fki_Obstacle_to_Map_Reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_Obstacle_to_Map_Reference" ON public."Obstacles" USING btree ("MapId");


--
-- TOC entry 3230 (class 1259 OID 16475)
-- Name: fki_Robot_to_Map_Reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_Robot_to_Map_Reference" ON public."Robot" USING btree ("MapId");


--
-- TOC entry 3233 (class 2606 OID 16464)
-- Name: Obstacles Obstacle_to_Map_Reference; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Obstacle_to_Map_Reference" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;


--
-- TOC entry 3234 (class 2606 OID 16470)
-- Name: Robot Robot_to_Map_Reference; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_to_Map_Reference" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;


-- Completed on 2022-10-23 10:44:54

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

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2022-10-23 10:44:54

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
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3316 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


-- Completed on 2022-10-23 10:44:55

--
-- PostgreSQL database dump complete
--

-- Completed on 2022-10-23 10:44:55

--
-- PostgreSQL database cluster dump complete
--

