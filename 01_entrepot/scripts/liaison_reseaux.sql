CREATE TABLE entrepot_liaison_reseaux AS
select distinct
	np.network as reseau_id,
	np.parents as reseau_parent_id
from network_parents np;

alter table entrepot_liaison_reseaux
add constraint liaison_reseaux_PK
PRIMARY KEY (reseau_id,reseau_parent_id);