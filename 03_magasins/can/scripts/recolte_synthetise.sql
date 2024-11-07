select 
	ed.code as domaine_code,
	earma.domaine_id,
	ed.nom as domaine_nom,
	ed.campagne as domaine_campagne,
	earma.sdc_id,
	esdc.nom as sdc_nom,
	es.id as systeme_synthetise_id, 
	es.nom as systeme_synthetise_nom,
	es.campagnes as systeme_synthetise_campagnes,
	earma.intervention_synthetise_id as intervention_id, 
	errp.action_id,
	ear.label as type_action,
	errp.destination as destination_nom, 
	errp.rendement_moy_corr as rendement_moyen,
	errp.rendement_median_corr as rendement_median,
	errp.rendement_min_corr as rendement_min,
	errp.rendement_max_corr as rendement_max,
	errp.rendement_unite as unite,
	errp.commercialisation_pct_corr as commercialisation_pct, 
	errp.autoconsommation_pct_corr as autoconsommation_pct,
	errp.nonvalorisation_pct_corr as nonvalorisation_pct
from entrepot_recolte_outils_can errp
join entrepot_action_synthetise ear on errp.action_id = ear.id
left join entrepot_action_synthetise_manquant_agrege earma on errp.action_id = earma.id
left join entrepot_domaine ed on earma.domaine_id = ed.id
left join entrepot_sdc esdc on earma.sdc_id = esdc.id
left join entrepot_synthetise es on es.id = earma.synthetise_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;
