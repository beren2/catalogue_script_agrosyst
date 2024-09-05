

select 
	ed.code as domaine_code,
	earma.domaine_id,
	ed.nom as domaine_nom,
	ed.campagne as domaine_campagne,
	earma.sdc_id,
	esdc.nom as sdc_name,
	earma.parcelle_id,
	ep.nom as parcelle_nom,
	earma.zone_id, 
	ez.nom as zone_nom,
	earma.intervention_realise_id, 
	errp.action_id,
	ear.label as type_action,
	errp.destination_id, 
	errp.destination as destination_nom, 
	errp.rendement_moy as rendement_moyen,
	errp.rendement_median,
	errp.rendement_min,
	errp.rendement_max,
	errp.rendement_unite as unite,
	errp.commercialisation_pct, 
	errp.autoconsommation_pct,
	errp.nonvalorisation_pct
from entrepot_recolte_rendement_prix errp
join entrepot_action_realise ear on errp.action_id = ear.id
left join entrepot_action_realise_agrege earma on errp.action_id = earma.id
left join entrepot_domaine ed on earma.domaine_id = ed.id
left join entrepot_sdc esdc on earma.sdc_id = esdc.id
left join entrepot_zone ez on earma.zone_id = ez.id
left join entrepot_parcelle ep on earma.parcelle_id = ep.id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;
