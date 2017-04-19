CREATE TABLE pres_vote
(
    fips INT
    ,election INT
    ,candidate TEXT
    ,party TEXT
    ,vote INT
);

--Copies data to table - use your own path here

COPY pres_vote FROM 'C:\Projects\presidential-vote-by-county\data\county\2000-2016-presidential-vote-by-county.csv' DELIMITER ',' CSV;