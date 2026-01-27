SELECT
	--------------------------------
	-- NOEUDS_REALISE_PERFORMANCE --
	--------------------------------

	-- ift_cible_non_mil_*
	itkR.ift_cible_non_mil_chimique_tot,
	itkR.ift_cible_non_mil_chim_tot_hts,
	itkR.ift_cible_non_mil_h,
	itkR.ift_cible_non_mil_f,
	itkR.ift_cible_non_mil_i,
	itkR.ift_cible_non_mil_ts,
	itkR.ift_cible_non_mil_a,
	itkR.ift_cible_non_mil_hh,
	itkR.ift_cible_non_mil_biocontrole,

	-- recours_*
	itkR.recours_aux_moyens_biologiques,
	itkR.recours_macroorganismes,
	itkR.recours_produits_biotiques_sansamm,
	itkR.recours_produits_abiotiques_sansamm,

	-- tps_*
	itkR.tps_utilisation_materiel,
	itkR.tps_travail_manuel,
	itkR.tps_travail_mecanise,
	itkR.tps_travail_total,

	-- nbre_de_passages_*
	itkR.nbre_de_passages,
	itkR.nbre_de_passages_labour,
	itkR.nbre_de_passages_tcs,
	itkR.nbre_de_passages_desherbage_meca,
	itkR.utili_desherbage_meca, -- TODO a suppr une fois que nbre_de_passages_desherbage_meca est débugué
	itkR.type_de_travail_du_sol,

	-- co_std_mil_*
	itkR.co_tot_std_mil as co_std_mil_tot,
	itkR.co_semis_std_mil as co_std_mil_semis,
	itkR.co_fertimin_std_mil as co_std_mil_fertimin,
	itkR.co_epandage_orga_std_mil as co_std_mil_epandage,
	itkR.co_phyto_sans_amm_std_mil as co_std_mil_phyto_sans_amm,
	itkR.co_phyto_avec_amm_std_mil as co_std_mil_phyto_avec_amm,
	itkR.co_trait_semence_std_mil as co_std_mil_trait_semence,
	itkR.co_irrigation_std_mil as co_std_mil_irrigation,
	itkR.co_intrants_autres_std_mil as co_std_mil_intrants_autres,

	-- cm_std_mil
	itkR.cm_std_mil,

	-- c_main_oeuvre_std_mil_*
	itkR.c_main_oeuvre_tot_std_mil as c_main_oeuvre_std_mil_tot,
	itkR.c_main_oeuvre_tractoriste_std_mil as c_main_oeuvre_std_mil_tractoriste,
	itkR.c_main_oeuvre_manuelle_std_mil as c_main_oeuvre_std_mil_manuelle,

	-- pb_std_mil_*
	itkR.pb_std_mil_avec_autoconso, -- Consigne pour ceux qui n'utilise pas les atelier d'élevage : avec auto
	itkR.pb_std_mil_sans_autoconso,

	-- mb_std_mil_*
	itkR.mb_std_mil_avec_autoconso,
	itkR.mb_std_mil_sans_autoconso,

	-- msn_std_mil_*
	itkR.msn_std_mil_sans_autoconso,
	itkR.msn_std_mil_avec_autoconso,

	-- md_std_mil_*
	itkR.md_std_mil_sans_autoconso,
	itkR.md_std_mil_avec_autoconso,

	-- conso_* 
	itkR.conso_carburant,
	itkR.conso_eau,

	-- ferti_*
	itkR.ferti_n_mineral,
	itkR.ferti_n_organique,
	itkR.ferti_p2o5_mineral,
	itkR.ferti_p2o5_organique,
	itkR.ferti_k2o_mineral,
	itkR.ferti_k2o_organique,

	-- qsa_*
	itkR.qsa_tot_hts,
	itkR.qsa_tot,
	itkR.qsa_danger_environnement_hts ,
	itkR.qsa_toxique_utilisateur_hts ,
	itkR.qsa_cmr_hts ,
	itkR.qsa_substances_candidates_substitution_hts ,
	itkR.qsa_substances_faible_risque_hts ,
	itkR.qsa_glyphosate_hts ,
	itkR.qsa_chlortoluron_hts ,
	itkR.qsa_diflufenican_hts ,
	itkR.qsa_prosulfocarbe_hts ,
	itkR.qsa_smetolachlore_hts ,
	itkR.qsa_boscalid_hts ,
	itkR.qsa_fluopyram_hts ,
	itkR.qsa_lambda_cyhalothrine_hts ,
	itkR.qsa_cuivre_tot_hts ,
	itkR.qsa_cuivre_tot,
	itkR.qsa_cuivre_phyto_hts ,
	itkR.qsa_cuivre_ferti,
	itkR.qsa_soufre_tot_hts,
	itkR.qsa_soufre_phyto_hts,
	itkR.qsa_soufre_ferti,
	itkR.qsa_bixafen,
	itkR.qsa_dicamba,
	itkR.qsa_mancozeb,
	itkR.qsa_phosmet,
	itkR.qsa_tebuconazole,
	itkR.qsa_dimethenamidp,
	itkR.qsa_pendimethalin,
	itkR.qsa_flufenacet,
	itkR.qsa_aclonifen,
	itkR.qsa_isoxaben,
	itkR.qsa_beflutamid,
	itkR.qsa_isoproturon,
	itkR.qsa_clothianidine,
	itkR.qsa_imidaclopride,
	itkR.qsa_thiamethoxam,
	itkR.qsa_acetamipride,
	itkR.qsa_thiaclopride,
	itkR.qsa_neonicotinoides,
	itkR.qsa_abamectine_hts,
	itkR.qsa_alpha_cypermethrine_hts,
	itkR.qsa_azadirachtine_hts,
	itkR.qsa_beta_cyfluthrine_hts,
	itkR.qsa_chlorpyrifos_methyl_hts,
	itkR.qsa_cyantraniliprole_hts,
	itkR.qsa_cypermethrine_hts,
	itkR.qsa_deltamethrine_hts,
	itkR.qsa_dimethoate_hts,
	itkR.qsa_emamectine_hts,
	itkR.qsa_esfenvalerate_hts,
	itkR.qsa_flonicamide_hts,
	itkR.qsa_huile_de_colza_hts,
	itkR.qsa_huile_de_paraffine_hts,
	itkR.qsa_indoxacarbe_hts,
	itkR.qsa_primicarbe_hts,
	itkR.qsa_pymetrozine_hts,
	itkR.qsa_pyrethrine_hts,
	itkR.qsa_silicate_aluminium_hts,
	itkR.qsa_spinosad_hts,
	itkR.qsa_spirotetramate_hts,
	itkR.qsa_tau_fluvalinate_hts,

	--------------------
	-- NOEUDS_REALISE --
	--------------------
	itkR.itk_realise_id,

	--------------------------------
	-- NOEUDS_REALISE_RESTRUCTURE --
	--------------------------------
	node_res.precedent_noeuds_realise_id as itk_precedent_id,

	-------------
	-- CULTURE --
	-------------
	-- culture_*
	culture1.id as culture_id,
	culture1.nom as culture_nom,
	culture1.melange_especes as culture_melange_especes,
	culture1.melange_varietes as culture_melange_varietes,
	culture1.code as culture_code,
	culture1."type" as culture_type,

	-- culture_typocan_*
	typoc1.typocan_culture_sans_compagne as culture_typocan_sans_compagne,
	typoc1.typocan_espece as culture_typocan_espece,
	typoc1.typocan_esp_sans_compagne as culture_typocan_espece_sans_compagne,
	typoc1.nb_composant_culture as culture_typocan_nbre_composant,
	typoc1.nb_typocan_esp as culture_typocan_nbre_espece,

	-- culture_intermediaire_*
	culture_inter.id as culture_intermediaire_id,
	culture_inter.nom as culture_intermediaire_nom,
	culture_inter.melange_especes as culture_intermediaire_melange_especes,
	culture_inter.melange_varietes as culture_intermediaire_melange_varietes,
	culture_inter.code as culture_intermediaire_code,
	culture_inter."type" as culture_intermediaire_type,

	-- culture_intermediaire_typocan_*
	typoci.typocan_culture_sans_compagne as culture_intermerdiaire_typocan_sans_compagne,
	typoci.typocan_espece as culture_intermerdiaire_typocan_espece,
	typoci.nb_composant_culture as culture_intermerdiaire_typocan_nbre_composant,

	----------
	-- ZONE --
	----------
	zone.id as zone_id,
	zone.code as zone_code,
	zone.nom as zone_nom,
	zone.surface as zone_surface,

	--------------
	-- PARCELLE --
	--------------
	parcelle.code as parcelle_code,
	parcelle.nom as parcelle_nom,
	parcelle.commune_id ,
	parcelle.sol_nom_ref ,
	CASE when parcelle.edaplos_utilisateur_id is not null THEN True ELSE False END AS parcelle_import_edaplos,
	
	---------
	-- SDC --
	---------
	sdc.id as sdc_id,
	sdc.code as sdc_code,
	sdc.nom as sdc_nom,
	sdc.code_dephy as sdc_code_dephy,
	sdc.date_debut_pratique as sdc_date_debut_pratique, -- format date
	sdc.date_fin_pratique as sdc_date_fin_pratique, -- format date
	sdc.filiere as sdc_filiere,
	sdc.type_production as sdc_type_production,
	sdc.type_agriculture as sdc_type_agriculture,
	sdc.part_sau_domaine as sdc_part_sau_domaine,

	-- sdc_typo_*
	typoassol.surface_totale_assol_dvlp as sdc_typo_surface_totale_assol_dvlp,
	typoassol.surface_totale_assol as sdc_typo_surface_totale_assol,
	
	-- sdc_typocan_*
	typoassol.typocan_assol_dvlp  as sdc_typocan_assol_dvlp,
	typoassol.typocan_assol  as sdc_typocan_assol,

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
	dom.code as domaine_code,
	dom.nom as domaine_nom,
	dom.campagne as domaine_campagne,
	dom.siret as domaine_siret,
	dom.type_ferme as domaine_type_ferme,
	dom.departement as domaine_position_departement,
	dom.commune_id as domaine_position_commune_id,
	dom.zonage as domaine_zonage,
	-- domaine_pct_*
	dom.pct_sau_zone_vulnerable as domaine_pct_sau_zone_vulnerable,
	dom.pct_sau_zone_excedent_structurel as domaine_pct_sau_zone_excedent_structurel,
	dom.pct_sau_zone_actions_complementaires as domaine_pct_sau_zone_excedent_structurel,
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
	dom.membre_cooperative as domaine_membre_cooperative,
	dom.membre_groupe_developpement as domaine_membre_groupe_developpement,
	dom.membre_cuma as domaine_membre_cuma,
	dom.domaine_touristique as domaine_domaine_touristique,
	-- domaine_main_oeuvre_*
	dom.main_oeuvre_exploitant as domaine_main_oeuvre_exploitant,
	dom.main_oeuvre_non_saisoniere as domaine_main_oeuvre_non_saisoniere,
	dom.main_oeuvre_saisoniere as domaine_main_oeuvre_saisoniere,
	dom.main_oeuvre_volontaire as domaine_main_oeuvre_volontaire,

	-----------------
	-- DOMAINE_SOL --
	-----------------
	domsol.id as domaine_sol_id,
	domsol.nom_local as domaine_sol_nom,
	domsol.sol_arvalis_id as domaine_sol_arvalis_id,
	
	-------------------------------------------
	-- DONNEES_SPATIALES_COMMMUNE_DU_DOMAINE --
	-------------------------------------------
	interop.codeinsee as domaine_position_code_insee,
	interop.safran_cell_id as domaine_position_cellule_safran,
	interop.rmqs_site_id as domaine_position_rmqs_site_id,
	interop.typo_ruralite as domaine_typologie_ruralite
	
