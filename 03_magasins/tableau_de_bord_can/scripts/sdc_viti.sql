-- SCRIPT SQL POUR LE TRAITEMENT DES DONNÉES VITICOLES (viti.csv)
-- Aligné sur le fichier viti_var.csv et inspiré de sdc_gcpe.sql

SELECT
    -- Identification unique
    COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne AS ID_CODE_DEPHY_CAMPAGNE,
    sdc.code_dephy AS sdc_code_dephy,
    sdc.campagne AS campagne_donnees,
    -- Dispositif et réseaux
    dispo."type" AS dispositif_type,
    errsotdbc.reseaux_it AS reseaux_it,
    errsotdbc.reseaux_ir AS reseau_ir,
    -- Domaine et localisation
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS Nom_Departement,  -- À remplir via une jointure avec une table de référence géographique
    comm.region AS Nom_Region,        -- Idem
    comm.ancienne_region AS Nom_Ancienne_Region,
    dom.sau_totale AS sau_domaine,
    dom.otex_18_nom AS otex_18_nom,       -- Spécifique viticulture : à vérifier dans la base
    dom.otex_70_nom AS otex_70_nom,       -- Idem
    dom.campagne AS domaine_campagne,
    -- SDC et approche
    'VITICOLE' AS sdc_filiere,  -- Filière fixe pour ce script
    'réalisé' AS approche_de_calcul,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.part_sau_domaine AS sdc_part_sau_domaine,
    -- Type d'agriculture et système synthétisé
    sdc.type_agriculture AS sdc_type_agriculture,
    null AS systeme_synthetise_id,      
    null AS systeme_synthetise_nom,  
    null AS systeme_synthetise_campagnes,
    -- Rendement (spécifique viticulture)
    ervsrotdbc.rendement_moyen AS rendement_moyen,  
   	ervsrotdbc.rendement_unite AS unite_rendement,
    -- Données économiques et techniques
    esrp.mb_reelle_avec_autoconso AS MB_reelle_ac_auto_SDC,
    esrp.msn_reelle_avec_autoconso AS MSN_relle_ac_auto_SDC,
    esrp.pb_reel_avec_autoconso AS pb_reel_avec_autoconso,
    esrp.co_tot_reelles AS CO_reelles_SDC,
    esrp.cm_reelles AS CM_reelles_SDC,
    esrp.conso_carburant AS conso_carburant_SDC,
    esrp.c_main_oeuvre_tractoriste_std_mil AS cout_mo_tractoriste,
    esrp.c_main_oeuvre_manuelle_std_mil AS cout_mo_manuelle,
    esrp.nombre_uth_necessaires AS nbre_uth_sdc,
    -- IFT et alertes (viticulture)
    esrp.ift_cible_non_mil_chimique_tot AS ift_cible_non_mil_chim_tot_SDC,
    esrp.ift_cible_non_mil_chim_tot_hts AS ift_cible_non_mil_chim_tot_hts_SDC,
    esrp.ift_cible_non_mil_biocontrole AS ift_cible_nonmil_biocontrole_SDC,
    esrp.ift_cible_non_mil_h AS ift_cible_non_mil_h_SDC,
    esrp.ift_cible_non_mil_hh AS ift_cible_non_mil_hh_SDC,
    esrp.ift_cible_non_mil_f AS ift_cible_non_mil_f_SDC,
    esrp.ift_cible_non_mil_i AS ift_cible_non_mil_i_SDC,
    esrp.ift_cible_non_mil_a AS ift_cible_non_mil_a_SDC,
    esrp.ift_cible_non_mil_ts AS ift_cible_non_mil_ts_SDC,
    null AS IFT_norme,                     -- Norme IFT viticole si disponible
    null AS IFT_chimique_moyen_SSP,       -- Idem
    comm.bassin_viticole AS bassin_viticole_SSP,        
    -- Interventions et produits
    esrp.nbre_de_passages AS Nbre_inter_phyto_SDC,
    esrp.qsa_tot AS quantite_mat_active_SDC,
    esrp.qsa_toxique_utilisateur AS quantite_mat_active_danger_SDC,
    esrp.qsa_danger_environnement AS qte_mat_active_danger_env_SDC,
    esrp.qsa_glyphosate AS quantite_mat_active_glypho_SDC,
    esrp.qsa_neonicotinoides AS quantite_mat_active_neonic_SDC,
    esrp.qsa_cuivre_metal_tot AS qte_cuivre_SDC,
    esrp.qsa_cuivre_metal_ferti AS qte_cuivre_engrais_SDC,
    esrp.qsa_cuivre_metal_phyto AS qte_cuivre_phyto_SDC,
    esrp.qsa_soufre_tot AS qte_soufre_SDC,
    esrp.qsa_soufre_ferti AS qte_soufre_engrais_SDC,
    esrp.qsa_soufre_phyto AS qte_soufre_phyto_SDC,
    -- Fertilisation
    esrp.ferti_n_tot AS N_SDC,
    esrp.ferti_n_mineral AS N_Mineral_SDC,
    esrp.ferti_n_organique AS N_Orga_SDC,
    esrp.ferti_p2o5_tot AS P_SDC,
    esrp.ferti_p2o5_mineral AS P_Mineral_SDC,
    esrp.ferti_p2o5_organique AS P_Orga_SDC,
    esrp.ferti_k2o_tot AS K_SDC,
    esrp.ferti_k2o_mineral AS K_Mineral_SDC,
    esrp.ferti_k2o_organique AS K_Orga_SDC,
    -- Eau et temps de travail
    esrp.conso_eau AS Qte_Eau_mm_ha_SDC,
    egesotdbc.use_enherbement AS gestion_enherbement_SDC,  -- Spécifique viticulture
    esrp.tps_utilisation_materiel AS tps_util_materiel_SDC,
    -- Temps mensuels (exemple pour janvier à décembre)
    esrp.tps_utilisation_materiel_janvier AS tps_util_materiel_janvier_SDC,
    esrp.tps_utilisation_materiel_fevrier AS tps_util_materiel_fevrier_SDC,
    -- ... (compléter pour tous les mois)
    esrp.tps_travail_manuel AS tps_travail_manuel_SDC,
    -- Temps manuel mensuel (exemple pour janvier à décembre)
    esrp.tps_travail_manuel_janvier AS tps_travail_manuel_janvier_SDC,
    -- ... (compléter pour tous les mois)
    -- GES et énergie
    esrp.ges_carburants_total_ges_total AS GES_SDC,
    esrp.ges_carburants_directes_ges_total AS GES_directes_SDC,
    esrp.ges_carburants_directes_co2 AS Emissions_directes_Fuel_SDC,
    esrp.ges_ferti_min_directes_ges_total AS Emissions_directes_Ferti_SDC,
    esrp.ges_carburants_indirectes_ges_total AS GES_indirectes_SDC,
    esrp.ges_carburants_indirectes_co2 AS Emissions_indirectes_fuel_SDC,
    esrp.ges_ferti_min_indirectes_ges_total AS emissions_indirectes_engrais_SDC,
    esrp.ges_phyto_total_ges_total AS emissions_indirectes_phyto_SDC,
    esrp.energie_totale_directes + esrp.energie_totale_indirectes AS NRJ_SDC,                     -- Énergie totale
    esrp.energie_carburants_directes + esrp.energie_carburants_indirectes AS Energie_Fuel_SDC,            -- Idem
    esrp.energie_ferti_min + esrp.energie_ferti_orga AS energie_indirecte_engrais_SDC,
    esrp.energie_phyto AS energie_indirecte_phyto_SDC,
    esrp.energie_totale_indirectes AS NRJ_indirecte_SDC,
    null AS NRJ_recolte,                 -- Spécifique viticulture
    null AS efficience_NRJ,
    null AS bilan_NRJ,
    -- Alertes (viticulture)
    esrp.alerte_ift_cible_mil_chim_tot_hts AS Alerte_IFT_total_SDC,
    esrp.alerte_ift_cible_mil_h AS Alerte_IFT_herbicide_SDC,    -- À adapter
    esrp.alerte_ift_cible_mil_i AS Alerte_IFT_insecticide_SDC,  -- Idem
    null AS Alerte_Intervention_Phytos,
    null AS Alerte_temps_travail_SDC,
    null AS Alerte_Absence_unite_dose_SDC,
    null AS Alerte_rendement_SDC,
    null AS Synthese_alertes,
    null AS surface_sdc_itk,
    null AS alerte_renseignement_donnees,
    null AS part_sole_sdc_sans_itk,
    null as alerte_sole_sdc,
    esrp.recours_produits_danger_environnement AS Nb_intrant_dang_env_SDC,
    null AS Bassin_viticole_bilan_ferme,
    -- Situation de production et coûts
    sdc.type_agriculture || '_' || comm.bassin_viticole AS situation_production,  -- Ex: "VITICOLE_Rouge" ou "VITICOLE_Champagne"
    esrp.co_tot_std_mil AS CO_std_mil_SDC,
    esrp.mb_reelle_sans_autoconso AS MB_reelle_sans_autoconso,
    esrp.msn_reelle_sans_autoconso AS MSN_reelle_sans_autoconso,
    esrp.qsa_cmr AS quantite_mat_active_CMR_SDC,
    esrp.recours_produits_cmr AS Nb_intrant_CMR_SDC,
    esrp.recours_produits_toxiques_utilisateurs AS nb_manip_produit_CMR_SDC,    -- À vérifier
    esrp.qsa_diflufenican AS qte_mat_active_diflufeni_SDC,
    esrp.qsa_mancozeb AS qte_mat_active_mancozebe_SDC,
    esrp.qsa_tebuconazole AS qte_mat_active_tebuco_SDC,
    -- ... (autres substances)
    -- Coûts par poste
    esrp.co_phyto_sans_amm_reelles AS CO_reelles_phytos_SDC,
    esrp.co_fertimin_reel AS CO_reelles_ferti_min_SDC,
    esrp.co_epandage_orga_reelles AS CO_reelles_ferti_orga_SDC,
    esrp.co_irrigation_reelles AS CO_reelles_irrig_SDC,
    esrp.co_semis_reel AS CO_reelles_semences_SDC,
    esrp.co_intrants_autres_reelles AS CO_reelles_autres_SDC,
    esrp.co_phyto_avec_amm_reelles AS CO_reelles_lutte_bio_SDC,
    -- Situation de production détaillée (millésime)
    sdc.type_agriculture || '_' || comm.bassin_viticole || '_' || COALESCE(TEXT(sdc.campagne), TEXT('sans_campagne')) AS situation_production_mill,
    sdc.codes_convention_dephy AS codes_convention_dephy,
    -- Recours aux moyens biologiques
    esrp.recours_aux_moyens_biologiques AS rec_moyens_biologiques_SDC,
    esrp.recours_macroorganismes AS recours_macroorganismes_SDC,
    esrp.recours_produits_biotiques_sansamm AS recours_pdts_biot_sansamm_SDC,
    esrp.recours_produits_abiotiques_sansamm AS recours_ptds_abiot_sansamm_SDC,
    null AS effectif_SP                  -- Spécifique viticulture
