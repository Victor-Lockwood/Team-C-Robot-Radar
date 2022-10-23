--
-- PostgreSQL database dump
--

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2022-10-23 13:58:43

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
-- TOC entry 843 (class 1247 OID 24578)
-- Name: LogType; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."LogType" AS ENUM (
    'Event',
    'Error'
);


ALTER TYPE public."LogType" OWNER TO postgres;

--
-- TOC entry 846 (class 1247 OID 24584)
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
-- TOC entry 214 (class 1259 OID 24589)
-- Name: BoilerPlate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."BoilerPlate" (
    "Id" integer NOT NULL,
    "CreatedAt" timestamp with time zone DEFAULT transaction_timestamp()
);


ALTER TABLE public."BoilerPlate" OWNER TO postgres;

--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 214
-- Name: TABLE "BoilerPlate"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."BoilerPlate" IS 'This is to have the base columns required for all tables.';


--
-- TOC entry 215 (class 1259 OID 24593)
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
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 215
-- Name: BoilerPlate_Id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."BoilerPlate_Id_seq" OWNED BY public."BoilerPlate"."Id";


--
-- TOC entry 216 (class 1259 OID 24594)
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
-- TOC entry 3393 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE "Logs"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Logs" IS 'Utility table; store things like event messages and errors.';


--
-- TOC entry 217 (class 1259 OID 24600)
-- Name: Map; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Map" (
)
INHERITS (public."BoilerPlate");
ALTER TABLE ONLY public."Map" ALTER COLUMN "CreatedAt" SET NOT NULL;


ALTER TABLE public."Map" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24604)
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
-- TOC entry 3396 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE "MapObjects"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."MapObjects" IS 'Includes boilerplate plus LocationX and LocationY columns.  Anything physically represented on the map should inherit from this or a child of this.';


--
-- TOC entry 219 (class 1259 OID 24608)
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
-- TOC entry 220 (class 1259 OID 24612)
-- Name: Robot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Robot" (
    "ServoAngle" double precision
)
INHERITS (public."MapObjects");
ALTER TABLE ONLY public."Robot" ALTER COLUMN "CreatedAt" SET NOT NULL;


ALTER TABLE public."Robot" OWNER TO postgres;

--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE "Robot"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Robot" IS 'Our robot, not the other robot - the other robot is considered an "Obstacle" and has a type dedicated to it.';


--
-- TOC entry 3199 (class 2604 OID 24616)
-- Name: BoilerPlate Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BoilerPlate" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3201 (class 2604 OID 24617)
-- Name: Logs Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3202 (class 2604 OID 24618)
-- Name: Logs CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3203 (class 2604 OID 24619)
-- Name: Map Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3204 (class 2604 OID 24620)
-- Name: Map CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3205 (class 2604 OID 24621)
-- Name: MapObjects Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3206 (class 2604 OID 24622)
-- Name: MapObjects CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3207 (class 2604 OID 24623)
-- Name: Obstacles Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3208 (class 2604 OID 24624)
-- Name: Obstacles CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3209 (class 2604 OID 24625)
-- Name: Robot Id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);


--
-- TOC entry 3210 (class 2604 OID 24626)
-- Name: Robot CreatedAt; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();


--
-- TOC entry 3377 (class 0 OID 24589)
-- Dependencies: 214
-- Data for Name: BoilerPlate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."BoilerPlate" ("Id", "CreatedAt") FROM stdin;
\.


--
-- TOC entry 3379 (class 0 OID 24594)
-- Dependencies: 216
-- Data for Name: Logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Logs" ("Id", "CreatedAt", "LogType", "Origin", "Message", "StackTrace") FROM stdin;
\.


--
-- TOC entry 3380 (class 0 OID 24600)
-- Dependencies: 217
-- Data for Name: Map; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Map" ("Id", "CreatedAt") FROM stdin;
1	2022-10-23 13:48:20.072026-04
\.


