CREATE TABLE IF NOT EXISTS Country (iso3 varchar PRIMARY KEY, iso2 varchar, name varchar, reg_id varchar, ilevel_id varchar, ltype_id varchar, capital varchar, lon varchar, lat varchar);
CREATE TABLE IF NOT EXISTS Region (id varchar PRIMARY KEY, iso2 varchar, value varchar);
CREATE TABLE IF NOT EXISTS LType (id varchar PRIMARY KEY, iso2 varchar, value varchar);
CREATE TABLE IF NOT EXISTS ILevel (id varchar PRIMARY KEY, iso2 varchar, value varchar);
CREATE TABLE IF NOT EXISTS GDPDatapoint (ctry_name varchar, ctry_code varchar, year varchar, value varchar, PRIMARY KEY (ctry_code, year));
