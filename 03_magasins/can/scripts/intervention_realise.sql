SELECT 
    d.code as domaine_code,
    d.id as domaine_id,
    d.nom as domaine_nom,
    d.campagne as domaine_campagne,
    sdc.code as sdc_code,
    sdc.id as sdc_id,
    sdc.nom as sdc_nom,
    p.id as parcelle_id,
    p.nom as parcelle_nom,
    z.id as zone_id,
    z.nom as zone_nom, 
    z.code as zone_code, 
    pppr.id as phase_id, 
    pppr.type as phase,
    c.id as culture_id, 
    (replace(replace(c.nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as culture_nom,
    cr.culture_intermediaire_id as ci_id,
    (replace(replace(c_intermediaire.nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as ci_nom,
    CASE CAST(ir.concerne_ci AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END concerne_la_ci,
    iroc.esp_complet_var as especes_de_l_intervention,
	iroc.precedent_id,
    (replace(replace(iroc.precedent_nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as precedent_nom,
	iroc.precedent_especes_edi,
    nr.rang+1 as culture_rang,
    ir.id as intervention_id,
    ir.type as intervention_type,
    iroc.interventions_actions,
    ir.nom as intervention_nom,
    (replace(replace(ir.commentaire,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as intervention_comment,
    iroc.combinaison_outil_id as combinaison_outils_id,
    (replace(replace(iroc.combinaison_outils_nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>')) as combinaison_outils_nom,
    iroc.tracteur_ou_automoteur,
    iroc.outils,
    to_char(ir.date_debut, 'DD/MM/YYYY') as date_debut,
    to_char(ir.date_fin, 'DD/MM/YYYY') as date_fin,
    ir.freq_spatiale, 
    ir.nombre_de_passage nombre_de_passage,
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
FROM  entrepot_intervention_realise ir
JOIN entrepot_intervention_realise_agrege ira ON ir.id = ira.id
JOIN entrepot_intervention_realise_outils_can iroc ON ira.id = iroc.id
JOIN entrepot_zone z ON ira.zone_id = z.id
JOIN entrepot_parcelle p ON ira.parcelle_id = p.id
LEFT JOIN entrepot_sdc sdc ON ira.sdc_id = sdc.id
JOIN entrepot_domaine d ON ira.domaine_id = d.id
LEFT JOIN entrepot_noeuds_realise nr ON ira.noeuds_realise_id = nr.id
LEFT JOIN entrepot_connection_realise cr ON cr.cible_noeuds_realise_id = nr.id
LEFT JOIN entrepot_plantation_perenne_phases_realise pppr ON CAST(ira.plantation_perenne_phases_realise_id AS VARCHAR) = pppr.id
LEFT JOIN entrepot_plantation_perenne_realise eppr on pppr.plantation_perenne_realise_id = eppr.id 
JOIN entrepot_culture c ON nr.culture_id = c.id or eppr.culture_id = c.id 
LEFT JOIN entrepot_culture c_intermediaire ON cr.culture_intermediaire_id = c_intermediaire.id
join entrepot_dispositif_filtres_outils_can edifoc on sdc.dispositif_id = edifoc.id;
