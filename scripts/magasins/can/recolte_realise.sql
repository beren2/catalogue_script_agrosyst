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
	dv.libelle as destination_nom, 
	errp.rendement_moy_corr as rendement_moyen,
	errp.rendement_median_corr as rendement_median,
	errp.rendement_min_corr as rendement_min,
	errp.rendement_max_corr as rendement_max,
	errp.rendement_unite as unite,
	errp.commercialisation_pct_corr as commercialisation_pct, 
	errp.autoconsommation_pct_corr as autoconsommation_pct,
	errp.nonvalorisation_pct_corr as nonvalorisation_pct
from entrepot_recolte_outils_can errp
join entrepot_action_realise ear on errp.action_id = ear.id
left join entrepot_action_realise_agrege earma on errp.action_id = earma.id
left join entrepot_domaine ed on earma.domaine_id = ed.id
left join entrepot_sdc esdc on earma.sdc_id = esdc.id
left join entrepot_zone ez on earma.zone_id = ez.id
left join entrepot_parcelle ep on earma.parcelle_id = ep.id
left join entrepot_destination_valorisation dv on errp.destination_id = dv.id
join entrepot_dispositif_filtres_outils_can edfoc on esdc.dispositif_id = edfoc.id;