CREATE TABLE entrepot_liaison_reseaux AS
select distinct
	np.network as reseau_id,
	np.parents as reseau_parent_id
from network_parents np;
