CREATE TABLE fips
(
    fips INT
    ,county TEXT
    ,state TEXT
);

--Copies data to table - use your own path here

COPY fips FROM 'C:\Projects\presidential-vote-by-county\data\geo\fips\fips.csv' DELIMITER ',' CSV;