FROM entrepot_sdc sdc
LEFT JOIN entrepot_dispositif dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine dom ON dom.id = dispo.domaine_id
LEFT JOIN entrepot_commune comm ON dom.commune_id = comm.id
LEFT JOIN entrepot_entite_unique_par_sdc_nettoyage eeupsn ON sdc.id = eeupsn.sdc_id
LEFT JOIN entrepot_reseaux_rattachement_sdc_outils_tableau_de_bord_can errsotdbc ON sdc.id = errsotdbc.id
LEFT JOIN entrepot_sdc_realise_outils_tableau_de_bord_can esrotdbc ON sdc.id = esrotdbc.id
LEFT JOIN entrepot_sdc_realise_performance esrp ON esrp.sdc_id = sdc.id
left join entrepot_rendement_viti_sdc_realise_outils_tableau_de_bord_can ervsrotdbc on ervsrotdbc.id = sdc.id
left join entrepot_gestion_enherbement_sdc_outils_tableau_de_bord_can egesotdbc on egesotdbc.id = sdc.id
WHERE sdc.filiere = 'VITICULTURE'
AND eeupsn.entite_retenue = 'realise_retenu'
AND NOT dispo.type = 'NOT_DEPHY'
UNION
SELECT
    -- Identification unique
    COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne AS ID_CODE_DEPHY_CAMPAGNE,
    sdc.code_dephy AS sdc_code_dephy,
    sdc.campagne AS campagne_donnees,
    -- Dispositif et réseaux
    dispo."type" AS dispositif_type,
    errsotdbc.reseaux_it AS reseaux_it,
    errsotdbc.reseaux_ir AS reseau_ir,
    -- Domaine et localisation
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS Nom_Departement,  -- À remplir via une jointure avec une table de référence géographique
    comm.region AS Nom_Region,        -- Idem
    comm.ancienne_region AS Nom_Ancienne_Region,
    dom.sau_totale AS sau_domaine,
    dom.otex_18_nom AS otex_18_nom,       -- Spécifique viticulture : à vérifier dans la base
    dom.otex_70_nom AS otex_70_nom,       -- Idem
    dom.campagne AS domaine_campagne,
    -- SDC et approche
    'VITICOLE' AS sdc_filiere,  -- Filière fixe pour ce script
    'synthétisé' AS approche_de_calcul,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.part_sau_domaine AS sdc_part_sau_domaine,
    -- Type d'agriculture et système synthétisé
    sdc.type_agriculture AS sdc_type_agriculture,
    synthetise.id AS systeme_synthetise_id,      
    synthetise.nom AS systeme_synthetise_nom,  
    synthetise.campagnes AS systeme_synthetise_campagnes,
    -- Rendement (spécifique viticulture)
	ervsrotdbc.rendement_moyen AS rendement_moyen,
    ervsrotdbc.rendement_unite AS unite_rendement,
    -- Données économiques et techniques
    essp.mb_reelle_avec_autoconso AS MB_reelle_ac_auto_SDC,
    essp.msn_reelle_avec_autoconso AS MSN_relle_ac_auto_SDC,
    essp.pb_reel_avec_autoconso AS pb_reel_avec_autoconso,
    essp.co_tot_reelles AS CO_reelles_SDC,
    essp.cm_reelles AS CM_reelles_SDC,
    essp.conso_carburant AS conso_carburant_SDC,
    essp.c_main_oeuvre_tractoriste_std_mil AS cout_mo_tractoriste,
    essp.c_main_oeuvre_manuelle_std_mil AS cout_mo_manuelle,
    essp.nombre_uth_necessaires AS nbre_uth_sdc,
    -- IFT et alertes (viticulture)
    essp.ift_cible_non_mil_chimique_tot AS ift_cible_non_mil_chim_tot_SDC,
    essp.ift_cible_non_mil_chim_tot_hts AS ift_cible_non_mil_chim_tot_hts_SDC,
    essp.ift_cible_non_mil_biocontrole AS ift_cible_nonmil_biocontrole_SDC,
    essp.ift_cible_non_mil_h AS ift_cible_non_mil_h_SDC,
    essp.ift_cible_non_mil_hh AS ift_cible_non_mil_hh_SDC,
    essp.ift_cible_non_mil_f AS ift_cible_non_mil_f_SDC,
    essp.ift_cible_non_mil_i AS ift_cible_non_mil_i_SDC,
    essp.ift_cible_non_mil_a AS ift_cible_non_mil_a_SDC,
    essp.ift_cible_non_mil_ts AS ift_cible_non_mil_ts_SDC,
    null AS IFT_norme,                     -- Norme IFT viticole si disponible
    null AS IFT_chimique_moyen_SSP,       -- Idem
    comm.bassin_viticole AS bassin_viticole_SSP,        
    -- Interventions et produits
    essp.nbre_de_passages AS Nbre_inter_phyto_SDC,
    essp.qsa_tot AS quantite_mat_active_SDC,
    essp.qsa_toxique_utilisateur AS quantite_mat_active_danger_SDC,
    essp.qsa_danger_environnement AS qte_mat_active_danger_env_SDC,
    essp.qsa_glyphosate AS quantite_mat_active_glypho_SDC,
    essp.qsa_neonicotinoides AS quantite_mat_active_neonic_SDC,
    essp.qsa_cuivre_metal_tot AS qte_cuivre_SDC,
    essp.qsa_cuivre_metal_ferti AS qte_cuivre_engrais_SDC,
    essp.qsa_cuivre_metal_phyto AS qte_cuivre_phyto_SDC,
    essp.qsa_soufre_tot AS qte_soufre_SDC,
    essp.qsa_soufre_ferti AS qte_soufre_engrais_SDC,
    essp.qsa_soufre_phyto AS qte_soufre_phyto_SDC,
    -- Fertilisation
    essp.ferti_n_tot AS N_SDC,
    essp.ferti_n_mineral AS N_Mineral_SDC,
    essp.ferti_n_organique AS N_Orga_SDC,
    essp.ferti_p2o5_tot AS P_SDC,
    essp.ferti_p2o5_mineral AS P_Mineral_SDC,
    essp.ferti_p2o5_organique AS P_Orga_SDC,
    essp.ferti_k2o_tot AS K_SDC,
    essp.ferti_k2o_mineral AS K_Mineral_SDC,
    essp.ferti_k2o_organique AS K_Orga_SDC,
    -- Eau et temps de travail
    essp.conso_eau AS Qte_Eau_mm_ha_SDC,
    egesotdbc.use_enherbement AS gestion_enherbement_SDC,  -- Spécifique viticulture
    essp.tps_utilisation_materiel AS tps_util_materiel_SDC,
    -- Temps mensuels (exemple pour janvier à décembre)
    essp.tps_utilisation_materiel_janvier AS tps_util_materiel_janvier_SDC,
    essp.tps_utilisation_materiel_fevrier AS tps_util_materiel_fevrier_SDC,
    -- ... (compléter pour tous les mois)
    essp.tps_travail_manuel AS tps_travail_manuel_SDC,
    -- Temps manuel mensuel (exemple pour janvier à décembre)
    essp.tps_travail_manuel_janvier AS tps_travail_manuel_janvier_SDC,
    -- ... (compléter pour tous les mois)
    -- GES et énergie
    essp.ges_carburants_total_ges_total AS GES_SDC,
    essp.ges_carburants_directes_ges_total AS GES_directes_SDC,
    essp.ges_carburants_directes_co2 AS Emissions_directes_Fuel_SDC,
    essp.ges_ferti_min_directes_ges_total AS Emissions_directes_Ferti_SDC,
    essp.ges_carburants_indirectes_ges_total AS GES_indirectes_SDC,
    essp.ges_carburants_indirectes_co2 AS Emissions_indirectes_fuel_SDC,
    essp.ges_ferti_min_indirectes_ges_total AS emissions_indirectes_engrais_SDC,
    essp.ges_phyto_total_ges_total AS emissions_indirectes_phyto_SDC,
    essp.energie_totale_directes + essp.energie_totale_indirectes AS NRJ_SDC,
    essp.energie_carburants_directes + essp.energie_carburants_indirectes AS Energie_Fuel_SDC,
    essp.energie_ferti_min + essp.energie_ferti_orga AS energie_indirecte_engrais_SDC,
    essp.energie_phyto AS energie_indirecte_phyto_SDC,
    essp.energie_totale_indirectes AS NRJ_indirecte_SDC,
    null AS NRJ_recolte,                 -- Spécifique viticulture
    null AS efficience_NRJ,
    null AS bilan_NRJ,
    -- Alertes (viticulture)
    essp.alerte_ift_cible_mil_chim_tot_hts AS Alerte_IFT_total_SDC,
    essp.alerte_ift_cible_mil_h AS Alerte_IFT_herbicide_SDC,    -- À adapter
    essp.alerte_ift_cible_mil_i AS Alerte_IFT_insecticide_SDC,  -- Idem
    null AS Alerte_Intervention_Phytos,
    null AS Alerte_temps_travail_SDC,
    null AS Alerte_Absence_unite_dose_SDC,
    null AS Alerte_rendement_SDC,
    null AS Synthese_alertes,
    null AS surface_sdc_itk,
    null AS alerte_renseignement_donnees,
    null AS part_sole_sdc_sans_itk,
    null as alerte_sole_sdc,
    essp.recours_produits_danger_environnement AS Nb_intrant_dang_env_SDC,
    null AS Bassin_viticole_bilan_ferme,
    -- Situation de production et coûts
    sdc.type_agriculture || '_' || comm.bassin_viticole AS situation_production,  -- Ex: "VITICOLE_Rouge" ou "VITICOLE_Champagne"
    essp.co_tot_std_mil AS CO_std_mil_SDC,
    essp.mb_reelle_sans_autoconso AS MB_reelle_sans_autoconso,
    essp.msn_reelle_sans_autoconso AS MSN_reelle_sans_autoconso,
    essp.qsa_cmr AS quantite_mat_active_CMR_SDC,
    essp.recours_produits_cmr AS Nb_intrant_CMR_SDC,
    essp.recours_produits_toxiques_utilisateurs AS nb_manip_produit_CMR_SDC,    -- À vérifier
    essp.qsa_diflufenican AS qte_mat_active_diflufeni_SDC,
    essp.qsa_mancozeb AS qte_mat_active_mancozebe_SDC,
    essp.qsa_tebuconazole AS qte_mat_active_tebuco_SDC,
    -- ... (autres substances)
    -- Coûts par poste
    essp.co_phyto_sans_amm_reelles AS CO_reelles_phytos_SDC,
    essp.co_fertimin_reel AS CO_reelles_ferti_min_SDC,
    essp.co_epandage_orga_reelles AS CO_reelles_ferti_orga_SDC,
    essp.co_irrigation_reelles AS CO_reelles_irrig_SDC,
    essp.co_semis_reel AS CO_reelles_semences_SDC,
    essp.co_intrants_autres_reelles AS CO_reelles_autres_SDC,
    essp.co_phyto_avec_amm_reelles AS CO_reelles_lutte_bio_SDC,
    -- Situation de production détaillée (millésime)
    sdc.type_agriculture || '_' || comm.bassin_viticole || '_' || COALESCE(TEXT(sdc.campagne), TEXT('sans_campagne')) AS situation_production_mill,
    sdc.codes_convention_dephy AS codes_convention_dephy,
    -- Recours aux moyens biologiques
    essp.recours_aux_moyens_biologiques AS rec_moyens_biologiques_SDC,
    essp.recours_macroorganismes AS recours_macroorganismes_SDC,
    essp.recours_produits_biotiques_sansamm AS recours_pdts_biot_sansamm_SDC,
    essp.recours_produits_abiotiques_sansamm AS recours_ptds_abiot_sansamm_SDC,
    null AS effectif_SP             
