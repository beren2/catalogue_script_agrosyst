-- On génère d'abord la table agrégée complète
CREATE TEMPORARY TABLE entrepot_action_realise_agrege AS
SELECT DISTINCT 
	nuirac.action_realise_id as id,
    nuirac.intervention_realise_id, 
    nuirac.plantation_perenne_realise_id, 
    nuirac.zone_id, 
    nuirac.noeuds_realise_id, 
    nuirac.plantation_perenne_phases_realise_id, 
    nuirac.parcelle_id, 
    nuirac.sdc_campagne, 
    nuirac.sdc_id, 
    nuirac.domaine_id, 
    nuirac.dispositif_id
FROM
    entrepot_action_realise air 
LEFT JOIN "entrepot_utilisation_intrant_realise_agrege" nuirac on air.id = nuirac.action_realise_id
UNION 
SELECT 
    id, 
    intervention_realise_id,
    plantation_perenne_realise_id, zone_id, noeuds_realise_id, plantation_perenne_phases_realise_id, parcelle_id, sdc_campagne, sdc_id, domaine_id, dispositif_id
FROM entrepot_action_realise_manquant_agrege earma;

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
