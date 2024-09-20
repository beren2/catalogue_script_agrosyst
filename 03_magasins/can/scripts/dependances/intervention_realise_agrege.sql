-- On génère d'abord la table agrégée complète
CREATE TEMPORARY TABLE entrepot_intervention_realise_agrege AS
SELECT DISTINCT 
    nuirac.intervention_realise_id AS id, 
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
    entrepot_intervention_realise eir
LEFT JOIN "entrepot_utilisation_intrant_realise_agrege" nuirac on eir.id = nuirac.intervention_realise_id
UNION 
SELECT
    id, 
    plantation_perenne_realise_id, zone_id, noeuds_realise_id, plantation_perenne_phases_realise_id, parcelle_id, sdc_campagne, sdc_id, domaine_id, dispositif_id
FROM entrepot_intervention_realise_manquant_agrege;