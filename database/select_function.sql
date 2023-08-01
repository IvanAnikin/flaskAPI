CREATE OR REPLACE FUNCTION select_by_json(input_dict json)

RETURNS void

AS $$

BEGIN

    CREATE TEMPORARY TABLE temp_json (

        id serial NOT NULL PRIMARY KEY,

        info json NOT NULL

    );

    

    INSERT INTO temp_json (info)

    VALUES (input_dict);

    

    EXECUTE 'CREATE TABLE new_table AS

             SELECT *

             FROM combined_table

             WHERE combined_table.continent = (SELECT info ->> ''continent'' FROM temp_json LIMIT 1)

                AND combined_table.country = (SELECT info ->> ''country'' FROM temp_json LIMIT 1)

                AND combined_table.city = (SELECT info ->> ''city'' FROM temp_json LIMIT 1)';

    

    ALTER TABLE new_table ADD PRIMARY KEY (new_id);

    

    DROP TABLE temp_json;

END;

$$ LANGUAGE plpgsql;





DROP TABLE if EXISTS new_table;



SELECT * FROM select_by_json('{"continent": "North America", "country": "USA", "city": "Baltimore"}'::json);

