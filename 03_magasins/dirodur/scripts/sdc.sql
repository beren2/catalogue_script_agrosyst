----------------
-- SYNTHÉTISÉ --
----------------
SELECT 
	---------
	-- SDC --
	---------
	sdc.id as sdc_id,
	sdc.code as sdc_code,
	sdc.nom as sdc_nom,
	sdc.code_dephy as sdc_code_dephy,
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
	dom.sau_totale as domaine_sau_totale,
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
	interop.typo_ruralite as domaine_typologie_ruralite,

    -----------------
	-- DOMAINE_SOL --
	-----------------
	-- domsol.id as domaine_sol_id,
	-- domsol.nom_local as domaine_sol_nom,
	-- domsol.sol_arvalis_id as domaine_sol_arvalis_id,

    -----------------
	-- SYNTHETISE --
	----------------
	synth.id as synthetise_id,
    typorota.typocan_rotation as synthetise_rotation_typo_can,
	typorota.list_freq_typoculture as synthetise_rotation_typo_liste_culture,
	synth.nom as synthetise_nom,
	synth.campagnes as synthetise_campagnes,
	--typorota.frequence_total_rota as synthetise_rotation_frequence_totale,

	---------------------------------------
	-- SYNTHETISE_SYNTHETISE_PERFORMANCE --
	---------------------------------------

	-- ift_cible_non_mil_*
	ssp.ift_cible_non_mil_chimique_tot as sdc_ift_cible_non_mil_chimique_tot,
	ssp.ift_cible_non_mil_chim_tot_hts as sdc_ift_cible_non_mil_chim_tot_hts,
	ssp.ift_cible_non_mil_h as sdc_ift_cible_non_mil_h,
	ssp.ift_cible_non_mil_f as sdc_ift_cible_non_mil_f,
	ssp.ift_cible_non_mil_i as sdc_ift_cible_non_mil_i,
	ssp.ift_cible_non_mil_ts as sdc_ift_cible_non_mil_ts,
	ssp.ift_cible_non_mil_a as sdc_ift_cible_non_mil_a,
	ssp.ift_cible_non_mil_hh as sdc_ift_cible_non_mil_hh,
	ssp.ift_cible_non_mil_biocontrole as sdc_ift_cible_non_mil_biocontrole,

	-- recours_*
	ssp.recours_aux_moyens_biologiques as sdc_recours_aux_moyens_biologiques,
	ssp.recours_macroorganismes as sdc_recours_macroorganismes,
	ssp.recours_produits_biotiques_sansamm as sdc_recours_produits_biotiques_sans_amm,
	ssp.recours_produits_abiotiques_sansamm as sdc_recours_produits_abiotiques_sans_amm,

	-- tps_*
	ssp.tps_utilisation_materiel as sdc_tps_utilisation_materiel,
	ssp.tps_travail_manuel as sdc_tps_travail_manuel,
	ssp.tps_travail_mecanise as sdc_tps_travail_meca,
	ssp.tps_travail_total as sdc_tps_travail_total,

	-- nbre_de_passages_*
	ssp.nbre_de_passages as sdc_nbre_de_passages,
	ssp.nbre_de_passages_labour as sdc_nbre_de_passages_labour,
	ssp.nbre_de_passages_tcs as sdc_nbre_de_passages_tcs,
	ssp.nbre_de_passages_desherbage_meca as sdc_nbre_de_passages_desherbage_meca,
	ssp.utili_desherbage_meca as sdc_utili_desherbage_meca, -- TODO a suppr une fois que nbre_de_passages_desherbage_meca est débugué
	ssp.type_de_travail_du_sol as sdc_type_de_travail_du_sol,
	
	-- co_std_mil_*
	ssp.co_tot_std_mil as sdc_co_std_mil_tot,
	ssp.co_semis_std_mil as sdc_co_std_mil_semis,
	ssp.co_fertimin_std_mil as sdc_co_std_mil_fertimin,
	ssp.co_epandage_orga_std_mil as sdc_co_std_mil_epandage_orga,
	ssp.co_phyto_sans_amm_std_mil as sdc_co_std_mil_phyto_sans_amm,
	ssp.co_phyto_avec_amm_std_mil as sdc_co_std_mil_phyto_avec_amm,
	ssp.co_trait_semence_std_mil as sdc_co_std_mil_trait_semence,
	ssp.co_irrigation_std_mil as sdc_co_std_mil_irrigation,
	ssp.co_intrants_autres_std_mil as sdc_co_std_mil_intrants_autres,

	-- cm_std_mil
	ssp.cm_std_mil as sdc_cm_std_mil,

	-- c_main_oeuvre_std_mil_*
	ssp.c_main_oeuvre_tot_std_mil as sdc_c_main_oeuvre_std_mil_tot,
	ssp.c_main_oeuvre_tractoriste_std_mil as sdc_c_main_oeuvre_std_mil_tractoriste,
	ssp.c_main_oeuvre_manuelle_std_mil as sdc_c_main_oeuvre_std_mil_manuelle,

	-- pb_std_mil_*
	ssp.pb_std_mil_avec_autoconso as sdc_pb_std_mil_avec_autoconso, -- Consigne pour ceux qui n'utilise pas les atelier d'élevage : avec auto
	ssp.pb_std_mil_sans_autoconso as sdc_pb_std_mil_sans_autoconso,

	-- mb_std_mil_*
	ssp.mb_std_mil_avec_autoconso as sdc_mb_std_mil_avec_autoconso,
	ssp.mb_std_mil_sans_autoconso as sdc_mb_std_mil_sans_autoconso,

	-- msn_std_mil_*
	ssp.msn_std_mil_sans_autoconso as sdc_msn_std_mil_sans_autoconso,
	ssp.msn_std_mil_avec_autoconso as sdc_msn_std_mil_avec_autoconso,

	-- md_std_mil_*
	ssp.md_std_mil_sans_autoconso as sdc_md_std_mil_sans_autoconso,
	ssp.md_std_mil_avec_autoconso as sdc_md_std_mil_avec_autoconso,

	-- conso_* 
	ssp.conso_carburant as sdc_conso_carburant,
	ssp.conso_eau as sdc_conso_eau,

	-- ferti_*
	ssp.ferti_n_mineral as sdc_ferti_n_mineral,
	ssp.ferti_n_organique as sdc_ferti_n_organique,
	ssp.ferti_p2o5_mineral as sdc_ferti_p2o5_mineral,
	ssp.ferti_p2o5_organique as sdc_ferti_p2o5_organique,
	ssp.ferti_k2o_mineral as sdc_ferti_k2o_mineral,
	ssp.ferti_k2o_organique as sdc_ferti_k2o_organique,

	-- qsa_*
	ssp.qsa_tot_hts as sdc_qsa_tot_hts,
	ssp.qsa_tot as sdc_qsa_tot,
	ssp.qsa_danger_environnement_hts as sdc_qsa_danger_environnement_hts,
	ssp.qsa_toxique_utilisateur_hts as sdc_qsa_toxique_utilisateur_hts,
	ssp.qsa_cmr_hts as sdc_qsa_cmr_hts,
	ssp.qsa_substances_candidates_substitution_hts as sdc_qsa_substances_candidates_substitution_hts,
	ssp.qsa_substances_faible_risque_hts as sdc_qsa_substances_faible_risque_hts,
	ssp.qsa_glyphosate_hts as sdc_qsa_glyphosate_hts,
	ssp.qsa_chlortoluron_hts as sdc_qsa_chlortoluron_hts,
	ssp.qsa_diflufenican_hts as sdc_qsa_diflufenican_hts,
	ssp.qsa_prosulfocarbe_hts as sdc_qsa_prosulfocarbe_hts,
	ssp.qsa_smetolachlore_hts as sdc_qsa_smetolachlore_hts,
	ssp.qsa_boscalid_hts as sdc_qsa_boscalid_hts,
	ssp.qsa_fluopyram_hts as sdc_qsa_fluopyram_hts,
	ssp.qsa_lambda_cyhalothrine_hts as sdc_qsa_lambda_cyhalothrine_hts,
	ssp.qsa_cuivre_tot_hts as sdc_qsa_cuivre_tot_hts,
	ssp.qsa_cuivre_tot as sdc_qsa_cuivre_tot,
	ssp.qsa_cuivre_phyto_hts as sdc_qsa_cuivre_phyto_hts,
	ssp.qsa_cuivre_ferti as sdc_qsa_cuivre_ferti,
	ssp.qsa_soufre_tot_hts as sdc_qsa_soufre_tot_hts,
	ssp.qsa_soufre_phyto_hts as sdc_qsa_soufre_phyto_hts,
	ssp.qsa_soufre_ferti as sdc_qsa_soufre_ferti,
	ssp.qsa_bixafen as sdc_qsa_bixafen,
	ssp.qsa_dicamba as sdc_qsa_dicamba,
	ssp.qsa_mancozeb as sdc_qsa_mancozeb,
	ssp.qsa_phosmet as sdc_qsa_phosmet,
	ssp.qsa_tebuconazole as sdc_qsa_tebuconazole,
	ssp.qsa_dimethenamidp as sdc_qsa_dimethenamidp,
	ssp.qsa_pendimethalin as sdc_qsa_pendimethalin,
	ssp.qsa_flufenacet as sdc_qsa_flufenacet,
	ssp.qsa_aclonifen as sdc_qsa_aclonifen,
	ssp.qsa_isoxaben as sdc_qsa_isoxaben,
	ssp.qsa_beflutamid as sdc_qsa_beflutamid,
	ssp.qsa_isoproturon as sdc_qsa_isoproturon,
	ssp.qsa_clothianidine as sdc_qsa_clothianidine,
	ssp.qsa_imidaclopride as sdc_qsa_imidaclopride,
	ssp.qsa_thiamethoxam as sdc_qsa_thiamethoxam,
	ssp.qsa_acetamipride as sdc_qsa_acetamipride,
	ssp.qsa_thiaclopride as sdc_qsa_thiaclopride,
	ssp.qsa_neonicotinoides as sdc_qsa_neonicotinoides,
	ssp.qsa_abamectine_hts as sdc_qsa_abamectine_hts,
	ssp.qsa_alpha_cypermethrine_hts as sdc_qsa_alpha_cypermethrine_hts,
	ssp.qsa_azadirachtine_hts as sdc_qsa_azadirachtine_hts,
	ssp.qsa_beta_cyfluthrine_hts as sdc_qsa_beta_cyfluthrine_hts,
	ssp.qsa_chlorpyrifos_methyl_hts as sdc_qsa_chlorpyrifos_methyl_hts,
	ssp.qsa_cyantraniliprole_hts as sdc_qsa_cyantraniliprole_hts,
	ssp.qsa_cypermethrine_hts as sdc_qsa_cypermethrine_hts,
	ssp.qsa_deltamethrine_hts as sdc_qsa_deltamethrine_hts,
	ssp.qsa_dimethoate_hts as sdc_qsa_dimethoate_hts,
	ssp.qsa_emamectine_hts as sdc_qsa_emamectine_hts,
	ssp.qsa_esfenvalerate_hts as sdc_qsa_esfenvalerate_hts,
	ssp.qsa_flonicamide_hts as sdc_qsa_flonicamide_hts,
	ssp.qsa_huile_de_colza_hts as sdc_qsa_huile_de_colza_hts,
	ssp.qsa_huile_de_paraffine_hts as sdc_qsa_huile_de_paraffine_hts,
	ssp.qsa_indoxacarbe_hts as sdc_qsa_indoxacarbe_hts,
	ssp.qsa_primicarbe_hts as sdc_qsa_primicarbe_hts,
	ssp.qsa_pymetrozine_hts as sdc_qsa_pymetrozine_hts,
	ssp.qsa_pyrethrine_hts as sdc_qsa_pyrethrine_hts,
	ssp.qsa_silicate_aluminium_hts as sdc_qsa_silicate_aluminium_hts,
	ssp.qsa_spinosad_hts as sdc_qsa_spinosad_hts,
	ssp.qsa_spirotetramate_hts as sdc_qsa_spirotetramate_hts,
	ssp.qsa_tau_fluvalinate_hts as sdc_qsa_tau_fluvalinate_hts

