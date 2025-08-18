CREATE TABLE entrepot_liaison_sdc_reseau AS
select 
	gn.growingsystem as sdc_id,
	gn.networks as reseau_id
from growingsystem_networks gn;

alter table entrepot_liaison_sdc_reseau
add constraint liaison_sdc_reseaux_PK
PRIMARY KEY (sdc_id,reseau_id);