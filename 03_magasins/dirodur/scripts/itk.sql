SELECT
    'realise' as mode_saisie,
    null as connexion_id,

    --------------------
	-- NOEUDS_REALISE --
	--------------------
	itkR.itk_realise_id as noeud_id,

	-------------
	-- CULTURE --
	-------------
	-- culture_*
	culture1.id as culture_id,
	culture1.nom as culture_nom,
	culture1.melange_especes as culture_est_melange_especes,
	culture1.melange_varietes as culture_est_melange_varietes,
	culture1."type" as culture_type,

	-- culture_typocan_*
	typoc1.typocan_culture_sans_compagne as culture_typo_can_sans_compagne,
	typoc1.typocan_espece as culture_typo_can_espece,
	typoc1.typocan_esp_sans_compagne as culture_typo_can_espece_sans_compagne,
	typoc1.nb_composant_culture as culture_typo_can_nbre_composant,
	typoc1.nb_typocan_esp as culture_typo_can_nbre_espece,

	-- culture_intermediaire_*
	culture_inter.id as culture_intermediaire_id,
	culture_inter.nom as culture_intermediaire_nom,

	-- culture_intermediaire_typocan_*
	typoci.typocan_culture_sans_compagne as culture_intermerdiaire_typo_can_sans_compagne,
	typoci.typocan_espece as culture_intermerdiaire_typo_can_espece,
	typoci.nb_composant_culture as culture_intermerdiaire_typo_can_nbre_composant,

    -- culture_precedente_*
    culture_prec.id as culture_precedente_id,
	culture_prec.nom as culture_precedente_nom,
	culture_prec.melange_especes as culture_precedente_est_melange_especes,
	culture_prec.melange_varietes as culture_precedente_est_melange_varietes,
	culture_prec."type" as culture_precedente_type,

    -- culture_precedente_typocan_*
	typocp.typocan_culture_sans_compagne as culture_precedente_typo_can_sans_compagne,
	typocp.typocan_espece as culture_precedente_typo_can_espece,
	typocp.nb_composant_culture as culture_precedente_typo_can_nbre_composant,
    
    ---------
	-- SDC --
	---------
	sdc.id as sdc_id,
	sdc.code as sdc_code,
	sdc.nom as sdc_nom,
	sdc.code_dephy as sdc_numero_dephy,
	sdc.filiere as sdc_filiere,
	sdc.type_production as sdc_type_production,
	sdc.type_agriculture as sdc_type_agriculture,
	sdc.part_sau_domaine as sdc_part_sau_domaine,

	-- sdc_typo_*
	typoassol.surface_totale_assol_dvlp as sdc_typo_surface_totale_assol_dvlp,
	typoassol.surface_totale_assol as sdc_typo_surface_totale_assol,
	
	-- sdc_typocan_*
	typoassol.typocan_assol_dvlp  as sdc_typo_can_assol_dvlp,
	typoassol.typocan_assol  as sdc_typo_can_assol,

	-- sdc_typoculture_*
	typoassol.list_freq_typoculture_dvlp  as sdc_typo_culture_liste_dvlp,
	typoassol.list_freq_typoculture as sdc_typo_culture_liste,

    ----------------
	-- DISPOSITIF --
	----------------
	sdc.dispositif_id as dispositif_id,
	dispo.code as dispositif_code,
	dispo.nom as dispositif_nom,
	dispo."type" as dispositif_type,

	-------------
	-- DOMAINE --
	-------------
	dom.id as domaine_id,
	dom.code as domaine_code,
	dom.nom as domaine_nom,
	dom.campagne as domaine_campagne,
	dom.siret as domaine_siret,
	dom.type_ferme as domaine_type_ferme,
	dom.departement as domaine_position_departement,
	dom.commune_id as domaine_position_commune_id,
	interop.codeinsee as domaine_position_code_insee,
	interop.safran_cell_id as domaine_position_cellule_safran,
	interop.rmqs_site_id as domaine_position_rmqs_site_id,
	dom.zonage as domaine_zonage,
	-- domaine_pct_*
	dom.pct_sau_zone_vulnerable as domaine_pct_sau_zone_vulnerable,
	dom.pct_sau_zone_excedent_structurel as domaine_pct_sau_zone_excedent_structurel,
	dom.pct_sau_zone_actions_complementaires as domaine_pct_sau_zone_actions_complementaires,
	dom.pct_sau_zone_natura_2000 as domaine_pct_sau_zone_natura_2000,
	dom.pct_sau_zone_erosion as domaine_pct_sau_zone_erosion,
	dom.pct_sau_perimetre_protection_captage as domaine_pct_sau_perimetre_protection_captage,
	dom.annee_naissance_exploitant as domaine_annee_naissance_exploitant,
	dom.cotisation_msa as domaine_cotisation_msa,
	dom.fermage_moyen as domaine_fermage_moyen,
	dom.aides_decouplees as domaine_aides_decouplees,
	dom.nombre_parcelles as domaine_nombre_parcelles,
	dom.distance_siege_parcelle_max as domaine_distance_siege_parcelle_max,
	-- domaine_parcelles_*
	dom.parcelles_groupees as domaine_parcelles_groupees,
	dom.parcelles_dispersees as domaine_parcelles_dispersees,
	dom.parcelles_plutot_dispersees as domaine_parcelles_plutot_dispersees,
	dom.parcelles_groupees_distinctes as domaine_parcelles_groupees_distinctes,
	dom.parcelles_plutot_groupees as domaine_parcelles_plutot_groupees,
	-- domaine_otex_* 
	dom.otex_18_nom as domaine_otex_18_nom,
	dom.otex_70_nom as domaine_otex_70_nom,
	dom.statut_juridique_nom as domaine_statut_juridique_nom,
	dom.objectifs as domaine_objectifs,
	dom.atouts_domaine as domaine_atouts,
	dom.contraintes_domaine as domaine_contraintes,
	dom.perspective_evolution_domaine as domaine_perspectives_evolution,
	-- domaine_membre_*
	dom.membre_cooperative as domaine_est_membre_cooperative,
	dom.membre_groupe_developpement as domaine_est_membre_groupe_developpement,
	dom.membre_cuma as domaine_est_membre_cuma,
	dom.domaine_touristique as domaine_est_touristique,
	-- domaine_main_oeuvre_*
	dom.main_oeuvre_exploitant as domaine_main_oeuvre_exploitant,
	dom.main_oeuvre_non_saisoniere as domaine_main_oeuvre_non_saisoniere,
	dom.main_oeuvre_saisoniere as domaine_main_oeuvre_saisoniere,
	dom.main_oeuvre_volontaire as domaine_main_oeuvre_volontaire,
	dom.sau_totale as domaine_sau,
    interop.typo_ruralite as domaine_typologie_ruralite,

	-----------------
	-- DOMAINE_SOL --
	-----------------
	-- domsol.id as domaine_sol_id,
	-- domsol.nom_local as domaine_sol_nom,
	-- domsol.sol_arvalis_id as domaine_sol_arvalis_id,


    --------------------------------
	-- NOEUDS_REALISE_RESTRUCTURE --
	--------------------------------
    null as noeud_est_fin_cycle,
    null as noeud_est_meme_campagne_noeud_precedent,
	node_res.precedent_noeuds_realise_id as noeud_precedent_id,
    null as noeud_precedent_est_fin_cycle,
    null as noeud_precedent_est_meme_campagne_noeud_precedent,

    ----------------
	-- SYNTHETISE --
	----------------
	null as synthetise_id, 
    null as synthetise_rotation_typo_can, 
    null as synthetise_rotation_typo_liste_culture,
    null as synthetise_nom,
    null as synthetise_campagnes,
	false as synthetise_est_pz0,

    -------------
	-- REALISE --
	-------------
	zone.id as zone_id,
	zone.code as zone_code,
	zone.nom as zone_nom,
	zone.surface as zone_surface,
	parcelle.code as parcelle_code,
	parcelle.nom as parcelle_nom,
	parcelle.commune_id as parcelle_commune_id,
	parcelle.sol_nom_ref as parcelle_sol_nom_ref ,
	CASE when parcelle.edaplos_utilisateur_id is not null THEN True ELSE False END AS parcelle_import_edaplos,


    ----------------
	-- CONNEXION --
	----------------
    null as connexion_frequence, 
    null as connexion_est_culture_absente,
    null as connexion_poids_agregation,

	--------------------------------
	-- NOEUDS_REALISE_PERFORMANCE --
	--------------------------------
	-- ift_cible_non_mil_*
	itkR.ift_cible_non_mil_chimique_tot as itk_ift_cible_non_mil_chimique_tot,
	itkR.ift_cible_non_mil_chim_tot_hts as itk_ift_cible_non_mil_chim_tot_hts,
	itkR.ift_cible_non_mil_h as itk_ift_cible_non_mil_h,
	itkR.ift_cible_non_mil_f as itk_ift_cible_non_mil_f,
	itkR.ift_cible_non_mil_i as itk_ift_cible_non_mil_i,
	itkR.ift_cible_non_mil_ts as itk_ift_cible_non_mil_ts,
	itkR.ift_cible_non_mil_a as itk_ift_cible_non_mil_a,
	itkR.ift_cible_non_mil_hh as itk_ift_cible_non_mil_hh,
	itkR.ift_cible_non_mil_biocontrole as itk_ift_cible_non_mil_biocontrole,

	-- recours_*
	itkR.recours_aux_moyens_biologiques as itk_recours_aux_moyens_biologiques,
	itkR.recours_macroorganismes as itk_recours_macroorganismes,
	itkR.recours_produits_biotiques_sansamm as itk_recours_produits_biotiques_sans_amm,
	itkR.recours_produits_abiotiques_sansamm as itk_recours_produits_abiotiques_sans_amm,

	-- tps_*
	itkR.tps_utilisation_materiel as itk_tps_utilisation_materiel,
	itkR.tps_travail_manuel as itk_tps_travail_manuel,
	itkR.tps_travail_mecanise as itk_tps_travail_meca,
	itkR.tps_travail_total as itk_tps_travail_total,

	-- nbre_de_passages_*
	itkR.nbre_de_passages as itk_nbre_de_passages,
	itkR.nbre_de_passages_labour as itk_nbre_de_passages_labour,
	itkR.nbre_de_passages_tcs as itk_nbre_de_passages_tcs,
	itkR.nbre_de_passages_desherbage_meca as itk_nbre_de_passages_desherbage_meca,
	itkR.utili_desherbage_meca as itk_utili_desherbage_meca, -- TODO a suppr une fois que nbre_de_passages_desherbage_meca est débugué
	itkR.type_de_travail_du_sol as itk_type_de_travail_du_sol,
	
	-- co_std_mil_*
	itkR.co_tot_std_mil as itk_co_std_mil_tot,
	itkR.co_semis_std_mil as itk_co_std_mil_semis,
	itkR.co_fertimin_std_mil as itk_co_std_mil_fertimin,
	itkR.co_epandage_orga_std_mil as itk_co_std_mil_epandage_orga,
	itkR.co_phyto_sans_amm_std_mil as itk_co_std_mil_phyto_sans_amm,
	itkR.co_phyto_avec_amm_std_mil as itk_co_std_mil_phyto_avec_amm,
	itkR.co_trait_semence_std_mil as itk_co_std_mil_trait_semence,
	itkR.co_irrigation_std_mil as itk_co_std_mil_irrigation,
	itkR.co_intrants_autres_std_mil as itk_co_std_mil_intrants_autres,

	-- cm_std_mil
	itkR.cm_std_mil as itk_cm_std_mil,

	-- c_main_oeuvre_std_mil_*
	itkR.c_main_oeuvre_tot_std_mil as itk_c_main_oeuvre_std_mil_tot,
	itkR.c_main_oeuvre_tractoriste_std_mil as itk_c_main_oeuvre_std_mil_tractoriste,
	itkR.c_main_oeuvre_manuelle_std_mil as itk_c_main_oeuvre_std_mil_manuelle,

	-- pb_std_mil_*
	itkR.pb_std_mil_avec_autoconso as itk_pb_std_mil_avec_autoconso, -- Consigne pour ceux qui n'utilise pas les atelier d'élevage : avec auto
	itkR.pb_std_mil_sans_autoconso as itk_pb_std_mil_sans_autoconso,

	-- mb_std_mil_*
	itkR.mb_std_mil_avec_autoconso as itk_mb_std_mil_avec_autoconso,
	itkR.mb_std_mil_sans_autoconso as itk_mb_std_mil_sans_autoconso,

	-- msn_std_mil_*
	itkR.msn_std_mil_sans_autoconso as itk_msn_std_mil_sans_autoconso,
	itkR.msn_std_mil_avec_autoconso as itk_msn_std_mil_avec_autoconso,

	-- md_std_mil_*
	itkR.md_std_mil_sans_autoconso as itk_md_std_mil_sans_autoconso,
	itkR.md_std_mil_avec_autoconso as itk_md_std_mil_avec_autoconso,

	-- conso_* 
	itkR.conso_carburant as itk_conso_carburant,
	itkR.conso_eau as itk_conso_eau,

	-- ferti_*
	itkR.ferti_n_mineral as itk_ferti_n_mineral,
	itkR.ferti_n_organique as itk_ferti_n_organique,
	itkR.ferti_p2o5_mineral as itk_ferti_p2o5_mineral,
	itkR.ferti_p2o5_organique as itk_ferti_p2o5_organique,
	itkR.ferti_k2o_mineral as itk_ferti_k2o_mineral,
	itkR.ferti_k2o_organique as itk_ferti_k2o_organique,

	-- qsa_*
	itkR.qsa_tot_hts as itk_qsa_tot_hts,
	itkR.qsa_tot as itk_qsa_tot,
	itkR.qsa_danger_environnement_hts as itk_qsa_danger_environnement_hts,
	itkR.qsa_toxique_utilisateur_hts as itk_qsa_toxique_utilisateur_hts,
	itkR.qsa_cmr_hts as itk_qsa_cmr_hts,
	itkR.qsa_substances_candidates_substitution_hts as itk_qsa_substances_candidates_substitution_hts,
	itkR.qsa_substances_faible_risque_hts  as itk_qsa_substances_faible_risque_hts,
	itkR.qsa_glyphosate_hts as itk_qsa_glyphosate_hts,
	itkR.qsa_chlortoluron_hts as itk_qsa_chlortoluron_hts,
	itkR.qsa_diflufenican_hts as itk_qsa_diflufenican_hts,
	itkR.qsa_prosulfocarbe_hts as itk_qsa_prosulfocarbe_hts,
	itkR.qsa_smetolachlore_hts as itk_qsa_smetolachlore_hts,
	itkR.qsa_boscalid_hts as itk_qsa_boscalid_hts,
	itkR.qsa_fluopyram_hts as itk_qsa_fluopyram_hts,
	itkR.qsa_lambda_cyhalothrine_hts as itk_qsa_lambda_cyhalothrine_hts,
	itkR.qsa_cuivre_tot_hts as itk_qsa_cuivre_tot_hts,
	itkR.qsa_cuivre_tot as itk_qsa_cuivre_tot,
	itkR.qsa_cuivre_phyto_hts as itk_qsa_cuivre_phyto_hts,
	itkR.qsa_cuivre_ferti as itk_qsa_cuivre_ferti,
	itkR.qsa_soufre_tot_hts as itk_qsa_soufre_tot_hts,
	itkR.qsa_soufre_phyto_hts as itk_qsa_soufre_phyto_hts,
	itkR.qsa_soufre_ferti as itk_qsa_soufre_ferti,
	itkR.qsa_bixafen as itk_qsa_bixafen,
	itkR.qsa_dicamba as itk_qsa_dicamba,
	itkR.qsa_mancozeb as itk_qsa_mancozeb,
	itkR.qsa_phosmet as itk_qsa_phosmet,
	itkR.qsa_tebuconazole as itk_qsa_tebuconazole,
	itkR.qsa_dimethenamidp as itk_qsa_dimethenamidp,
	itkR.qsa_pendimethalin as itk_qsa_pendimethalin,
	itkR.qsa_flufenacet as itk_qsa_flufenacet,
	itkR.qsa_aclonifen as itk_qsa_aclonifen,
	itkR.qsa_isoxaben as itk_qsa_isoxaben,
	itkR.qsa_beflutamid as itk_qsa_beflutamid,
	itkR.qsa_isoproturon as itk_qsa_isoproturon,
	itkR.qsa_clothianidine as itk_qsa_clothianidine,
	itkR.qsa_imidaclopride as itk_qsa_imidaclopride,
	itkR.qsa_thiamethoxam as itk_qsa_thiamethoxam,
	itkR.qsa_acetamipride as itk_qsa_acetamipride,
	itkR.qsa_thiaclopride as itk_qsa_thiaclopride,
	itkR.qsa_neonicotinoides as itk_qsa_neonicotinoides,
	itkR.qsa_abamectine_hts as itk_qsa_abamectine_hts,
	itkR.qsa_alpha_cypermethrine_hts as itk_qsa_alpha_cypermethrine_hts,
	itkR.qsa_azadirachtine_hts as itk_qsa_azadirachtine_hts,
	itkR.qsa_beta_cyfluthrine_hts as itk_qsa_beta_cyfluthrine_hts,
	itkR.qsa_chlorpyrifos_methyl_hts as itk_qsa_chlorpyrifos_methyl_hts,
	itkR.qsa_cyantraniliprole_hts as itk_qsa_cyantraniliprole_hts,
	itkR.qsa_cypermethrine_hts as itk_qsa_cypermethrine_hts,
	itkR.qsa_deltamethrine_hts as itk_qsa_deltamethrine_hts,
	itkR.qsa_dimethoate_hts as itk_qsa_dimethoate_hts,
	itkR.qsa_emamectine_hts as itk_qsa_emamectine_hts,
	itkR.qsa_esfenvalerate_hts as itk_qsa_esfenvalerate_hts,
	itkR.qsa_flonicamide_hts as itk_qsa_flonicamide_hts,
	itkR.qsa_huile_de_colza_hts as itk_qsa_huile_de_colza_hts,
	itkR.qsa_huile_de_paraffine_hts as itk_qsa_huile_de_paraffine_hts,
	itkR.qsa_indoxacarbe_hts as itk_qsa_indoxacarbe_hts,
	itkR.qsa_primicarbe_hts as itk_qsa_primicarbe_hts,
	itkR.qsa_pymetrozine_hts as itk_qsa_pymetrozine_hts,
	itkR.qsa_pyrethrine_hts as itk_qsa_pyrethrine_hts,
	itkR.qsa_silicate_aluminium_hts as itk_qsa_silicate_aluminium_hts,
	itkR.qsa_spinosad_hts as itk_qsa_spinosad_hts,
	itkR.qsa_spirotetramate_hts as itk_qsa_spirotetramate_hts,
	itkR.qsa_tau_fluvalinate_hts as itk_qsa_tau_fluvalinate_hts
	
