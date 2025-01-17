

SELECT 
    d.id as domaine_id,
    d.nom as domaine_nom,
    d.code as domaine_code,
    d.campagne as domaine_campagne,
    sdc.code as sdc_code,
    sdc.id as sdc_id,
    sdc.nom as sdc_nom,
    s.id as systeme_synthetise_id,
    s.nom as systeme_synthetise_nom,
    s.campagnes as systeme_synthetise_campagnes,
    CASE CAST(s.valide AS BOOLEAN) WHEN true then 'oui' WHEN false then 'non' END systeme_synthetise_validation,
    pppr.id as phase_id, 
    pppr.type as phase,
    c.code as culture_code, 
    (replace(replace(CAST(c.nom AS VARCHAR),CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as culture_nom,
    c_i.code as ci_code,
    (replace(replace(CAST(c_i.nom AS VARCHAR),CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as ci_nom,
    CASE CAST(ir.concerne_ci AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END concerne_la_ci,
    iroc.esp_complet_var as especes_de_l_intervention,
	iroc.precedent_code,
    (replace(replace(CAST(iroc.precedent_nom AS VARCHAR),CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as precedent_nom,
	iroc.precedent_especes_edi,
    ecs.id as culture_precedent_rang_id,
    nr.rang+1 as culture_rang,
    ir.id as intervention_id,
    ir.rang as rang_intervention,
    ir.type as intervention_type,
    iroc.interventions_actions,
    ir.nom as intervention_nom,
    (replace(replace(CAST(ir.commentaire AS VARCHAR),CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as intervention_comment,
    co.code as combinaison_outils_code,
    (replace(replace(CAST(iroc.combinaison_outils_nom AS VARCHAR), CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as combinaison_outils_nom,
    iroc.tracteur_ou_automoteur,
    iroc.outils,
    ir.date_debut as date_debut,
    ir.date_fin as date_fin,
    ir.freq_spatiale, 
    ir.freq_temporelle as freq_temporelle,
    ir.psci as psci,
    ir.psci_phyto_avec_amm as psci_phyto,
    ir.psci_phyto_sans_amm as psci_lutte_bio,
    iroc.proportion_surface_traitee_phyto,
    iroc.proportion_surface_traitee_lutte_bio,
    ir.debit_de_chantier,
    ir.debit_de_chantier_unite, 
    ir.nb_personne_mobili,
    iroc.quantite_eau_mm,
    iroc.especes_semees,
    iroc.densite_semis,
    iroc.unite_semis,
    iroc.traitement_chimique_semis,
    iroc.inoculation_biologique_semis,
    iroc.type_semence
FROM  entrepot_intervention_synthetise ir
LEFT JOIN entrepot_connection_synthetise ecs ON ecs.id = ir.connection_synthetise_id  
LEFT JOIN entrepot_intervention_synthetise_agrege_extanded irae ON ir.id = irae.id
LEFT JOIN entrepot_intervention_synthetise_outils_can iroc ON irae.id = iroc.id
LEFT JOIN entrepot_noeuds_synthetise nr ON irae.cible_noeuds_synthetise_id = nr.id
LEFT JOIN entrepot_plantation_perenne_phases_synthetise pppr ON CAST(irae.plantation_perenne_phases_synthetise_id AS VARCHAR)= pppr.id
LEFT JOIN entrepot_plantation_perenne_synthetise epps on pppr.plantation_perenne_synthetise_id = epps.id 
LEFT JOIN entrepot_synthetise s ON nr.synthetise_id = s.id or epps.synthetise_id = s.id
LEFT JOIN entrepot_sdc sdc ON irae.sdc_id = sdc.id
LEFT JOIN entrepot_domaine d ON irae.domaine_id = d.id
left join entrepot_culture c on irae.culture_id = c.id
left join entrepot_culture c_i on irae.culture_intermediaire_id = c_i.id
LEFT JOIN entrepot_combinaison_outil co ON iroc.combinaison_outil_id = co.id
join entrepot_dispositif_filtres_outils_can edifoc on sdc.dispositif_id = edifoc.id;