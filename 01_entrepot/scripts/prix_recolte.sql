CREATE TABLE entrepot_prix_recolte AS
select
r.topiaid as id,
r.code_destination_a, --code_destination_a dans destination_valorisation 
r.code_qualifiant_aee,
r.produitrecolte,
r.organic as bio,
r.marketingperioddecade as decade_de_vente,
r.campaign as campagne,
r.priceunit as prix_unite,
r.price as prix,
r.code_scenario as code_scenario,
r.scenario as scenario, 
r.marketingperiod as mois_de_vente,
r."source",
from refharvestingprice r
where active is true;

alter table entrepot_prix_recolte
add constraint entrepot_prix_recolte_pk
PRIMARY KEY (id);