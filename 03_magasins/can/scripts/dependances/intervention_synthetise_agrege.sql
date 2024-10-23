CREATE TEMPORARY TABLE entrepot_intervention_synthetise_agrege AS
SELECT DISTINCT 
    nuirac.intervention_synthetise_id AS id, 
    nuirac.plantation_perenne_synthetise_id, 
    nuirac.cible_noeuds_synthetise_id,
    nuirac.connection_synthetise_id,
    nuirac.plantation_perenne_phases_synthetise_id, 
    nuirac.synthetise_id,
    nuirac.sdc_id, 
    nuirac.sdc_campagne, 
    nuirac.domaine_id, 
    nuirac.dispositif_id
FROM
    entrepot_intervention_synthetise eir 
LEFT JOIN "entrepot_utilisation_intrant_synthetise_agrege" nuirac on eir.id = nuirac.intervention_synthetise_id
WHERE nuirac.intervention_synthetise_id IS NOT null
UNION 
SELECT 
    id, 
    plantation_perenne_synthetise_id, 
    cible_noeuds_synthetise_id,
    connection_synthetise_id, 
    plantation_perenne_phases_synthetise_id, 
    synthetise_id, 
    sdc_id, 
    sdc_campagne, 
    domaine_id, 
    dispositif_id
FROM entrepot_intervention_synthetise_manquant_agrege;

alter table entrepot_intervention_synthetise_agrege add primary key (id);


-- on rajoute les informations sur les culture_id et culture intermediaire_id...
CREATE TEMPORARY TABLE entrepot_intervention_synthetise_agrege_extanded AS 
SELECT 
    eisa.id, 
    eisa.plantation_perenne_synthetise_id, 
    eisa.cible_noeuds_synthetise_id,
    eisa.connection_synthetise_id, 
    eisa.plantation_perenne_phases_synthetise_id, 
    eisa.synthetise_id, 
    eisa.sdc_id, 
    eisa.sdc_campagne, 
    eisa.domaine_id, 
    eisa.dispositif_id,
    coalesce(nsr.culture_id, '') || coalesce(eppsr.culture_id, '') as culture_id,
    csr.culture_intermediaire_id
FROM entrepot_intervention_synthetise_agrege eisa
LEFT JOIN entrepot_noeuds_synthetise_restructure nsr ON nsr.id = eisa.cible_noeuds_synthetise_id
LEFT JOIN entrepot_connection_synthetise_restructure csr ON csr.id = CAST(eisa.connection_synthetise_id AS VARCHAR)
LEFT JOIN entrepot_plantation_perenne_synthetise_restructure eppsr ON eppsr.id = CAST(eisa.plantation_perenne_synthetise_id AS VARCHAR);

alter table entrepot_intervention_synthetise_agrege_extanded add primary key (id);

