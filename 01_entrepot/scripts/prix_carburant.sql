CREATE TABLE entrepot_prix_carburant AS
select
r.topiaid as id,
r.campaign as campagne,
r.price as prix,
r.unit as unite,
r."source" 
from refprixcarbu r
where active is true; -- les lignes ou les scenarios sont mentionnées ne sont pas retires puisque pas de valeurs sinon

alter table entrepot_prix_carburant
add constraint prix_carburant_pk
PRIMARY KEY (id);
