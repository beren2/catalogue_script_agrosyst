CREATE TABLE entrepot_nuisible_edi AS
select 
r.topiaid as id, 
r.reference_param as categorie_nuisible,
r.reference_label as label_nuisible,
r."source" 
from refnuisibleedi r 
where active is true;

alter table entrepot_nuisible_edi
add constraint nuisible_edi_PK
PRIMARY KEY (id);
