CREATE TABLE entrepot_intervention_travail_edi AS
select topiaid id,
reference_code code_reference,
intervention_agrosyst action_type,
reference_label action_label,
"source" ,
active actif
from refinterventionagrosysttravailedi refint  ;

alter table entrepot_intervention_travail_edi
add constraint intervention_travail_edi_PK
PRIMARY KEY (id);