FROM entrepot_itk_realise_performance AS itkR
LEFT JOIN entrepot_noeuds_realise_restructure AS node_res ON node_res.id = itkR.noeuds_realise_id 
LEFT JOIN entrepot_connection_realise AS cx ON cx.cible_noeuds_realise_id = itkR.noeuds_realise_id
LEFT JOIN entrepot_zone AS zone ON zone.id = itkR.zone_id 
LEFT JOIN entrepot_parcelle AS parcelle ON parcelle.id = zone.parcelle_id 
JOIN (
	SELECT * from entrepot_sdc as sdc 
	-- filtration sur les systèmes de cultures en grandes cultures et polyculture-élevage
	where sdc.filiere = 'POLYCULTURE_ELEVAGE' or sdc.filiere = 'GRANDES_CULTURES'
) sdc on sdc.id = parcelle.sdc_id
LEFT JOIN entrepot_domaine AS dom ON dom.id = parcelle.domaine_id
--LEFT JOIN entrepot_domaine_sol AS domsol ON domsol.id = parcelle.domaine_sol_id 
LEFT JOIN entrepot_dispositif AS dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_commune AS comm ON parcelle.commune_id = comm.id
LEFT JOIN entrepot_donnees_spatiales_commune_du_domaine AS interop ON interop.domaine_id = parcelle.domaine_id
LEFT JOIN entrepot_culture AS culture1 ON culture1.id = itkR.culture_id 
LEFT JOIN entrepot_typologie_can_culture AS typoc1 ON typoc1.culture_id = itkR.culture_id 
LEFT JOIN entrepot_culture AS culture_inter ON culture_inter.id = cx.culture_intermediaire_id 
LEFT JOIN entrepot_typologie_can_culture AS typoci ON typoci.culture_id = cx.culture_intermediaire_id 
LEFT JOIN entrepot_noeuds_realise AS noeud_prec ON node_res.precedent_noeuds_realise_id = noeud_prec.id
LEFT JOIN entrepot_culture AS culture_prec ON culture_prec.id = noeud_prec.culture_id 
LEFT JOIN entrepot_typologie_can_culture AS typocp ON typocp.culture_id = culture_prec.id 
LEFT JOIN entrepot_typologie_assol_can_realise AS typoassol ON typoassol.sdc_id = sdc.id
WHERE
	(itkR.alerte_co_semis_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_co_semis_std_mil is null) AND 
	(itkR.alerte_ift_cible_non_mil_chim_tot_hts IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_ift_cible_non_mil_chim_tot_hts is null) AND 
	(itkR.alerte_ift_cible_non_mil_f IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_ift_cible_non_mil_f is null) AND
	(itkR.alerte_ift_cible_non_mil_h IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_ift_cible_non_mil_h is null) AND	
	(itkR.alerte_ift_cible_non_mil_i IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_ift_cible_non_mil_i is null) AND	
	(itkR.alerte_ift_cible_non_mil_biocontrole IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_ift_cible_non_mil_biocontrole is null) AND	
	(itkR.alerte_co_irrigation_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_co_irrigation_std_mil is null) AND	
	(itkR.alerte_msn_std_mil_avec_autoconso IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_msn_std_mil_avec_autoconso is null) AND	
	(itkR.alerte_pb_std_mil_avec_autoconso IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_pb_std_mil_avec_autoconso is null) AND	
	(itkR.alerte_rendement IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_rendement is null) AND	
	(itkR.alerte_cm_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_cm_std_mil is null) AND	
	(itkR.alerte_co_semis_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alerte_co_semis_std_mil is null) AND	
	(itkR.alertes_charges IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkR.alertes_charges is null)
