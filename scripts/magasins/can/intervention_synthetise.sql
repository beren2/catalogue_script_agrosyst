

SELECT 
    d.code as domaine_code,
    d.id as domaine_id,
    d.nom as domaine_nom,
    d.campagne as domaine_campagne,
    sdc.code as sdc_code,
    sdc.id as sdc_id,
    sdc.nom as sdc_nom,
    s.id as synthetise_id,
    s.nom as synthetise_nom,
    pppr.id as phase_id, 
    pppr.type as phase,
    nr.culture_code as culture_code, 
    (replace(replace(c.nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as culture_nom,
    c_i.id as ci_id,
    c_i.code as ci_code,
    (replace(replace(c_i.nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as ci_nom,
    CASE ir.concerne_ci WHEN true THEN 'oui' WHEN false THEN 'non' END concerne_la_ci,
    iroc.esp_var as especes_de_l_intervention,
	iroc.precedent_code,
    (replace(replace(iroc.precedent_nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as precedent_nom,
	iroc.precedent_especes_edi,
    nr.rang+1 as culture_rang,
    ir.id as intervention_id,
    ir.type as intervention_type,
    iroc.interventions_actions,
    ir.nom as intervention_nom,
    (replace(replace(ir.commentaire,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as intervention_comment,
    co.code as combinaison_outils_code,
    (replace(replace(iroc.combinaison_outils_nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as combinaison_outils_nom,
    iroc.tracteur_ou_automoteur,
    iroc.outils,
    ir.date_debut,
    ir.date_fin,
    ir.freq_spatiale, 
    ir.freq_temporelle as freq_temporelle,
    ir.psci_intervention as psci,
    iroc.proportion_surface_traitee_phyto,
    iroc.psci_phyto, 
    iroc.proportion_surface_traitee_lutte_bio,
    iroc.psci_lutte_bio,
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
LEFT JOIN entrepot_intervention_synthetise_agrege_extanded irae ON ir.id = irae.id
LEFT JOIN entrepot_intervention_synthetise_outils_can iroc ON irae.id = iroc.intervention_synthetise_id
LEFT JOIN entrepot_noeuds_synthetise nr ON irae.cible_noeuds_synthetise_id = nr.id
LEFT JOIN entrepot_synthetise s ON nr.synthetise_id = s.id
LEFT JOIN entrepot_sdc sdc ON irae.sdc_id = sdc.id
LEFT JOIN entrepot_domaine d ON irae.domaine_id = d.id
left join entrepot_culture c on irae.culture_id = c.id
left join entrepot_culture c_i on irae.culture_intermediaire_id = c_i.id
LEFT JOIN entrepot_plantation_perenne_phases_synthetise pppr ON irae.plantation_perenne_phases_synthetise_id = pppr.id
LEFT JOIN entrepot_combinaison_outil co ON iroc.combinaison_outil_id = co.id
join entrepot_dispositif_filtres_outils_can edifoc on sdc.dispositif_id = edifoc.id;