--
-- TOC entry 3381 (class 0 OID 24604)
-- Dependencies: 218
-- Data for Name: MapObjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."MapObjects" ("Id", "CreatedAt", "LocationX", "LocationY", "MapId") FROM stdin;
\.


--
-- TOC entry 3382 (class 0 OID 24608)
-- Dependencies: 219
-- Data for Name: Obstacles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Obstacles" ("Id", "CreatedAt", "LocationX", "LocationY", "MapId", "ObstacleType") FROM stdin;
\.


--
-- TOC entry 3383 (class 0 OID 24612)
-- Dependencies: 220
-- Data for Name: Robot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Robot" ("Id", "CreatedAt", "LocationX", "LocationY", "MapId", "ServoAngle") FROM stdin;
\.


--
-- TOC entry 3401 (class 0 OID 0)
-- Dependencies: 215
-- Name: BoilerPlate_Id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."BoilerPlate_Id_seq"', 1, true);


--
-- TOC entry 3212 (class 2606 OID 24628)
-- Name: BoilerPlate BoilerPlate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BoilerPlate"
    ADD CONSTRAINT "BoilerPlate_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3214 (class 2606 OID 24630)
-- Name: BoilerPlate Id_Must_Be_Unique_Boiler; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BoilerPlate"
    ADD CONSTRAINT "Id_Must_Be_Unique_Boiler" UNIQUE ("Id");


--
-- TOC entry 3220 (class 2606 OID 24632)
-- Name: MapObjects Id_Must_Be_Unique_MapObjects; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects"
    ADD CONSTRAINT "Id_Must_Be_Unique_MapObjects" UNIQUE ("Id");


--
-- TOC entry 3224 (class 2606 OID 24634)
-- Name: Obstacles Id_Must_Be_Unique_Obstacles; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Id_Must_Be_Unique_Obstacles" UNIQUE ("Id");


--
-- TOC entry 3229 (class 2606 OID 24636)
-- Name: Robot Id_Must_Be_Unique_Robot; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Id_Must_Be_Unique_Robot" UNIQUE ("Id");


--
-- TOC entry 3216 (class 2606 OID 24638)
-- Name: Logs Logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Logs"
    ADD CONSTRAINT "Logs_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3222 (class 2606 OID 24640)
-- Name: MapObjects MapObjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MapObjects"
    ADD CONSTRAINT "MapObjects_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3218 (class 2606 OID 24642)
-- Name: Map Map_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Map"
    ADD CONSTRAINT "Map_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3226 (class 2606 OID 24644)
-- Name: Obstacles Obstacles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Obstacles_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3231 (class 2606 OID 24646)
-- Name: Robot Robot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 3227 (class 1259 OID 24647)
-- Name: fki_Obstacle_to_Map_Reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_Obstacle_to_Map_Reference" ON public."Obstacles" USING btree ("MapId");


--
-- TOC entry 3232 (class 1259 OID 24648)
-- Name: fki_Robot_to_Map_Reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_Robot_to_Map_Reference" ON public."Robot" USING btree ("MapId");


--
-- TOC entry 3233 (class 2606 OID 24649)
-- Name: Obstacles Obstacle_to_Map_Reference; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Obstacle_to_Map_Reference" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;


--
-- TOC entry 3234 (class 2606 OID 24654)
-- Name: Robot Robot_to_Map_Reference; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_to_Map_Reference" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;


--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO flaskuser WITH GRANT OPTION;


--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 214
-- Name: TABLE "BoilerPlate"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."BoilerPlate" TO flaskuser WITH GRANT OPTION;


--
-- TOC entry 3394 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE "Logs"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."Logs" TO flaskuser;


--
-- TOC entry 3395 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE "Map"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."Map" TO flaskuser;


--
-- TOC entry 3397 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE "MapObjects"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."MapObjects" TO flaskuser;


--
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE "Obstacles"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."Obstacles" TO flaskuser;


--
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE "Robot"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public."Robot" TO flaskuser;


-- Completed on 2022-10-23 13:58:43

--
-- PostgreSQL database dump complete
--

