CREATE TABLE entrepot_liaison_sdc_reseau AS
select 
	gn.growingsystem as sdc_id,
	gn.networks as reseau_id
from growingsystem_networks gn;