FROM entrepot_itk_realise_performance AS itkR
LEFT JOIN entrepot_noeuds_realise_restructure AS node_res
    ON node_res.id = itkR.noeuds_realise_id 
LEFT JOIN entrepot_connection_realise AS cx
    ON cx.cible_noeuds_realise_id = itkR.noeuds_realise_id
LEFT JOIN entrepot_zone AS zone
    ON zone.id = itkR.zone_id 
LEFT JOIN entrepot_parcelle AS parcelle
    ON parcelle.id = zone.parcelle_id 
LEFT JOIN entrepot_sdc AS sdc
    ON sdc.id = parcelle.sdc_id 
LEFT JOIN entrepot_domaine AS dom
    ON dom.id = parcelle.domaine_id
LEFT JOIN entrepot_domaine_sol AS domsol
    ON domsol.id = parcelle.domaine_sol_id 
LEFT JOIN entrepot_dispositif AS dispo
    ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_commune AS comm
    ON parcelle.commune_id = comm.id
LEFT JOIN entrepot_donnees_spatiales_commune_du_domaine AS interop
    ON interop.domaine_id = parcelle.domaine_id
LEFT JOIN entrepot_culture AS culture1
    ON culture1.id = itkR.culture_id 
LEFT JOIN entrepot_typologie_can_culture AS typoc1
    ON typoc1.culture_id = itkR.culture_id 
LEFT JOIN entrepot_culture AS culture_inter
    ON culture_inter.id = cx.culture_intermediaire_id 
LEFT JOIN entrepot_typologie_can_culture AS typoci
    ON typoci.culture_id = cx.culture_intermediaire_id 
LEFT JOIN entrepot_typologie_assol_can_realise AS typoassol
    ON typoassol.sdc_id = sdc.id
;



