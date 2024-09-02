-- On génère d'abord la table agrégée complète
CREATE TEMPORARY TABLE entrepot_action_synthetise_agrege AS
SELECT DISTINCT 
	nuirac.action_synthetise_id as id,
    nuirac.intervention_synthetise_id, 
    nuirac.plantation_perenne_synthetise_id, 
    nuirac.connection_synthetise_id, 
    nuirac.cible_noeuds_synthetise_id,
    nuirac.plantation_perenne_phases_synthetise_id, 
    nuirac.synthetise_id, 
    nuirac.sdc_campagne, 
    nuirac.sdc_id, 
    nuirac.domaine_id, 
    nuirac.dispositif_id
FROM
    entrepot_action_synthetise air 
LEFT JOIN "entrepot_utilisation_intrant_synthetise_agrege" nuirac on air.id = nuirac.action_synthetise_id
UNION 
SELECT 
    id, 
    intervention_synthetise_id,
    plantation_perenne_synthetise_id, connection_synthetise_id, cible_noeuds_synthetise_id, plantation_perenne_phases_synthetise_id, synthetise_id, 
    sdc_campagne, sdc_id, domaine_id, dispositif_id
FROM entrepot_action_synthetise_manquant_agrege earma;

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
	earma.intervention_synthetise_id, 
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
join entrepot_action_synthetise ear on errp.action_id = ear.id
left join entrepot_action_synthetise_manquant_agrege earma on errp.action_id = earma.id
left join entrepot_domaine ed on earma.domaine_id = ed.id
left join entrepot_sdc esdc on earma.sdc_id = esdc.id
left join entrepot_synthetise es on es.id = earma.synthetise_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;