UNION 

SELECT 
    'synthetise' as mode_saisie,
    --------------------------
	-- CONNEXION_SYNTHETISE --
	--------------------------
	cx.id as connexion_id,
    cx.cible_noeuds_synthetise_id as noeud_id,

    -------------
	-- CULTURE --
	-------------
	-- culture_*
	culture1.id as culture_id,
	culture1.nom as culture_nom,
	culture1.melange_especes as culture_est_melange_especes,
	culture1.melange_varietes as culture_est_melange_varietes,
	culture1."type" as culture_type,

	-- culture_typocan_*
	typoc1.typocan_culture_sans_compagne as culture_typo_can_sans_compagne,
	typoc1.typocan_espece as culture_typo_can_espece,
	typoc1.typocan_esp_sans_compagne as culture_typo_can_espece_sans_compagne,
	typoc1.nb_composant_culture as culture_typo_can_nbre_composant,
	typoc1.nb_typocan_esp as culture_typo_can_nbre_espece,

	-- culture_intermediaire_*
	cx_rst.culture_intermediaire_id as culture_intermediaire_id,
	culture_inter.nom as culture_intermediaire_nom,

	-- culture_intermediaire_typocan_*
	typoci.typocan_culture_sans_compagne as culture_intermerdiaire_typo_can_sans_compagne,
	typoci.typocan_espece as culture_intermerdiaire_typo_can_espece,
	typoci.nb_composant_culture as culture_intermerdiaire_typo_can_nbre_composant,

	-- culture_precedente_*
	culture0.id as culture_precedente_id,
	culture0.nom as culture_precedente_nom,
	culture0.melange_especes as culture_precedente_est_melange_especes,
	culture0.melange_varietes as culture_precedente_est_melange_varietes,
	culture0."type" as culture_precedente_type,

	-- culture_precedente_typocan_*
	typoc0.typocan_culture_sans_compagne as culture_precedente_typo_can_sans_compagne,
	typoc0.typocan_espece as culture_precedente_typo_can_espece,
	typoc0.nb_composant_culture as culture_precedente_typo_can_nbre_composant,

	---------
	-- SDC --
	---------
	sdc.id as sdc_id,
	sdc.code as sdc_code,
	sdc.nom as sdc_nom,
	sdc.code_dephy as sdc_numero_dephy,
	sdc.filiere as sdc_filiere,
	sdc.type_production as sdc_type_production,
	sdc.type_agriculture as sdc_type_agriculture,
	sdc.part_sau_domaine as sdc_part_sau_domaine,

	-- sdc_typo_*
	null as sdc_typo_surface_totale_assol_dvlp,
	null as sdc_typo_surface_totale_assol,
	-- sdc_typocan_*
	null as sdc_typo_can_assol_dvlp,
	null as sdc_typo_can_assol,
	-- sdc_typoculture_*
	null as sdc_typo_culture_liste_dvlp,
	null as sdc_typo_culture_liste,

	----------------
	-- DISPOSITIF --
	----------------
	sdc.dispositif_id as dispositif_id,
	dispo.code as dispositif_code,
	dispo.nom as dispositif_nom,
	dispo."type" as dispositif_type,

	-------------
	-- DOMAINE --
	-------------
	dom.id as domaine_id,
	dom.code as domaine_code,
	dom.nom as domaine_nom,
	dom.campagne as domaine_campagne,
	dom.siret as domaine_siret,
	dom.type_ferme as domaine_type_ferme,
	dom.departement as domaine_position_departement,
    dom.commune_id as domaine_position_commune_id,
    interop.codeinsee as domaine_position_code_insee,
	interop.safran_cell_id as domaine_position_cellule_safran,
	interop.rmqs_site_id as domaine_position_rmqs_site_id,
	dom.zonage as domaine_zonage,
	-- domaine_pct_*
	dom.pct_sau_zone_vulnerable as domaine_pct_sau_zone_vulnerable,
	dom.pct_sau_zone_excedent_structurel as domaine_pct_sau_zone_excedent_structurel,
	dom.pct_sau_zone_actions_complementaires as domaine_pct_sau_zone_actions_complementaires,
	dom.pct_sau_zone_natura_2000 as domaine_pct_sau_zone_natura_2000,
	dom.pct_sau_zone_erosion as domaine_pct_sau_zone_erosion,
	dom.pct_sau_perimetre_protection_captage as domaine_pct_sau_perimetre_protection_captage,
	dom.annee_naissance_exploitant as domaine_annee_naissance_exploitant,
	dom.cotisation_msa as domaine_cotisation_msa,
	dom.fermage_moyen as domaine_fermage_moyen,
	dom.aides_decouplees as domaine_aides_decouplees,
	dom.nombre_parcelles as domaine_nombre_parcelles,
	dom.distance_siege_parcelle_max as domaine_distance_siege_parcelle_max,
	-- domaine_parcelles_*
	dom.parcelles_groupees as domaine_parcelles_groupees,
	dom.parcelles_dispersees as domaine_parcelles_dispersees,
	dom.parcelles_plutot_dispersees as domaine_parcelles_plutot_dispersees,
	dom.parcelles_groupees_distinctes as domaine_parcelles_groupees_distinctes,
	dom.parcelles_plutot_groupees as domaine_parcelles_plutot_groupees,
	-- domaine_otex_* 
	dom.otex_18_nom as domaine_otex_18_nom,
	dom.otex_70_nom as domaine_otex_70_nom,
	dom.statut_juridique_nom as domaine_statut_juridique_nom,
	dom.objectifs as domaine_objectifs,
	dom.atouts_domaine as domaine_atouts,
	dom.contraintes_domaine as domaine_contraintes,
	dom.perspective_evolution_domaine as domaine_perspectives_evolution,
	-- domaine_membre_*
	dom.membre_cooperative as domaine_est_membre_cooperative,
	dom.membre_groupe_developpement as domaine_est_membre_groupe_developpement,
	dom.membre_cuma as domaine_est_membre_cuma,
	dom.domaine_touristique as domaine_est_touristique,
	-- domaine_main_oeuvre_*
	dom.main_oeuvre_exploitant as domaine_main_oeuvre_exploitant,
	dom.main_oeuvre_non_saisoniere as domaine_main_oeuvre_non_saisoniere,
	dom.main_oeuvre_saisoniere as domaine_main_oeuvre_saisoniere,
	dom.main_oeuvre_volontaire as domaine_main_oeuvre_volontaire,
	dom.sau_totale as domaine_sau,
	interop.typo_ruralite as domaine_typologie_ruralite,

    -----------------
	-- DOMAINE_SOL --
	-----------------
	-- domsol.id as domaine_sol_id,
	-- domsol.nom_local as domaine_sol_nom,
	-- domsol.sol_arvalis_id as domaine_sol_arvalis_id,

    ------------
	-- NOEUDS --
	------------
	nd_cible.fin_cycle as noeud_est_fin_cycle,
	nd_cible.memecampagne_noeudprecedent as noeud_est_meme_campagne_noeud_precedent,
    cx.source_noeuds_synthetise_id as noeud_precedent_id,
    nd_source.fin_cycle as noeud_precedent_est_fin_cycle,
	nd_source.memecampagne_noeudprecedent as noeud_precedent_est_meme_campagne_noeud_precedent,

    -----------------
	-- SYNTHETISE --
	----------------
	synth.id as synthetise_id, 
    typorota.typocan_rotation as synthetise_rotation_typo_can,
	typorota.list_freq_typoculture as synthetise_rotation_typo_liste_culture,
	synth.nom as synthetise_nom,
	synth.campagnes as synthetise_campagnes,
	case when pz0.pz0='pz0' then true else false end as synthetise_est_pz0,

	--typorota.frequence_total_rota as synthetise_rotation_frequence_totale,

    -------------
	-- REALISE --
	-------------
    null as zone_id,
    null as zone_code,
    null as zone_nom,
    null as zone_surface,
    null as parcelle_code,
    null as parcelle_nom,
    null as parcelle_commune_id,
    null as parcelle_sol_nom_ref,
    null as parcelle_import_edaplos,

    ---------------
	-- CONNEXION --
	---------------
	cx.frequence_source as connexion_frequence,
	cx.culture_absente as connexion_est_culture_absente,
	poidscx.poids_conx_agregation as connexion_poids_agregation,

	-----------------------------------
	-- NOEUDS_SYNTHETISE_PERFORMANCE --
	-----------------------------------

	-- ift_cible_non_mil_*
	itkS.ift_cible_non_mil_chimique_tot as itk_ift_cible_non_mil_chimique_tot,
	itkS.ift_cible_non_mil_chim_tot_hts as itk_ift_cible_non_mil_chim_tot_hts,
	itkS.ift_cible_non_mil_h as itk_ift_cible_non_mil_h,
	itkS.ift_cible_non_mil_f as itk_ift_cible_non_mil_f,
	itkS.ift_cible_non_mil_i as itk_ift_cible_non_mil_i,
	itkS.ift_cible_non_mil_ts as itk_ift_cible_non_mil_ts,
	itkS.ift_cible_non_mil_a as itk_ift_cible_non_mil_a,
	itkS.ift_cible_non_mil_hh as itk_ift_cible_non_mil_hh,
	itkS.ift_cible_non_mil_biocontrole as itk_ift_cible_non_mil_biocontrole,

	-- recours_*
	itkS.recours_aux_moyens_biologiques as itk_recours_aux_moyens_biologiques,
	itkS.recours_macroorganismes as itk_recours_macroorganismes,
	itkS.recours_produits_biotiques_sansamm as itk_recours_produits_biotiques_sans_amm,
	itkS.recours_produits_abiotiques_sansamm as itk_recours_produits_abiotiques_sans_amm,

	-- tps_*
	itkS.tps_utilisation_materiel as itk_tps_utilisation_materiel,
	itkS.tps_travail_manuel as itk_tps_travail_manuel,
	itkS.tps_travail_mecanise as itk_tps_travail_meca,
	itkS.tps_travail_total as itk_tps_travail_total,

	-- nbre_de_passages_*
	itkS.nbre_de_passages as itk_nbre_de_passages,
	itkS.nbre_de_passages_labour as itk_nbre_de_passages_labour,
	itkS.nbre_de_passages_tcs as itk_nbre_de_passages_tcs,
	itkS.nbre_de_passages_desherbage_meca as itk_nbre_de_passages_desherbage_meca,
	itkS.utili_desherbage_meca as itk_utili_desherbage_meca, -- TODO a suppr une fois que nbre_de_passages_desherbage_meca est débugué
	itkS.type_de_travail_du_sol as itk_type_de_travail_du_sol,
	
	-- co_std_mil_*
	itkS.co_tot_std_mil as itk_co_std_mil_tot,
	itkS.co_semis_std_mil as itk_co_std_mil_semis,
	itkS.co_fertimin_std_mil as itk_co_std_mil_fertimin,
	itkS.co_epandage_orga_std_mil as itk_co_std_mil_epandage_orga,
	itkS.co_phyto_sans_amm_std_mil as itk_co_std_mil_phyto_sans_amm,
	itkS.co_phyto_avec_amm_std_mil as itk_co_std_mil_phyto_avec_amm,
	itkS.co_trait_semence_std_mil as itk_co_std_mil_trait_semence,
	itkS.co_irrigation_std_mil as itk_co_std_mil_irrigation,
	itkS.co_intrants_autres_std_mil as itk_co_std_mil_intrants_autres,

	-- cm_std_mil
	itkS.cm_std_mil as itk_cm_std_mil,

	-- c_main_oeuvre_std_mil_*
	itkS.c_main_oeuvre_tot_std_mil as itk_c_main_oeuvre_std_mil_tot,
	itkS.c_main_oeuvre_tractoriste_std_mil as itk_c_main_oeuvre_std_mil_tractoriste,
	itkS.c_main_oeuvre_manuelle_std_mil as itk_c_main_oeuvre_std_mil_manuelle,

	-- pb_std_mil_*
	itkS.pb_std_mil_avec_autoconso as itk_pb_std_mil_avec_autoconso, -- Consigne pour ceux qui n'utilise pas les atelier d'élevage : avec auto
	itkS.pb_std_mil_sans_autoconso as itk_pb_std_mil_sans_autoconso,

	-- mb_std_mil_*
	itkS.mb_std_mil_avec_autoconso as itk_mb_std_mil_avec_autoconso,
	itkS.mb_std_mil_sans_autoconso as itk_mb_std_mil_sans_autoconso,

	-- msn_std_mil_*
	itkS.msn_std_mil_sans_autoconso as itk_msn_std_mil_sans_autoconso,
	itkS.msn_std_mil_avec_autoconso as itk_msn_std_mil_avec_autoconso,

	-- md_std_mil_*
	itkS.md_std_mil_sans_autoconso as itk_md_std_mil_sans_autoconso,
	itkS.md_std_mil_avec_autoconso as itk_md_std_mil_avec_autoconso,

	-- conso_* 
	itkS.conso_carburant as itk_conso_carburant,
	itkS.conso_eau as itk_conso_eau,

	-- ferti_*
	itkS.ferti_n_mineral as itk_ferti_n_mineral,
	itkS.ferti_n_organique as itk_ferti_n_organique,
	itkS.ferti_p2o5_mineral as itk_ferti_p2o5_mineral,
	itkS.ferti_p2o5_organique as itk_ferti_p2o5_organique,
	itkS.ferti_k2o_mineral as itk_ferti_k2o_mineral,
	itkS.ferti_k2o_organique as itk_ferti_k2o_organique,

	-- qsa_*
	itkS.qsa_tot_hts as itk_qsa_tot_hts,
	itkS.qsa_tot as itk_qsa_tot,
	itkS.qsa_danger_environnement_hts as itk_qsa_danger_environnement_hts,
	itkS.qsa_toxique_utilisateur_hts as itk_qsa_toxique_utilisateur_hts,
	itkS.qsa_cmr_hts as itk_qsa_cmr_hts,
	itkS.qsa_substances_candidates_substitution_hts as itk_qsa_substances_candidates_substitution_hts,
	itkS.qsa_substances_faible_risque_hts as itk_qsa_substances_faible_risque_hts,
	itkS.qsa_glyphosate_hts as itk_qsa_glyphosate_hts,
	itkS.qsa_chlortoluron_hts as itk_qsa_chlortoluron_hts,
	itkS.qsa_diflufenican_hts as itk_qsa_diflufenican_hts,
	itkS.qsa_prosulfocarbe_hts as itk_qsa_prosulfocarbe_hts,
	itkS.qsa_smetolachlore_hts as itk_qsa_smetolachlore_hts,
	itkS.qsa_boscalid_hts as itk_qsa_boscalid_hts,
	itkS.qsa_fluopyram_hts as itk_qsa_fluopyram_hts,
	itkS.qsa_lambda_cyhalothrine_hts as itk_qsa_lambda_cyhalothrine_hts,
	itkS.qsa_cuivre_tot_hts as itk_qsa_cuivre_tot_hts,
	itkS.qsa_cuivre_tot as itk_qsa_cuivre_tot,
	itkS.qsa_cuivre_phyto_hts as itk_qsa_cuivre_phyto_hts,
	itkS.qsa_cuivre_ferti as itk_qsa_cuivre_ferti,
	itkS.qsa_soufre_tot_hts as itk_qsa_soufre_tot_hts,
	itkS.qsa_soufre_phyto_hts as itk_qsa_soufre_phyto_hts,
	itkS.qsa_soufre_ferti as itk_qsa_soufre_ferti,
	itkS.qsa_bixafen as itk_qsa_bixafen,
	itkS.qsa_dicamba as itk_qsa_dicamba,
	itkS.qsa_mancozeb as itk_qsa_mancozeb,
	itkS.qsa_phosmet as itk_qsa_phosmet,
	itkS.qsa_tebuconazole as itk_qsa_tebuconazole,
	itkS.qsa_dimethenamidp as itk_qsa_dimethenamidp,
	itkS.qsa_pendimethalin as itk_qsa_pendimethalin,
	itkS.qsa_flufenacet as itk_qsa_flufenacet,
	itkS.qsa_aclonifen as itk_qsa_aclonifen,
	itkS.qsa_isoxaben as itk_qsa_isoxaben,
	itkS.qsa_beflutamid as itk_qsa_beflutamid,
	itkS.qsa_isoproturon as itk_qsa_isoproturon,
	itkS.qsa_clothianidine as itk_qsa_clothianidine,
	itkS.qsa_imidaclopride as itk_qsa_imidaclopride,
	itkS.qsa_thiamethoxam as itk_qsa_thiamethoxam,
	itkS.qsa_acetamipride as itk_qsa_acetamipride,
	itkS.qsa_thiaclopride as itk_qsa_thiaclopride,
	itkS.qsa_neonicotinoides as itk_qsa_neonicotinoides,
	itkS.qsa_abamectine_hts as itk_qsa_abamectine_hts,
	itkS.qsa_alpha_cypermethrine_hts as itk_qsa_alpha_cypermethrine_hts,
	itkS.qsa_azadirachtine_hts as itk_qsa_azadirachtine_hts,
	itkS.qsa_beta_cyfluthrine_hts as itk_qsa_beta_cyfluthrine_hts,
	itkS.qsa_chlorpyrifos_methyl_hts as itk_qsa_chlorpyrifos_methyl_hts,
	itkS.qsa_cyantraniliprole_hts as itk_qsa_cyantraniliprole_hts,
	itkS.qsa_cypermethrine_hts as itk_qsa_cypermethrine_hts,
	itkS.qsa_deltamethrine_hts as itk_qsa_deltamethrine_hts,
	itkS.qsa_dimethoate_hts as itk_qsa_dimethoate_hts,
	itkS.qsa_emamectine_hts as itk_qsa_emamectine_hts,
	itkS.qsa_esfenvalerate_hts as itk_qsa_esfenvalerate_hts,
	itkS.qsa_flonicamide_hts as itk_qsa_flonicamide_hts,
	itkS.qsa_huile_de_colza_hts as itk_qsa_huile_de_colza_hts,
	itkS.qsa_huile_de_paraffine_hts as itk_qsa_huile_de_paraffine_hts,
	itkS.qsa_indoxacarbe_hts as itk_qsa_indoxacarbe_hts,
	itkS.qsa_primicarbe_hts as itk_qsa_primicarbe_hts,
	itkS.qsa_pymetrozine_hts as itk_qsa_pymetrozine_hts,
	itkS.qsa_pyrethrine_hts as itk_qsa_pyrethrine_hts,
	itkS.qsa_silicate_aluminium_hts as itk_qsa_silicate_aluminium_hts,
	itkS.qsa_spinosad_hts as itk_qsa_spinosad_hts,
	itkS.qsa_spirotetramate_hts as itk_qsa_spirotetramate_hts,
	itkS.qsa_tau_fluvalinate_hts as itk_qsa_tau_fluvalinate_hts

