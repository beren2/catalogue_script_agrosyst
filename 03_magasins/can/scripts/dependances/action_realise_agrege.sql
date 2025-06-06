-- On génère d'abord la table agrégée complète
CREATE TEMPORARY TABLE IF NOT EXISTS entrepot_action_realise_agrege  AS
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