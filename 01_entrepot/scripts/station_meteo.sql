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

alter table entrepot_station_meteo
ADD CONSTRAINT station_meteo_PK
primary key (id);