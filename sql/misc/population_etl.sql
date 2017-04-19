-- Creates temp staging table to population estimate CSV
create temp table population_stage
(
    GEONAME TEXT 
    ,LNTITLE TEXT
    ,GEOID TEXT 
    ,LNNUMBER TEXT
    ,TOT_EST TEXT 
    ,TOT_MOE TEXT
    ,ADU_EST TEXT 
    ,ADU_MOE TEXT
    ,CIT_EST TEXT
    ,CIT_MOE TEXT
    ,CVAP_EST TEXT 
    ,CVAP_MOE TEXT 
);

--Loads CSV to temp table
COPY population_stage FROM 'C:\Projects\presidential-vote-by-county\data\demographics\population2012.csv' DELIMITER ',' CSV;

-- ETL for mo
SELECT * 
FROM population_stage;