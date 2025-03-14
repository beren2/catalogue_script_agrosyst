-- On génère d'abord la table agrégée complète
CREATE TEMPORARY TABLE entrepot_action_synthetise_agrege IF NOT EXISTS AS
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