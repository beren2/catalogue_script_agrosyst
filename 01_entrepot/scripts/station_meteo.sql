DROP TABLE IF EXISTS entrepot_station_meteo CASCADE;

CREATE TABLE entrepot_station_meteo AS
select 
r.topiaid as id ,
r.codepostal ,
r.communesite ,
r.commune , 
r.site ,
r.pointgps ,
r.affectation ,
r."source" 
from refstationmeteo r 
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_station_meteo
        ADD CONSTRAINT station_meteo_PK
        primary key (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;