FROM entrepot_synthetise synthetise 
LEFT JOIN entrepot_sdc sdc on synthetise.sdc_id = sdc.id
LEFT JOIN entrepot_dispositif  dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine     dom   ON dom.id   = dispo.domaine_id
LEFT JOIN entrepot_commune    comm   ON dom.commune_id = comm.id
left join entrepot_entite_unique_par_sdc_nettoyage eeupsn on sdc.id = eeupsn.sdc_id
left join entrepot_reseaux_rattachement_sdc_outils_tableau_de_bord_can errsotdbc on sdc.id = errsotdbc.id 
left join entrepot_stc_synthetise_outils_tableau_de_bord_can essotdbc on essotdbc.id = synthetise.id
left join entrepot_surface_synthetise_outils_tableau_de_bord_can esusotdb on esusotdb.id = synthetise.id
left join entrepot_typologie_can_rotation_synthetise etcrs on etcrs.synthetise_id = synthetise.id
left join entrepot_synthetise_synthetise_performance essp on synthetise.id = essp.synthetise_id
left join entrepot_gestion_enherbement_sdc_outils_tableau_de_bord_can egesotdbc on egesotdbc.id = sdc.id
left join entrepot_rendement_viti_sdc_realise_outils_tableau_de_bord_can ervsrotdbc on ervsrotdbc.id = sdc.id
WHERE sdc.filiere = 'VITICULTURE'
and eeupsn.entite_retenue != 'realise_retenu'
AND NOT dispo.type = 'NOT_DEPHY';

