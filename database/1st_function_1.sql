CREATE OR REPLACE FUNCTION select_by_json(input_dict json)

RETURNS void AS $$



BEGIN



    CREATE TEMPORARY TABLE temp_json (

        id serial NOT NULL PRIMARY KEY,

        info json NOT NULL

    );



    INSERT INTO temp_json (info)

    VALUES (input_dict);



    EXECUTE 'CREATE TABLE districts AS

             SELECT new_id, continent, country, city, geom

             FROM census_data

             WHERE census_data.continent IN (SELECT json_array_elements_text(info->''continent'') FROM temp_json);';



    EXECUTE 'CREATE TABLE countries AS

             SELECT

                continent, country,

                ST_SetSRID(ST_Multi(ST_Union(geom)), 4326) AS geom,

                ST_AsText(ST_Centroid(ST_SetSRID(ST_Multi(ST_Union(geom)), 4326))) AS centroid

             FROM districts

             GROUP BY continent, country;';



    EXECUTE 'CREATE TABLE continents AS

             SELECT

                continent,

                ST_SetSRID(ST_Multi(ST_Union(geom)), 4326) AS geom,

                ST_AsText(ST_Centroid(ST_SetSRID(ST_Multi(ST_Union(geom)), 4326))) AS centroid

             FROM countries

             GROUP BY continent;';



    ALTER TABLE districts ADD PRIMARY KEY (new_id);

    ALTER TABLE countries ADD PRIMARY KEY (country);

    ALTER TABLE continents ADD PRIMARY KEY (continent);



    DROP TABLE temp_json;



END;



$$ LANGUAGE plpgsql;



DROP TABLE if EXISTS districts;

DROP TABLE if EXISTS countries;

DROP TABLE if EXISTS continents;



-- Call the function with multiple continents in the input JSON array

SELECT * FROM select_by_json('{"continent": [