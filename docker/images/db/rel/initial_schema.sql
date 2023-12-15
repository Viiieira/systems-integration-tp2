CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

-- Country
CREATE TABLE public.Country (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name 			varchar(250) UNIQUE NOT NULL,
)

-- Province
CREATE TABLE public.Province (
	id				uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name			varchar(250)
	coords 			point,
	id_country		uuid NOT NULL,
)

ALTER TABLE Province
	ADD CONSTRAINT provinces_countries_id_fk
		FOREIGN KEY (id_country) REFERENCES Country
			ON DELETE CASCADE;

-- Winery
CREATE TABLE public.Winery (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name 			varchar(250) UNIQUE NOT NULL,
	id_province		uuid NOT NULL,
)

ALTER TABLE Winery
	ADD CONSTRAINT wineries_provinces_id_fk
		FOREIGN KEY (id_province) REFERENCES Province
			ON DELETE CASCADE;

-- Taster
CREATE TABLE public.Taster (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name 			varchar(250) UNIQUE NOT NULL,
	twitter_handle	varchar(250) UNIQUE NOT NULL,
)

CREATE TABLE public.Wine (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name 			varchar(250) UNIQUE NOT NULL,
	points 			INT NOT NULL,
	price 			NUMERIC(10,2) NOT NULL,
	variety			varchar(250) NOT NULL,
	id_province		uuid NOT NULL,
	id_taster		uuid NOT NULL,
	id_winery		uuid NOT NULL,
)

ALTER TABLE Wine
    ADD CONSTRAINT wines_provinces_id_fk
        FOREIGN KEY (id_province) REFERENCES Province
            ON DELETE CASCADE;

ALTER TABLE Wine
	ADD CONSTRAINT wines_tasters_id_fk
		FOREIGN KEY (id_taster) REFERENCES Taster
			ON DELETE CASCADE;

ALTER TABLE Wine
	ADD CONSTRAINT wines_wineries_id_fk
		FOREIGN KEY (id_winery) REFERENCES Winery
			ON DELETE CASCADE;