FROM entrepot_sdc AS sdc
JOIN (
	SELECT * FROM entrepot_entite_unique_par_sdc_nettoyage sub_sdc
	WHERE sub_sdc.entite_retenue NOT LIKE 'realise_retenu'
) AS sub_sdc ON sdc.id = sub_sdc.sdc_id	
LEFT JOIN entrepot_dispositif AS dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine AS dom ON dom.id = dispo.domaine_id
LEFT JOIN entrepot_commune AS comm ON dom.commune_id = comm.id
LEFT JOIN entrepot_donnees_spatiales_commune_du_domaine AS interop ON interop.domaine_id = dom.id
LEFT JOIN entrepot_synthetise_synthetise_performance AS ssp ON sub_sdc.entite_retenue = ssp.synthetise_id
LEFT JOIN entrepot_synthetise AS synth ON synth.id = sub_sdc.entite_retenue
LEFT JOIN entrepot_typologie_can_rotation_synthetise AS typorota ON typorota.synthetise_id = synth.id
-- filtration sur les systèmes de cultures en grandes cultures et polyculture-élevage
--LEFT JOIN entrepot_domaine_sol AS domsol ON domsol.domaine_id = dom.id
WHERE
	(sdc.filiere = 'POLYCULTURE_ELEVAGE' OR sdc.filiere = 'GRANDES_CULTURES') AND
	(ssp.alerte_co_semis_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_co_semis_std_mil is null) AND 
	(ssp.alerte_ift_cible_non_mil_chim_tot_hts IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_ift_cible_non_mil_chim_tot_hts is null) AND 
	(ssp.alerte_ift_cible_non_mil_f IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_ift_cible_non_mil_f is null) AND	
	(ssp.alerte_ift_cible_non_mil_h IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_ift_cible_non_mil_h is null) AND	
	(ssp.alerte_ift_cible_non_mil_i IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_ift_cible_non_mil_i is null) AND	
	(ssp.alerte_ift_cible_non_mil_biocontrole IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_ift_cible_non_mil_biocontrole is null) AND	
	(ssp.alerte_co_irrigation_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_co_irrigation_std_mil is null) AND	
	(ssp.alerte_msn_std_mil_avec_autoconso IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_msn_std_mil_avec_autoconso is null) AND	
	(ssp.alerte_pb_std_mil_avec_autoconso IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_pb_std_mil_avec_autoconso is null) AND	
	(ssp.alerte_rendement IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_rendement is null) AND	
	(ssp.alerte_cm_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_cm_std_mil is null) AND	
	(ssp.alerte_co_semis_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_co_semis_std_mil is null) AND	
	(ssp.alerte_tps_travail_total IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alerte_tps_travail_total is null) AND	
	(ssp.alertes_charges IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR ssp.alertes_charges is null)

