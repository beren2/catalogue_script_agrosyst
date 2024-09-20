CREATE TABLE entrepot_commune AS
select 
refl.topiaid id,
refl.codeinsee,
refl.commune ,
refl.petiteregionagricolecode ,
refl.petiteregionagricolenom ,
refl.departement ,
refl.codepostal ,
refl.region ,
refl.latitude ,
refl.longitude ,
refp.frenchname nom_francais
from reflocation refl 
join refcountry refp on refl.refcountry = refp.topiaid 
where refl.active = true;

alter table entrepot_commune
add constraint entrepot_commune_PK
PRIMARY KEY (id);

