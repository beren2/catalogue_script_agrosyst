select 
	es.id as semence_id, 
	es.inoculation_biologique,
	es.traitement_chimique,
	es.bio,
	es.traitement_semence_id,
	es.espece_id,
	es.type_semence,
	es.prix_saisi,
	es.prix_saisi_unite,
	es.prix_ref,
	es.prix_ref_unite,
	es.lot_semence_id
from entrepot_semence es;