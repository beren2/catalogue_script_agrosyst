CREATE TABLE entrepot_zone AS
  select
    z.topiaid id,
    z.code,
    z.name nom,
    p.campagne ,
    z.area surface,
    z.latitude,
    z.longitude,
    z.type as type,
    p.id parcelle_id
  FROM zone z
  JOIN entrepot_parcelle p ON z.plot = p.id
  AND z.active is TRUE;
  
alter table entrepot_zone
ADD CONSTRAINT zone_PK
primary key (id);

alter table entrepot_zone
add FOREIGN KEY (parcelle_id) REFERENCES entrepot_parcelle(id);
