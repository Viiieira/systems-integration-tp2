-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Country
CREATE TABLE public.Country (
    id   uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(250) UNIQUE NOT NULL
);

-- Province
CREATE TABLE public.Province (
    id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        varchar(250),
    latitude    double precision,
    longitude   double precision,
    id_country  uuid NOT NULL,
    
    CONSTRAINT provinces_countries_id_fk
        FOREIGN KEY (id_country) REFERENCES public.Country(id)
        ON DELETE CASCADE
);

-- Winery
CREATE TABLE public.Winery (
    id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        varchar(250) UNIQUE NOT NULL,
    id_province uuid NOT NULL,

    CONSTRAINT wineries_provinces_id_fk
        FOREIGN KEY (id_province) REFERENCES public.Province(id)
        ON DELETE CASCADE
);

-- Taster
CREATE TABLE public.Taster (
    id             uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name           varchar(250) UNIQUE NOT NULL,
    twitter_handle varchar(250) UNIQUE NOT NULL
);

-- Wine
CREATE TABLE public.Wine (
    id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        varchar(250) UNIQUE NOT NULL,
    points      INT NOT NULL,
    price       NUMERIC(10,2) NOT NULL,
    variety     varchar(250) NOT NULL,
    id_province uuid NOT NULL,
    id_taster   uuid NOT NULL,
    id_winery   uuid NOT NULL,

    CONSTRAINT wines_provinces_id_fk
        FOREIGN KEY (id_province) REFERENCES public.Province(id)
        ON DELETE CASCADE,

    CONSTRAINT wines_tasters_id_fk
        FOREIGN KEY (id_taster) REFERENCES public.Taster(id)
        ON DELETE CASCADE,

    CONSTRAINT wines_wineries_id_fk
        FOREIGN KEY (id_winery) REFERENCES public.Winery(id)
        ON DELETE CASCADE
);