UNION
-------------
-- RÉALISÉ --
-------------
----------------
-- SYNTHÉTISÉ --
----------------
SELECT 
	---------
	-- SDC --
	---------
	sdc.id as sdc_id,
	sdc.code as sdc_code,
	sdc.nom as sdc_nom,
	sdc.code_dephy as sdc_code_dephy,
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
	typoassol.list_freq_typoculture_dvlp  as sdc_typoculture_liste_dvlp,
	typoassol.list_freq_typoculture as sdc_typoculture_liste,

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
	dom.sau_totale as domaine_sau_totale,
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
	interop.typo_ruralite as domaine_typologie_ruralite,

    -----------------
	-- DOMAINE_SOL --
	-----------------
	-- domsol.id as domaine_sol_id,
	-- domsol.nom_local as domaine_sol_nom,
	-- domsol.sol_arvalis_id as domaine_sol_arvalis_id,

    -----------------
	-- SYNTHETISE --
	----------------
	null as synthetise_id,
    null as synthetise_rotation_typo_can,
	null as synthetise_rotation_typo_liste_culture,
	null as synthetise_nom,
	null as synthetise_campagnes,
	--typorota.frequence_total_rota as synthetise_rotation_frequence_totale,

	---------------------------------------
	-- SYNTHETISE_SYNTHETISE_PERFORMANCE --
	---------------------------------------

	-- ift_cible_non_mil_*
	srp.ift_cible_non_mil_chimique_tot as sdc_ift_cible_non_mil_chimique_tot,
	srp.ift_cible_non_mil_chim_tot_hts as sdc_ift_cible_non_mil_chim_tot_hts,
	srp.ift_cible_non_mil_h as sdc_ift_cible_non_mil_h,
	srp.ift_cible_non_mil_f as sdc_ift_cible_non_mil_f,
	srp.ift_cible_non_mil_i as sdc_ift_cible_non_mil_i,
	srp.ift_cible_non_mil_ts as sdc_ift_cible_non_mil_ts,
	srp.ift_cible_non_mil_a as sdc_ift_cible_non_mil_a,
	srp.ift_cible_non_mil_hh as sdc_ift_cible_non_mil_hh,
	srp.ift_cible_non_mil_biocontrole as sdc_ift_cible_non_mil_biocontrole,

	-- recours_*
	srp.recours_aux_moyens_biologiques as sdc_recours_aux_moyens_biologiques,
	srp.recours_macroorganismes as sdc_recours_macroorganismes,
	srp.recours_produits_biotiques_sansamm as sdc_recours_produits_biotiques_sans_amm,
	srp.recours_produits_abiotiques_sansamm as sdc_recours_produits_abiotiques_sans_amm,

	-- tps_*
	srp.tps_utilisation_materiel as sdc_tps_utilisation_materiel,
	srp.tps_travail_manuel as sdc_tps_travail_manuel,
	srp.tps_travail_mecanise as sdc_tps_travail_meca,
	srp.tps_travail_total as sdc_tps_travail_total,

	-- nbre_de_passages_*
	srp.nbre_de_passages as sdc_nbre_de_passages,
	srp.nbre_de_passages_labour as sdc_nbre_de_passages_labour,
	srp.nbre_de_passages_tcs as sdc_nbre_de_passages_tcs,
	srp.nbre_de_passages_desherbage_meca as sdc_nbre_de_passages_desherbage_meca,
	srp.utili_desherbage_meca as noeud_utili_desherbage_meca, -- TODO a suppr une fois que nbre_de_passages_desherbage_meca est débugué
	srp.type_de_travail_du_sol as noeud_type_de_travail_du_sol,
	
	-- co_std_mil_*
	srp.co_tot_std_mil as sdc_co_std_mil_tot,
	srp.co_semis_std_mil as sdc_co_std_mil_semis,
	srp.co_fertimin_std_mil as sdc_co_std_mil_fertimin,
	srp.co_epandage_orga_std_mil as sdc_co_std_mil_epandage_orga,
	srp.co_phyto_sans_amm_std_mil as sdc_co_std_mil_phyto_sans_amm,
	srp.co_phyto_avec_amm_std_mil as sdc_co_std_mil_phyto_avec_amm,
	srp.co_trait_semence_std_mil as sdc_co_std_mil_trait_semence,
	srp.co_irrigation_std_mil as sdc_co_std_mil_irrigation,
	srp.co_intrants_autres_std_mil as sdc_co_std_mil_intrants_autres,

	-- cm_std_mil
	srp.cm_std_mil as sdc_cm_std_mil,

	-- c_main_oeuvre_std_mil_*
	srp.c_main_oeuvre_tot_std_mil as sdc_c_main_oeuvre_std_mil_tot,
	srp.c_main_oeuvre_tractoriste_std_mil as sdc_c_main_oeuvre_std_mil_tractoriste,
	srp.c_main_oeuvre_manuelle_std_mil as sdc_c_main_oeuvre_std_mil_manuelle,

	-- pb_std_mil_*
	srp.pb_std_mil_avec_autoconso as sdc_pb_std_mil_avec_autoconso, -- Consigne pour ceux qui n'utilise pas les atelier d'élevage : avec auto
	srp.pb_std_mil_sans_autoconso as sdc_pb_std_mil_sans_autoconso,

	-- mb_std_mil_*
	srp.mb_std_mil_avec_autoconso as sdc_mb_std_mil_avec_autoconso,
	srp.mb_std_mil_sans_autoconso as sdc_mb_std_mil_sans_autoconso,

	-- msn_std_mil_*
	srp.msn_std_mil_sans_autoconso as sdc_msn_std_mil_sans_autoconso,
	srp.msn_std_mil_avec_autoconso as sdc_msn_std_mil_avec_autoconso,

	-- md_std_mil_*
	srp.md_std_mil_sans_autoconso as sdc_md_std_mil_sans_autoconso,
	srp.md_std_mil_avec_autoconso as sdc_md_std_mil_avec_autoconso,

	-- conso_* 
	srp.conso_carburant as sdc_conso_carburant,
	srp.conso_eau as sdc_conso_eau,

	-- ferti_*
	srp.ferti_n_mineral as sdc_ferti_n_mineral,
	srp.ferti_n_organique as sdc_ferti_n_organique,
	srp.ferti_p2o5_mineral as sdc_ferti_p2o5_mineral,
	srp.ferti_p2o5_organique as sdc_ferti_p2o5_organique,
	srp.ferti_k2o_mineral as sdc_ferti_k2o_mineral,
	srp.ferti_k2o_organique as sdc_ferti_k2o_organique,

	-- qsa_*
	srp.qsa_tot_hts as sdc_qsa_tot_hts,
	srp.qsa_tot as sdc_qsa_tot,
	srp.qsa_danger_environnement_hts as sdc_qsa_danger_environnement_hts,
	srp.qsa_toxique_utilisateur_hts as sdc_qsa_toxique_utilisateur_hts,
	srp.qsa_cmr_hts as sdc_qsa_cmr_hts,
	srp.qsa_substances_candidates_substitution_hts as sdc_qsa_substances_candidates_substitution_hts,
	srp.qsa_substances_faible_risque_hts as sdc_qsa_substances_faible_risque_hts,
	srp.qsa_glyphosate_hts as sdc_qsa_glyphosate_hts,
	srp.qsa_chlortoluron_hts as sdc_qsa_chlortoluron_hts,
	srp.qsa_diflufenican_hts as sdc_qsa_diflufenican_hts,
	srp.qsa_prosulfocarbe_hts as sdc_qsa_prosulfocarbe_hts,
	srp.qsa_smetolachlore_hts as sdc_qsa_smetolachlore_hts,
	srp.qsa_boscalid_hts as sdc_qsa_boscalid_hts,
	srp.qsa_fluopyram_hts as sdc_qsa_fluopyram_hts,
	srp.qsa_lambda_cyhalothrine_hts as sdc_qsa_lambda_cyhalothrine_hts,
	srp.qsa_cuivre_tot_hts as sdc_qsa_cuivre_tot_hts,
	srp.qsa_cuivre_tot as sdc_qsa_cuivre_tot,
	srp.qsa_cuivre_phyto_hts as sdc_qsa_cuivre_phyto_hts,
	srp.qsa_cuivre_ferti as sdc_qsa_cuivre_ferti,
	srp.qsa_soufre_tot_hts as sdc_qsa_soufre_tot_hts,
	srp.qsa_soufre_phyto_hts as sdc_qsa_soufre_phyto_hts,
	srp.qsa_soufre_ferti as sdc_qsa_soufre_ferti,
	srp.qsa_bixafen as sdc_qsa_bixafen,
	srp.qsa_dicamba as sdc_qsa_dicamba,
	srp.qsa_mancozeb as sdc_qsa_mancozeb,
	srp.qsa_phosmet as sdc_qsa_phosmet,
	srp.qsa_tebuconazole as sdc_qsa_tebuconazole,
	srp.qsa_dimethenamidp as sdc_qsa_dimethenamidp,
	srp.qsa_pendimethalin as sdc_qsa_pendimethalin,
	srp.qsa_flufenacet as sdc_qsa_flufenacet,
	srp.qsa_aclonifen as sdc_qsa_aclonifen,
	srp.qsa_isoxaben as sdc_qsa_isoxaben,
	srp.qsa_beflutamid as sdc_qsa_beflutamid,
	srp.qsa_isoproturon as sdc_qsa_isoproturon,
	srp.qsa_clothianidine as sdc_qsa_clothianidine,
	srp.qsa_imidaclopride as sdc_qsa_imidaclopride,
	srp.qsa_thiamethoxam as sdc_qsa_thiamethoxam,
	srp.qsa_acetamipride as sdc_qsa_acetamipride,
	srp.qsa_thiaclopride as sdc_qsa_thiaclopride,
	srp.qsa_neonicotinoides as sdc_qsa_neonicotinoides,
	srp.qsa_abamectine_hts as sdc_qsa_abamectine_hts,
	srp.qsa_alpha_cypermethrine_hts as sdc_qsa_alpha_cypermethrine_hts,
	srp.qsa_azadirachtine_hts as sdc_qsa_azadirachtine_hts,
	srp.qsa_beta_cyfluthrine_hts as sdc_qsa_beta_cyfluthrine_hts,
	srp.qsa_chlorpyrifos_methyl_hts as sdc_qsa_chlorpyrifos_methyl_hts,
	srp.qsa_cyantraniliprole_hts as sdc_qsa_cyantraniliprole_hts,
	srp.qsa_cypermethrine_hts as sdc_qsa_cypermethrine_hts,
	srp.qsa_deltamethrine_hts as sdc_qsa_deltamethrine_hts,
	srp.qsa_dimethoate_hts as sdc_qsa_dimethoate_hts,
	srp.qsa_emamectine_hts as sdc_qsa_emamectine_hts,
	srp.qsa_esfenvalerate_hts as sdc_qsa_esfenvalerate_hts,
	srp.qsa_flonicamide_hts as sdc_qsa_flonicamide_hts,
	srp.qsa_huile_de_colza_hts as sdc_qsa_huile_de_colza_hts,
	srp.qsa_huile_de_paraffine_hts as sdc_qsa_huile_de_paraffine_hts,
	srp.qsa_indoxacarbe_hts as sdc_qsa_indoxacarbe_hts,
	srp.qsa_primicarbe_hts as sdc_qsa_primicarbe_hts,
	srp.qsa_pymetrozine_hts as sdc_qsa_pymetrozine_hts,
	srp.qsa_pyrethrine_hts as sdc_qsa_pyrethrine_hts,
	srp.qsa_silicate_aluminium_hts as sdc_qsa_silicate_aluminium_hts,
	srp.qsa_spinosad_hts as sdc_qsa_spinosad_hts,
	srp.qsa_spirotetramate_hts as sdc_qsa_spirotetramate_hts,
	srp.qsa_tau_fluvalinate_hts as sdc_qsa_tau_fluvalinate_hts

