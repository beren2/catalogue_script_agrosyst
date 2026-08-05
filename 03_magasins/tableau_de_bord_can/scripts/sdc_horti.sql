-- SCRIPT SQL POUR LE TRAITEMENT DES DONNÉES VITICOLES (viti.csv)
-- Aligné sur le fichier viti_var.csv et inspiré de sdc_gcpe.sql


SELECT
    -- Identification unique
    COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne AS ID_CODE_DEPHY_CAMPAGNE,
    sdc.code_dephy AS sdc_code_dephy,
    sdc.campagne AS campagne_donnees,
    -- Dispositif et réseaux
    dispo."type" AS dispositif_type,
    escotdbc.reseaux_it AS reseaux_it,
    escotdbc.reseaux_ir AS reseau_ir,
    -- Domaine et localisation
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS Nom_Departement,  -- À remplir via une jointure avec une table de référence géographique
    comm.region AS Nom_Region,        -- Idem
    comm.ancienne_region AS Nom_Ancienne_Region,
    dom.sau_totale AS sau_domaine,
    dom.campagne AS domaine_campagne,
    -- SDC et approche
    'réalisé' AS approche_de_calcul,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.part_sau_domaine AS sdc_part_sau_domaine,
    -- Type d'agriculture et système synthétisé
    sdc.type_agriculture AS sdc_type_agriculture,
    null AS systeme_synthetise_id,      
    null AS systeme_synthetise_nom,  
    null AS systeme_synthetise_campagnes,
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
    -- Interventions et produits
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
    null as alerte_description_rotation,
    null AS Alerte_Absence_unite_dose_SDC,
    null AS alerte_renseignement_donnees,
    -- Situation de production et coûts
    sdc.type_agriculture || '_' || comm.bassin_viticole AS situation_production,  -- Ex: "VITICOLE_Rouge" ou "VITICOLE_Champagne"
    esrp.co_tot_std_mil AS CO_std_mil_SDC,
    esrp.qsa_diflufenican AS qte_mat_active_diflufeni_SDC,
    esrp.qsa_mancozeb AS qte_mat_active_mancozebe_SDC,
    esrp.qsa_tebuconazole AS qte_mat_active_tebuco_SDC,
	esrp.qsa_prosulfocarbe as qte_mat_active_prosulfo_sdc,
    esrp.qsa_bixafen as qte_mat_active_bixafen_sdc,
    -- ... (autres substances)
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
LEFT JOIN entrepot_sdc_complet_outils_tableau_de_bord_can escotdbc ON sdc.id = escotdbc.id
LEFT JOIN entrepot_sdc_realise_performance esrp ON esrp.sdc_id = sdc.id
WHERE sdc.filiere = 'HORTICULTURE'
AND eeupsn.entite_retenue = 'realise_retenu'
AND NOT dispo.type = 'NOT_DEPHY'
union
SELECT
    -- Identification unique
    COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne AS ID_CODE_DEPHY_CAMPAGNE,
    sdc.code_dephy AS sdc_code_dephy,
    sdc.campagne AS campagne_donnees,
    -- Dispositif et réseaux
    dispo."type" AS dispositif_type,
    escotdbc.reseaux_it AS reseaux_it,
    escotdbc.reseaux_ir AS reseau_ir,
    -- Domaine et localisation
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS Nom_Departement,  -- À remplir via une jointure avec une table de référence géographique
    comm.region AS Nom_Region,        -- Idem
    comm.ancienne_region AS Nom_Ancienne_Region,
    dom.sau_totale AS sau_domaine,
    dom.campagne AS domaine_campagne,
    -- SDC et approche
    'synthétisé' AS approche_de_calcul,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.part_sau_domaine AS sdc_part_sau_domaine,
    -- Type d'agriculture et système synthétisé
    sdc.type_agriculture AS sdc_type_agriculture,
    synthetise.id AS systeme_synthetise_id,      
    synthetise.nom AS systeme_synthetise_nom,  
    synthetise.campagnes AS systeme_synthetise_campagnes,
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
    -- Interventions et produits
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
    null as alerte_description_rotation,
    null AS Alerte_Absence_unite_dose_SDC,
    null AS alerte_renseignement_donnees,
    -- Situation de production et coûts
    sdc.type_agriculture || '_' || comm.bassin_viticole AS situation_production,  -- Ex: "VITICOLE_Rouge" ou "VITICOLE_Champagne"
    essp.co_tot_std_mil AS CO_std_mil_SDC,
    essp.qsa_diflufenican AS qte_mat_active_diflufeni_SDC,
    essp.qsa_mancozeb AS qte_mat_active_mancozebe_SDC,
    essp.qsa_tebuconazole AS qte_mat_active_tebuco_SDC,
    essp.qsa_prosulfocarbe as qte_mat_active_prosulfo_sdc,
    essp.qsa_bixafen as qte_mat_active_bixafen_sdc,
    -- ... (autres substances)
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
left join entrepot_sdc_complet_outils_tableau_de_bord_can escotdbc on escotdbc.id = eeupsn.sdc_id
left join entrepot_synthetise_synthetise_performance essp on synthetise.id = essp.synthetise_id
left join entrepot_synthetise_complet_outils_tableau_de_bord_can escotdbc2 on escotdbc2.id = essp.synthetise_id
WHERE sdc.filiere = 'HORTICULTURE'
and eeupsn.entite_retenue != 'realise_retenu'
AND NOT dispo.type = 'NOT_DEPHY';
