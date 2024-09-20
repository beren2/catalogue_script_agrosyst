select 
	epnroc.reseaux_it,
	epnroc.reseaux_ir,
	epnroc.codes_convention_dephy,
	epnroc.id as domaine_id, 
	ed.code as domaine_code, 
	ed.nom as domaine_nom, 
	ed.campagne as domaine_campagne, 
	epnroc.nb_parcelles_sans_sdc,
	epnroc.nb_parcelles_avec_id_edaplos
from 
	entrepot_parcelle_non_rattachee_outils_can epnroc
left join entrepot_domaine ed on ed.id = epnroc.id
join entrepot_domaine_filtres_outils_can edfoc on ed.id = edfoc.id
where epnroc.reseaux_ir is not null;