PGDMP             
        	    z           RobotRadarAlpha    15.0    15.0 2    :           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ;           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            <           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            =           1262    16399    RobotRadarAlpha    DATABASE     �   CREATE DATABASE "RobotRadarAlpha" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
 !   DROP DATABASE "RobotRadarAlpha";
                postgres    false            W           1247    16428    LogType    TYPE     C   CREATE TYPE public."LogType" AS ENUM (
    'Event',
    'Error'
);
    DROP TYPE public."LogType";
       public          postgres    false            K           1247    16401    ObstacleType    TYPE     K   CREATE TYPE public."ObstacleType" AS ENUM (
    'Can',
    'OtherRobot'
);
 !   DROP TYPE public."ObstacleType";
       public          postgres    false            �            1259    16406    BoilerPlate    TABLE     �   CREATE TABLE public."BoilerPlate" (
    "Id" integer NOT NULL,
    "CreatedAt" timestamp with time zone DEFAULT transaction_timestamp()
);
 !   DROP TABLE public."BoilerPlate";
       public         heap    postgres    false            >           0    0    TABLE "BoilerPlate"    COMMENT     f   COMMENT ON TABLE public."BoilerPlate" IS 'This is to have the base columns required for all tables.';
          public          postgres    false    215            �            1259    16405    BoilerPlate_Id_seq    SEQUENCE     �   CREATE SEQUENCE public."BoilerPlate_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public."BoilerPlate_Id_seq";
       public          postgres    false    215            ?           0    0    BoilerPlate_Id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public."BoilerPlate_Id_seq" OWNED BY public."BoilerPlate"."Id";
          public          postgres    false    214            �            1259    16420    Logs    TABLE     �   CREATE TABLE public."Logs" (
    "LogType" public."LogType" NOT NULL,
    "Origin" text,
    "Message" text,
    "StackTrace" text
)
INHERITS (public."BoilerPlate");
    DROP TABLE public."Logs";
       public         heap    postgres    false    855    215            @           0    0    TABLE "Logs"    COMMENT     a   COMMENT ON TABLE public."Logs" IS 'Utility table; store things like event messages and errors.';
          public          postgres    false    217            �            1259    16449    Map    TABLE     �   CREATE TABLE public."Map" (
)
INHERITS (public."BoilerPlate");
ALTER TABLE ONLY public."Map" ALTER COLUMN "CreatedAt" SET NOT NULL;
    DROP TABLE public."Map";
       public         heap    postgres    false    215            �            1259    16435 
   MapObjects    TABLE     �   CREATE TABLE public."MapObjects" (
    "LocationX" double precision,
    "LocationY" double precision,
    "MapId" integer NOT NULL
)
INHERITS (public."BoilerPlate");
     DROP TABLE public."MapObjects";
       public         heap    postgres    false    215            A           0    0    TABLE "MapObjects"    COMMENT     �   COMMENT ON TABLE public."MapObjects" IS 'Includes boilerplate plus LocationX and LocationY columns.  Anything physically represented on the map should inherit from this or a child of this.';
          public          postgres    false    218            �            1259    16413 	   Obstacles    TABLE     �   CREATE TABLE public."Obstacles" (
    "LocationX" double precision,
    "LocationY" double precision,
    "ObstacleType" public."ObstacleType" NOT NULL
)
INHERITS (public."MapObjects");
    DROP TABLE public."Obstacles";
       public         heap    postgres    false    843    218            �            1259    16440    Robot    TABLE     �   CREATE TABLE public."Robot" (
    "ServoAngle" double precision
)
INHERITS (public."MapObjects");
ALTER TABLE ONLY public."Robot" ALTER COLUMN "CreatedAt" SET NOT NULL;
    DROP TABLE public."Robot";
       public         heap    postgres    false    218            B           0    0    TABLE "Robot"    COMMENT     �   COMMENT ON TABLE public."Robot" IS 'Our robot, not the other robot - the other robot is considered an "Obstacle" and has a type dedicated to it.';
          public          postgres    false    219                       2604    16409    BoilerPlate Id    DEFAULT     v   ALTER TABLE ONLY public."BoilerPlate" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);
 A   ALTER TABLE public."BoilerPlate" ALTER COLUMN "Id" DROP DEFAULT;
       public          postgres    false    215    214    215            �           2604    16423    Logs Id    DEFAULT     o   ALTER TABLE ONLY public."Logs" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);
 :   ALTER TABLE public."Logs" ALTER COLUMN "Id" DROP DEFAULT;
       public          postgres    false    214    217            �           2604    16424    Logs CreatedAt    DEFAULT     ]   ALTER TABLE ONLY public."Logs" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();
 A   ALTER TABLE public."Logs" ALTER COLUMN "CreatedAt" DROP DEFAULT;
       public          postgres    false    217            �           2604    16452    Map Id    DEFAULT     n   ALTER TABLE ONLY public."Map" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);
 9   ALTER TABLE public."Map" ALTER COLUMN "Id" DROP DEFAULT;
       public          postgres    false    220    214            �           2604    16453    Map CreatedAt    DEFAULT     \   ALTER TABLE ONLY public."Map" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();
 @   ALTER TABLE public."Map" ALTER COLUMN "CreatedAt" DROP DEFAULT;
       public          postgres    false    220            �           2604    16438    MapObjects Id    DEFAULT     u   ALTER TABLE ONLY public."MapObjects" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);
 @   ALTER TABLE public."MapObjects" ALTER COLUMN "Id" DROP DEFAULT;
       public          postgres    false    214    218            �           2604    16439    MapObjects CreatedAt    DEFAULT     c   ALTER TABLE ONLY public."MapObjects" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();
 G   ALTER TABLE public."MapObjects" ALTER COLUMN "CreatedAt" DROP DEFAULT;
       public          postgres    false    218            �           2604    16416    Obstacles Id    DEFAULT     t   ALTER TABLE ONLY public."Obstacles" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);
 ?   ALTER TABLE public."Obstacles" ALTER COLUMN "Id" DROP DEFAULT;
       public          postgres    false    216    214            �           2604    16417    Obstacles CreatedAt    DEFAULT     b   ALTER TABLE ONLY public."Obstacles" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();
 F   ALTER TABLE public."Obstacles" ALTER COLUMN "CreatedAt" DROP DEFAULT;
       public          postgres    false    216            �           2604    16443    Robot Id    DEFAULT     p   ALTER TABLE ONLY public."Robot" ALTER COLUMN "Id" SET DEFAULT nextval('public."BoilerPlate_Id_seq"'::regclass);
 ;   ALTER TABLE public."Robot" ALTER COLUMN "Id" DROP DEFAULT;
       public          postgres    false    214    219            �           2604    16444    Robot CreatedAt    DEFAULT     ^   ALTER TABLE ONLY public."Robot" ALTER COLUMN "CreatedAt" SET DEFAULT transaction_timestamp();
 B   ALTER TABLE public."Robot" ALTER COLUMN "CreatedAt" DROP DEFAULT;
       public          postgres    false    219            2          0    16406    BoilerPlate 
   TABLE DATA           :   COPY public."BoilerPlate" ("Id", "CreatedAt") FROM stdin;
    public          postgres    false    215   q9       4          0    16420    Logs 
   TABLE DATA           a   COPY public."Logs" ("Id", "CreatedAt", "LogType", "Origin", "Message", "StackTrace") FROM stdin;
    public          postgres    false    217   �9       7          0    16449    Map 
   TABLE DATA           2   COPY public."Map" ("Id", "CreatedAt") FROM stdin;
    public          postgres    false    220   �9       5          0    16435 
   MapObjects 
   TABLE DATA           \   COPY public."MapObjects" ("Id", "CreatedAt", "LocationX", "LocationY", "MapId") FROM stdin;
    public          postgres    false    218   �9       3          0    16413 	   Obstacles 
   TABLE DATA           k   COPY public."Obstacles" ("Id", "CreatedAt", "LocationX", "LocationY", "MapId", "ObstacleType") FROM stdin;
    public          postgres    false    216   �9       6          0    16440    Robot 
   TABLE DATA           e   COPY public."Robot" ("Id", "CreatedAt", "LocationX", "LocationY", "ServoAngle", "MapId") FROM stdin;
    public          postgres    false    219   :       C           0    0    BoilerPlate_Id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public."BoilerPlate_Id_seq"', 1, false);
          public          postgres    false    214            �           2606    16412    BoilerPlate BoilerPlate_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public."BoilerPlate"
    ADD CONSTRAINT "BoilerPlate_pkey" PRIMARY KEY ("Id");
 J   ALTER TABLE ONLY public."BoilerPlate" DROP CONSTRAINT "BoilerPlate_pkey";
       public            postgres    false    215            �           2606    16457 $   BoilerPlate Id_Must_Be_Unique_Boiler 
   CONSTRAINT     c   ALTER TABLE ONLY public."BoilerPlate"
    ADD CONSTRAINT "Id_Must_Be_Unique_Boiler" UNIQUE ("Id");
 R   ALTER TABLE ONLY public."BoilerPlate" DROP CONSTRAINT "Id_Must_Be_Unique_Boiler";
       public            postgres    false    215            �           2606    16459 '   MapObjects Id_Must_Be_Unique_MapObjects 
   CONSTRAINT     f   ALTER TABLE ONLY public."MapObjects"
    ADD CONSTRAINT "Id_Must_Be_Unique_MapObjects" UNIQUE ("Id");
 U   ALTER TABLE ONLY public."MapObjects" DROP CONSTRAINT "Id_Must_Be_Unique_MapObjects";
       public            postgres    false    218            �           2606    16461 %   Obstacles Id_Must_Be_Unique_Obstacles 
   CONSTRAINT     d   ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Id_Must_Be_Unique_Obstacles" UNIQUE ("Id");
 S   ALTER TABLE ONLY public."Obstacles" DROP CONSTRAINT "Id_Must_Be_Unique_Obstacles";
       public            postgres    false    216            �           2606    16463    Robot Id_Must_Be_Unique_Robot 
   CONSTRAINT     \   ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Id_Must_Be_Unique_Robot" UNIQUE ("Id");
 K   ALTER TABLE ONLY public."Robot" DROP CONSTRAINT "Id_Must_Be_Unique_Robot";
       public            postgres    false    219            �           2606    16426    Logs Logs_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public."Logs"
    ADD CONSTRAINT "Logs_pkey" PRIMARY KEY ("Id");
 <   ALTER TABLE ONLY public."Logs" DROP CONSTRAINT "Logs_pkey";
       public            postgres    false    217            �           2606    16448    MapObjects MapObjects_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public."MapObjects"
    ADD CONSTRAINT "MapObjects_pkey" PRIMARY KEY ("Id");
 H   ALTER TABLE ONLY public."MapObjects" DROP CONSTRAINT "MapObjects_pkey";
       public            postgres    false    218            �           2606    16455    Map Map_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public."Map"
    ADD CONSTRAINT "Map_pkey" PRIMARY KEY ("Id");
 :   ALTER TABLE ONLY public."Map" DROP CONSTRAINT "Map_pkey";
       public            postgres    false    220            �           2606    16419    Obstacles Obstacles_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Obstacles_pkey" PRIMARY KEY ("Id");
 F   ALTER TABLE ONLY public."Obstacles" DROP CONSTRAINT "Obstacles_pkey";
       public            postgres    false    216            �           2606    16446    Robot Robot_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_pkey" PRIMARY KEY ("Id");
 >   ALTER TABLE ONLY public."Robot" DROP CONSTRAINT "Robot_pkey";
       public            postgres    false    219            �           1259    16469    fki_Obstacle_to_Map_Reference    INDEX     Z   CREATE INDEX "fki_Obstacle_to_Map_Reference" ON public."Obstacles" USING btree ("MapId");
 3   DROP INDEX public."fki_Obstacle_to_Map_Reference";
       public            postgres    false    216            �           1259    16475    fki_Robot_to_Map_Reference    INDEX     S   CREATE INDEX "fki_Robot_to_Map_Reference" ON public."Robot" USING btree ("MapId");
 0   DROP INDEX public."fki_Robot_to_Map_Reference";
       public            postgres    false    219            �           2606    16464 #   Obstacles Obstacle_to_Map_Reference    FK CONSTRAINT     �   ALTER TABLE ONLY public."Obstacles"
    ADD CONSTRAINT "Obstacle_to_Map_Reference" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;
 Q   ALTER TABLE ONLY public."Obstacles" DROP CONSTRAINT "Obstacle_to_Map_Reference";
       public          postgres    false    220    3232    216            �           2606    16470    Robot Robot_to_Map_Reference    FK CONSTRAINT     �   ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_to_Map_Reference" FOREIGN KEY ("MapId") REFERENCES public."Map"("Id") NOT VALID;
 J   ALTER TABLE ONLY public."Robot" DROP CONSTRAINT "Robot_to_Map_Reference";
       public          postgres    false    220    3232    219            2      x������ � �      4      x������ � �      7      x������ � �      5      x������ � �      3      x������ � �      6      x������ � �     