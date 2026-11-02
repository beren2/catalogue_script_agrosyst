select 
	ed.id as domaine_id,
	eae.id as atelier_elevage_id, 
	eae.type_elevage as atelier_elevage_type_animaux,
	eae.taille_elevage as atelier_elevage_taille,
	eae.taille_elevage_unite as atelier_elevage_unite
from entrepot_atelier_elevage eae
left join entrepot_domaine ed on ed.id = eae.domaine_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id; -- vérifier qu'on a pas de dupplication !