FROM entrepot_itk_synthetise_performance AS itkS
LEFT JOIN entrepot_connection_synthetise AS cx ON cx.id = itkS.connection_synthetise_id 
LEFT JOIN entrepot_noeuds_synthetise AS nd_cible ON nd_cible.id = cx.cible_noeuds_synthetise_id    
LEFT JOIN entrepot_synthetise AS synth ON synth.id = nd_cible.synthetise_id
JOIN (
	SELECT * from entrepot_sdc as sdc 
	-- filtration sur les systèmes de cultures en grandes cultures et polyculture-élevage
	where sdc.filiere = 'POLYCULTURE_ELEVAGE' or sdc.filiere = 'GRANDES_CULTURES'
) sdc on sdc.id = synth.sdc_id
LEFT JOIN entrepot_connection_synthetise_restructure AS cx_rst ON cx_rst.id = itkS.connection_synthetise_id 
LEFT JOIN entrepot_poids_connexions_synthetise_rotation AS poidscx ON poidscx.connexion_id = itkS.connection_synthetise_id
LEFT JOIN entrepot_noeuds_synthetise AS nd_source ON nd_source.id = cx.source_noeuds_synthetise_id
LEFT JOIN entrepot_noeuds_synthetise_restructure AS nd_source_rst ON nd_source_rst.id = cx.source_noeuds_synthetise_id
LEFT JOIN entrepot_noeuds_synthetise_restructure AS nd_cible_rst ON nd_cible_rst.id = cx.cible_noeuds_synthetise_id
LEFT JOIN entrepot_dispositif AS dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine AS dom ON dom.id = dispo.domaine_id
LEFT JOIN entrepot_commune AS comm ON dom.commune_id = comm.id
LEFT JOIN entrepot_donnees_spatiales_commune_du_domaine AS interop ON interop.domaine_id = dom.id
LEFT JOIN entrepot_culture AS culture1 ON culture1.id = nd_cible_rst.culture_id 
LEFT JOIN entrepot_typologie_can_culture AS typoc1 ON typoc1.culture_id = nd_cible_rst.culture_id
LEFT JOIN entrepot_typologie_assol_can_realise AS typoassol ON typoassol.sdc_id = sdc.id
LEFT JOIN entrepot_culture AS culture0 ON culture0.id = nd_source_rst.culture_id 
LEFT JOIN entrepot_typologie_can_culture AS typoc0 ON typoc0.culture_id = nd_source_rst.culture_id 
LEFT JOIN entrepot_culture AS culture_i ON culture_i.id = cx_rst.culture_intermediaire_id 
LEFT JOIN entrepot_typologie_can_culture AS typo_ci ON typo_ci.culture_id = cx_rst.culture_intermediaire_id 
LEFT JOIN entrepot_typologie_can_rotation_synthetise AS typorota ON typorota.synthetise_id = synth.id
LEFT JOIN entrepot_culture AS culture_inter ON culture_inter.id = cx_rst.culture_intermediaire_id
LEFT JOIN entrepot_typologie_can_culture AS typoci ON  culture_inter.id = typoc1.culture_id
LEFT JOIN entrepot_identification_pz0 pz0 on pz0.entite_id = synth.id

