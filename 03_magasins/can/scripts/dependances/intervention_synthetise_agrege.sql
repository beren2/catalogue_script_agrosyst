

-- on rajoute les informations sur les culture_id et culture intermediaire_id...
CREATE TEMPORARY TABLE IF NOT EXISTS entrepot_intervention_synthetise_agrege_extanded AS 
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

--alter table entrepot_intervention_synthetise_agrege_extanded add primary key (id);