FROM entrepot_sdc AS sdc
JOIN (
	SELECT * FROM entrepot_entite_unique_par_sdc_nettoyage sub_sdc
	WHERE sub_sdc.entite_retenue LIKE 'realise_retenu'
) AS sub_sdc ON sdc.id = sub_sdc.sdc_id	
LEFT JOIN entrepot_dispositif AS dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine AS dom ON dom.id = dispo.domaine_id
LEFT JOIN entrepot_commune AS comm ON dom.commune_id = comm.id
LEFT JOIN entrepot_donnees_spatiales_commune_du_domaine AS interop ON interop.domaine_id = dom.id
LEFT JOIN entrepot_typologie_assol_can_realise AS typoassol ON typoassol.sdc_id = sdc.id
LEFT JOIN entrepot_sdc_realise_performance AS srp ON sdc.id = srp.sdc_id
-- filtration sur les systèmes de cultures en grandes cultures et polyculture-élevage
WHERE
	(sdc.filiere = 'POLYCULTURE_ELEVAGE' OR sdc.filiere = 'GRANDES_CULTURES') AND
	(srp.alerte_co_semis_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_co_semis_std_mil is null) AND 
	(srp.alerte_ift_cible_non_mil_chim_tot_hts IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_ift_cible_non_mil_chim_tot_hts is null) AND 
	(srp.alerte_ift_cible_non_mil_f IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_ift_cible_non_mil_f is null) AND	
	(srp.alerte_ift_cible_non_mil_h IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_ift_cible_non_mil_h is null) AND	
	(srp.alerte_ift_cible_non_mil_i IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_ift_cible_non_mil_i is null) AND	
	(srp.alerte_ift_cible_non_mil_biocontrole IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_ift_cible_non_mil_biocontrole is null) AND	
	(srp.alerte_co_irrigation_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_co_irrigation_std_mil is null) AND	
	(srp.alerte_msn_std_mil_avec_autoconso IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_msn_std_mil_avec_autoconso is null) AND	
	(srp.alerte_pb_std_mil_avec_autoconso IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_pb_std_mil_avec_autoconso is null) AND	
	(srp.alerte_rendement IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_rendement is null) AND	
	(srp.alerte_cm_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_cm_std_mil is null) AND	
	(srp.alerte_co_semis_std_mil IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_co_semis_std_mil is null) AND	
	(srp.alerte_tps_travail_total IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alerte_tps_travail_total is null) AND	
	(srp.alertes_charges IN ('Pas d''alerte', 'Cette alerte n''existe pas dans cette filière', 'Cette alerte n''existe pas encore dans cette filière') OR srp.alertes_charges is null);
--LEFT JOIN entrepot_domaine_sol AS domsol ON domsol.domaine_id = dom.id;