WHERE
	(itkS.alerte_co_semis_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_co_semis_std_mil is null) AND 
	(itkS.alerte_ift_cible_non_mil_chim_tot_hts IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_ift_cible_non_mil_chim_tot_hts is null) AND 
	(itkS.alerte_ift_cible_non_mil_f IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_ift_cible_non_mil_f is null) AND	
	(itkS.alerte_ift_cible_non_mil_h IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_ift_cible_non_mil_h is null) AND	
	(itkS.alerte_ift_cible_non_mil_i IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_ift_cible_non_mil_i is null) AND	
	(itkS.alerte_ift_cible_non_mil_biocontrole IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_ift_cible_non_mil_biocontrole is null) AND	
	(itkS.alerte_co_irrigation_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_co_irrigation_std_mil is null) AND	
	(itkS.alerte_msn_std_mil_avec_autoconso IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_msn_std_mil_avec_autoconso is null) AND	
	(itkS.alerte_pb_std_mil_avec_autoconso IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_pb_std_mil_avec_autoconso is null) AND	
	(itkS.alerte_rendement IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_rendement is null) AND	
	(itkS.alerte_cm_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_cm_std_mil is null) AND	
	(itkS.alerte_co_semis_std_mil IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alerte_co_semis_std_mil is null) AND	
	(itkS.alertes_charges IN ('Pas d''alerte','Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') or itkS.alertes_charges is null);

--LEFT JOIN entrepot_domaine_sol AS domsol ON domsol.domaine_id = dom.id;