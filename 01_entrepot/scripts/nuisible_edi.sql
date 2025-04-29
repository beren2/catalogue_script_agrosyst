CREATE TABLE entrepot_nuisible_edi AS
select 
r.topiaid as id, 
r.reference_param as categorie_nuisible,
r.reference_label as label_nuisible,
r.reference_id as reference_id,
r."source" 
from refnuisibleedi r;

alter table entrepot_nuisible_edi
add constraint nuisible_edi_PK
PRIMARY KEY (id);
