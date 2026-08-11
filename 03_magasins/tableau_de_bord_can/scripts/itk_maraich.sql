-- SYNTHETISE

select type_production from entrepot_sdc where filiere = 'MARAICHAGE'

SELECT
	COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne as identifiant_systeme_campagne,
  	--etcc.typocan_espece || ' ; ' || sdc.type_agriculture AS groupe_typologique_de_la_culture, -- Concaténation situation de production et typologiqe culture
	--sdc.code_dephy AS sdc_code_dephy,
    null as identifiant_itk, -- exemple ???
	COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne  as identifiant_systeme_campagne, --concaténation des variables sdc_code_dephy + campagne
	null AS identifiant_itk, -- exemple ???
	null  AS identifiant_itk_sdc_camp,-- exemple ?
	--
    'synthetise' AS approche_de_calcul,
    sdc.campagne AS campagne_donnees,
    sdc.type_production as situation_production,
    sdc.code_dephy as sdc_code_dephy,
    --
    dispo."type" AS dispositif_type,
    errsotdbc.reseaux_it AS reseaux_it,
    errsotdbc.reseaux_ir AS reseaux_ir,
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS departement,
    comm.departement AS Nom_Departement, 
    comm.region AS Nom_Region,    
    comm.ancienne_region AS Nom_Ancienne_Region,
    dom.otex_18_nom AS otex_18_nom, 
    dom.campagne AS domaine_campagne,
    sdc.filiere AS sdc_filiere,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.type_production AS sdc_type_production, 
    sdc.validite AS sdc_valide,
    sdc.type_agriculture AS sdc_type_agricutlure,
    sdc.type_agriculture AS ab_conv, --doublon avec la variable précédente ?
    es.id AS systeme_synthetise_id,
    es.nom AS systeme_synthetise_nom,
    es.campagnes AS systeme_synthetise_campagnes,
    es.valide AS systeme_synthetise_validation,
    epcsr.poids_conx_agregation AS assolement_culture_CP,
    null AS parcelle_nom,
    null AS parcelle_id,
    null AS parcelle_surface,
    null AS zone_nom,
    null AS zone_id, 
    null AS zone_surface,
    -- culture_precedent_rang_id --> supprimer
    -- culture_rang --> supprimer
    ecs.id AS connexion_synthetise_id,
    ens.rang AS rang,
    ec.nom AS culture_nom,
    ec.code AS culture_code,
    ec.id AS culture_id,
    ec.type AS culture_type,
    etcod.typodirodur_espece AS especes,  -- (typologie d'espece utilisée pour DiRoDur)
    etcc.nb_typocan_esp AS nb_espece, -- Quelle différence avec nb_typo_espece ?
    etcc.typocan_espece AS typo_especes,
    etcc.nb_typocan_esp as nb_typo_espece, --nb composant culture ?
    etcod.typodirodur_culture AS typo_culture,
    ec_intermediaire.id AS ci_id,
    ec_intermediaire.nom AS ci_nom,
    ec_intermediaire.code AS ci_code,
    ec_prec.nom AS precedent_nom,
    ec_prec.code AS precedent_code,
    ec_prec.id AS precedent_id,
    null as unite_rendement, -- que faire si il y a plusieurs opérations de récolte dans l'itk ? Quelle unité ?
    null as Rdt_Toutes_catego_Tous_condition, -- idem ?
    null as Rdt_Autre, -- idem ?
    null as Rdt_Production_semences,-- idem ?
    null as Rdt_Fraiches_Primeur,-- idem ?
    null as Rdt_Exportation,-- idem ?
    null as Rdt_Circuit_Long,-- idem ?
    null as Rdt_Circuit_Court,-- idem ?
    null as Rendement_total,-- idem ?
    eisp.ift_histo_chimique_tot        AS ift_histo_chimique_tot_CP,
    eisp.ift_histo_chim_tot_hts        AS ift_histo_chim_tot_hts_CP,
    eisp.ift_histo_biocontrole         AS ift_histo_biocontrole_CP,
    eisp.ift_histo_hh                  AS ift_histo_hh_CP,
    eisp.ift_histo_f                   AS ift_histo_f_CP,
    eisp.ift_histo_i                   AS ift_histo_i_CP,
    eisp.ift_histo_a                   AS ift_histo_a_CP,
    eisp.ift_histo_ts                  AS ift_histo_ts_CP,
    eisp.ift_cible_mil_chimique_tot     AS ift_cible_mil_chimiq_tot_CP,
    eisp.ift_cible_mil_biocontrole      AS ift_cible_mil_biocontrole_CP,
    eisp.ift_cible_mil_h                 AS ift_cible_mil_h_CP,
    eisp.ift_cible_mil_hh                AS ift_cible_mil_hh_CP,
    eisp.ift_cible_mil_f                 AS ift_cible_mil_f_CP,
    eisp.ift_cible_mil_i                 AS ift_cible_mil_i_CP,
    eisp.ift_cible_mil_a                 AS ift_cible_mil_a_CP,
    eisp.ift_cible_mil_ts                AS ift_cible_mil_ts_CP,
    eisp.ift_cible_non_mil_chimique_tot  AS ift_cible_non_mil_chimiq_tot_CP,
    eisp.ift_cible_non_mil_biocontrole   AS ift_cible_non_mil_biocontrole_CP,
    eisp.ift_cible_non_mil_h              AS ift_cible_non_mil_h_CP,
    eisp.ift_cible_non_mil_hh             AS ift_cible_non_mil_hh_CP,
    eisp.ift_cible_non_mil_f              AS ift_cible_non_mil_f_CP,
    eisp.ift_cible_non_mil_i              AS ift_cible_non_mil_i_CP,
    eisp.ift_cible_non_mil_a              AS ift_cible_non_mil_a_CP,
    eisp.ift_cible_non_mil_ts             AS ift_cible_non_mil_ts_CP,
    eisp.ift_culture_mil_chim_tot_hts     AS ift_culture_mil_chim_tot_hts_CP,
    eisp.ift_culture_mil_biocontrole      AS ift_culture_mil_biocontrole_CP,
    eisp.ift_culture_mil_h                 AS ift_culture_mil_h_CP,
    eisp.ift_culture_mil_hh                AS ift_culture_mil_hh_CP,
    eisp.ift_culture_mil_f                 AS ift_culture_mil_f_CP,
    eisp.ift_culture_mil_i                 AS ift_culture_mil_i_CP,
    eisp.ift_culture_mil_ts                AS ift_culture_mil_ts_CP,
    eisp.ift_culture_non_mil_chim_tot_hts  AS ift_culture_non_mil_chim_tot_hts_CP,
    eisp.ift_culture_non_mil_biocontrole   AS ift_culture_non_mil_biocontrole_CP,
    eisp.ift_culture_non_mil_h              AS ift_culture_non_mil_h_CP,
    eisp.ift_culture_non_mil_hh             AS ift_culture_non_mil_hh_CP,
    eisp.ift_culture_non_mil_f              AS ift_culture_non_mil_f_CP,
    eisp.ift_culture_non_mil_i              AS ift_culture_non_mil_i_CP,
    eisp.ift_culture_non_mil_ts             AS ift_culture_non_mil_ts_CP,
    eisp.qsa_tot                            AS quantite_mat_active_CP,
    eisp.qsa_danger_environnement          AS quantite_mat_active_danger_CP,
    eisp.qsa_danger_environnement_hts      AS qte_mat_active_danger_env_CP,
    eisp.qsa_cmr                            AS quantite_mat_active_CMR_CP,
    eisp.qsa_cmr_hts                        AS quantite_mat_active_glypho_CP,
    eisp.qsa_cuivre_phyto_hts               AS quantite_mat_active_neonic_CP,
    eisp.qsa_cuivre_metal_tot                 AS quantite_cuivre_CP,
    eisp.qsa_cuivre_metal_ferti               AS qte_cuivre_engrais_CP,
    eisp.qsa_cuivre_metal_phyto               AS qte_cuivre_phyto_CP,
    eisp.qsa_soufre_tot                      AS quantite_soufre_CP,
    eisp.qsa_soufre_ferti                     AS qte_soufre_engrais_CP,
    eisp.qsa_soufre_phyto_hts                 AS qte_soufre_phyto_CP,
    null AS nb_intrants_verif_biocontrole, -- à venir sur Agrosyst
	eisp.recours_produits_danger_environnement AS Nb_intrant_dang_env_CP,
	eisp.recours_produits_toxiques_utilisateurs AS Nb_intrant_dang_CP,
	eisp.recours_produits_cmr AS Nb_intrant_CMR_CP,
    eisp.c_main_oeuvre_manuelle_reelle      AS c_main_oeuvre_manuelle_reelle_CP,
    eisp.c_main_oeuvre_manuelle_reelle_tx_comp  AS c_main_oeuvre_manuelle_reelle_tx_comp_CP,
    eisp.c_main_oeuvre_tractoriste_reelle  AS c_main_oeuvre_tractoriste_reelle_CP,
    eisp.c_main_oeuvre_tractoriste_reelle_tx_comp  AS c_main_oeuvre_tractoriste_reelle_tx_comp_CP,
    eisp.c_main_oeuvre_tot_reelle          AS c_main_oeuvre_tot_reelle_CP,
    eisp.c_main_oeuvre_tot_reelle_tx_comp  AS c_main_oeuvre_tot_reelle_tx_comp_CP,
    eisp.c_main_oeuvre_manuelle_reelle      AS charges_totale_CP,
    eisp.cm_reelles                           AS CM_reelles_CP,
    eisp.co_tot_reelles                       AS CO_reelles_CP,
    eisp.conso_carburant                      AS conso_carburant_CP,
    eisp.conso_carburant_tx_comp              AS conso_carburant_tx_comp_CP,
    eisp.energie_ferti_min                    AS energie_ferti_min_CP,
    eisp.energie_ferti_orga                    AS energie_ferti_orga_CP,
    eisp.energie_phyto                        AS energie_phyto_CP,
    eisp.energie_ferti_min                   AS GES_CP,                     -- CO2 equivalente
    eisp.energie_ferti_orga                   AS GES_directes_CP,           -- direct
    eisp.energie_ferti_min                    AS GES_indirectes_CP,         -- indirect
    eisp.tps_utilisation_materiel            AS tps_util_materiel_CP,
    eisp.tps_utilisation_materiel_tx_comp    AS tps_util_materiel_tx_comp_CP,
    eisp.tps_utilisation_materiel_janvier    AS tps_util_materiel_janvier_CP,
    eisp.tps_utilisation_materiel_fevrier    AS tps_util_materiel_fevrier_CP,
    eisp.tps_utilisation_materiel_mars       AS tps_util_materiel_mars_CP,
    eisp.tps_utilisation_materiel_avril      AS tps_util_materiel_avril_CP,
    eisp.tps_utilisation_materiel_mai        AS tps_util_materiel_mai_CP,
    eisp.tps_utilisation_materiel_juin       AS tps_util_materiel_juin_CP,
    eisp.tps_utilisation_materiel_juillet     AS tps_util_materiel_juillet_CP,
    eisp.tps_utilisation_materiel_aout      AS tps_util_materiel_aout_CP,
    eisp.tps_utilisation_materiel_sept       AS tps_util_materiel_sept_CP,
    eisp.tps_utilisation_materiel_oct         AS tps_util_materiel_oct_CP,
    eisp.tps_utilisation_materiel_nov         AS tps_util_materiel_nov_CP,
    eisp.tps_utilisation_materiel_dec         AS tps_util_materiel_dec_CP,
    eisp.tps_travail_manuel                  AS tps_travail_manuel_CP,
    eisp.tps_travail_manuel_tx_comp          AS tps_travail_manuel_tx_comp_CP,
    eisp.tps_travail_manuel_janvier          AS tps_travail_manuel_janvier_CP,
    eisp.tps_travail_manuel_fevrier          AS tps_travail_manuel_fevrier_CP,
    eisp.tps_travail_manuel_mars             AS tps_travail_manuel_mars_CP,
    eisp.tps_travail_manuel_avril            AS tps_travail_manuel_avril_CP,
    eisp.tps_travail_manuel_mai              AS tps_travail_manuel_mai_CP,
    eisp.tps_travail_manuel_juin             AS tps_travail_manuel_juin_CP,
    eisp.tps_travail_manuel_juillet           AS tps_travail_manuel_juillet_CP,
    eisp.tps_travail_manuel_aout            AS tps_travail_manuel_aout_CP,
    eisp.tps_travail_manuel_septembre        AS tps_travail_manuel_septembre_CP,
    eisp.tps_travail_manuel_octobre          AS tps_travail_manuel_octobre_CP,
    eisp.tps_travail_manuel_novembre         AS tps_travail_manuel_novembre_CP,
    eisp.tps_travail_manuel_decembre        AS tps_travail_manuel_decembre_CP,
    eisp.qsa_tot                   AS quantite_mat_active_CP,
    eisp.ferti_n_tot                        AS N_CP,
    eisp.ferti_n_mineral                    AS N_Mineral_CP,
    eisp.ferti_n_organique                  AS N_Orga_CP,
    eisp.ferti_p2o5_tot                     AS P_CP,
    eisp.ferti_p2o5_mineral                 AS P_Mineral_CP,
    eisp.ferti_p2o5_organique               AS P_Orga_CP,
    eisp.ferti_k2o_tot                      AS K_CP,
    eisp.ferti_k2o_mineral                  AS K_Mineral_CP,
    eisp.ferti_k2o_organique                AS K_Orga_CP,
    eisp.ges_carburants_directes_ch4        AS GES_CP,
    eisp.ges_carburants_directes_co2        AS GES_directes_CP,
    eisp.ges_carburants_directes_n2o        AS GES_indirectes_CP,
    eisp.ges_carburants_indirectes_ch4      AS GES_CP,
    eisp.ges_carburants_indirectes_co2      AS GES_directes_CP,
    eisp.ges_carburants_indirectes_n2o      AS GES_indirectes_CP,
    eisp.alertes_charges                 AS Alerte_Phyto_CP,
    eisp.alerte_ferti_n_tot              AS Alerte_ferti_azotee_CP,
    eisp.alerte_co_irrigation_std_mil    AS Alerte_semis_culture_principale,
    eisp.alerte_msn_std_mil_avec_autoconso AS Alerte_recolte_cult_princi,
    null AS Alerte_travail_sol, -- à venir sur Agrosyst
    eisp.c_main_oeuvre_manuelle_reelle    AS cout_mo_manuelle_CP,
    eisp.c_main_oeuvre_manuelle_reelle_tx_comp  AS cout_mo_manuelle_cp_tx_comp,
    eisp.c_main_oeuvre_tractoriste_reelle    AS cout_mo_tractoriste_CP,
    eisp.c_main_oeuvre_tractoriste_reelle_tx_comp  AS cout_mo_tractoriste_cp_tx_comp,
    eisp.alerte_nombre_interventions_phyto  AS rec_moyens_biologiques_CP,
    eisp.recours_macroorganismes          AS recours_macroorganismes_CP,
    eisp.recours_produits_biotiques_sansamm  AS rec_pdts_biot_sansamm_CP,
    eisp.recours_produits_abiotiques_sansamm AS rec_pdts_abiot_sansamm_CP,
    eisp.ift_cible_non_mil_chimique_tot     AS ift_cible_non_mil_chimiq_tot_CP,
    eisp.ift_cible_non_mil_biocontrole     AS ift_cible_non_mil_biocontrole_CP,
    eisp.ift_cible_non_mil_h                AS ift_cible_non_mil_h_CP,
    eisp.ift_cible_non_mil_hh               AS ift_cible_non_mil_hh_CP,
    eisp.ift_cible_non_mil_f                AS ift_cible_non_mil_f_CP,
    eisp.ift_cible_non_mil_i                AS ift_cible_non_mil_i_CP,
    eisp.ift_cible_non_mil_a                AS ift_cible_non_mil_a_CP,
    eisp.ift_cible_non_mil_ts               AS ift_cible_non_mil_ts_CP,
    null      								AS ift_cible_non_mil_rec_moy_bio_CP, -- à venir sur Agrosyst ? 
    eisp.ift_cible_mil_chimique_tot         AS ift_cible_mil_chimiq_tot_CP,
    eisp.ift_cible_mil_biocontrole          AS ift_cible_mil_biocontrole_CP,
    eisp.ift_cible_mil_h                    AS ift_cible_mil_h_CP,
    eisp.ift_cible_mil_hh                   AS ift_cible_mil_hh_CP,
    eisp.ift_cible_mil_f                    AS ift_cible_mil_f_CP,
    eisp.ift_cible_mil_i                    AS ift_cible_mil_i_CP,
    eisp.ift_cible_mil_a                    AS ift_cible_mil_a_CP,
    eisp.ift_cible_mil_ts                   AS ift_cible_mil_ts_CP,
    null           							AS ift_cible_mil_rec_moy_bio_CP, -- à venir sur Agrosyst ? 
    eisp.co_tot_reelles                      AS co_tot_reelles_CP,
    eisp.co_tot_reelles_tx_comp              AS co_tot_reelles_tx_comp_CP,
	--
	eisp.recours_produits_toxiques_utilisateurs AS Nb_intrant_dang_CP,
	eisp.recours_produits_danger_environnement AS Nb_intrant_dang_env_CP,
	eisp.recours_produits_cmr AS Nb_intrant_CMR_CP,
	--
	eisp.co_tot_reelles + eisp.cm_reelles AS charges_totale_CP, 
	eisp.nbre_uth_necessaires AS nbre_uth_CP, 
	--
	null AS IFT_h_smethola_CP, -- à venir sur Agrosyst --> jugé non prioritaire.
	null AS IFT_h_chlorto_CP, -- à venir sur Agrosyst
	null AS IFT_h_diflufeni_CP, -- à venir sur Agrosyst
	null AS IFT_h_dicamba_CP, -- à venir sur Agrosyst
	null AS IFT_h_prosulfo_CP, -- à venir sur Agrosyst
	null AS IFT_f_bixafen_CP, -- à venir sur Agrosyst
	null AS IFT_f_boscalid_CP, -- à venir sur Agrosyst
	null AS IFT_f_mancozebe_CP, -- à venir sur Agrosyst
	null AS IFT_f_tebuco_CP, -- à venir sur Agrosyst
	null AS IFT_i_phosmet_CP -- à venir sur Agrosyst
FROM entrepot_connection_synthetise ecs
LEFT JOIN entrepot_itk_synthetise_agrege eisa ON eisa.itk_id = ecs.id
LEFT JOIN entrepot_itk_synthetise_performance eisp ON ecs.id = eisp.itk_synthetise_id
LEFT JOIN entrepot_noeuds_synthetise ens ON ecs.cible_noeuds_synthetise_id = ens.id
LEFT JOIN entrepot_noeuds_synthetise_restructure ensr ON ensr.id = ecs.cible_noeuds_synthetise_id
LEFT JOIN entrepot_noeuds_synthetise_restructure ensr_prec ON ensr_prec.id = ecs.source_noeuds_synthetise_id 
LEFT JOIN entrepot_noeuds_synthetise ens_prec ON ecs.source_noeuds_synthetise_id = ens_prec.id
LEFT JOIN entrepot_connection_synthetise_restructure ecsr ON ecsr.id = ecs.id
LEFT JOIN entrepot_culture ec ON ensr.culture_id = ec.id
LEFT JOIN entrepot_culture ec_intermediaire ON  ec_intermediaire.id = ecsr.culture_intermediaire_id 
LEFT JOIN entrepot_culture ec_prec ON ec_prec.id = ensr_prec.culture_id
LEFT JOIN entrepot_typologie_culture_outils_dirodur etcod ON ec.id = etcod.culture_id
LEFT JOIN entrepot_typologie_can_culture etcc ON ec.id = etcc.culture_id 
LEFT JOIN entrepot_sdc sdc ON sdc.id = eisa.sdc_id
LEFT JOIN entrepot_dispositif  dispo ON dispo.id = eisa.dispositif_id
LEFT JOIN entrepot_domaine     dom   ON dom.id   = eisa.domaine_id
LEFT JOIN entrepot_commune    comm   ON dom.commune_id = comm.id
LEFT JOIN entrepot_synthetise es ON eisa.synthetise_id = es.id
LEFT JOIN entrepot_entite_unique_par_sdc_nettoyage eeupsn ON sdc.id = eeupsn.sdc_id
LEFT JOIN entrepot_reseaux_rattachement_sdc_outils_tableau_de_bord_can errsotdbc ON sdc.id = errsotdbc.id 
LEFT JOIN entrepot_sdc_realise_outils_tableau_de_bord_can esrotdbc ON sdc.id = esrotdbc.id
LEFT JOIN entrepot_typologie_assol_can_realise etacr ON etacr.sdc_id = sdc.id
LEFT JOIN entrepot_stc_sdc_realise_outils_tableau_de_bord_can essrotdbc ON sdc.id = essrotdbc.id
LEFT JOIN entrepot_sdc_realise_performance esrp ON sdc.id = esrp.sdc_id 
LEFT JOIN entrepot_poids_connexions_synthetise_rotation epcsr ON epcsr.connexion_id = ecs.id
LEFT JOIN entrepot_itk_rendement_gcpe_outils_tableau_de_bord_can eirgotdbc ON eirgotdbc.id = ecs.id
WHERE (sdc.filiere='MARAICHAGE')
AND eeupsn.entite_retenue != 'realise_retenu'
AND NOT dispo.type = 'NOT_DEPHY'
union 
SELECT
	COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne as identifiant_systeme_campagne,
  	--etcc.typocan_espece || ' ; ' || sdc.type_agriculture AS groupe_typologique_de_la_culture, -- Concaténation situation de production et typologiqe culture
	--sdc.code_dephy AS sdc_code_dephy,
    null as identifiant_itk, -- exemple ???
	COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT') || '_' || sdc.campagne  as identifiant_systeme_campagne, --concaténation des variables sdc_code_dephy + campagne
	null AS identifiant_itk, -- exemple ???
	null  AS identifiant_itk_sdc_camp,-- exemple ?
	--
    'synthetise' AS approche_de_calcul,
    sdc.campagne AS campagne_donnees,
    sdc.type_production as situation_production,
    sdc.code_dephy as sdc_code_dephy,
    --
    dispo."type" AS dispositif_type,
    errsotdbc.reseaux_it AS reseaux_it,
    errsotdbc.reseaux_ir AS reseaux_ir,
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS departement,
    comm.departement AS Nom_Departement, 
    comm.region AS Nom_Region,    
    comm.ancienne_region AS Nom_Ancienne_Region,
    dom.otex_18_nom AS otex_18_nom, 
    dom.campagne AS domaine_campagne,
    sdc.filiere AS sdc_filiere,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.type_production AS sdc_type_production, 
    sdc.validite AS sdc_valide,
    sdc.type_agriculture AS sdc_type_agricutlure,
    sdc.type_agriculture AS ab_conv, --doublon avec la variable précédente ?
    es.id AS systeme_synthetise_id,
    es.nom AS systeme_synthetise_nom,
    es.campagnes AS systeme_synthetise_campagnes,
    es.valide AS systeme_synthetise_validation,
    epcsr.poids_conx_agregation AS assolement_culture_CP,
    null AS parcelle_nom,
    null AS parcelle_id,
    null AS parcelle_surface,
    null AS zone_nom,
    null AS zone_id, 
    null AS zone_surface,
    -- culture_precedent_rang_id --> supprimer
    -- culture_rang --> supprimer
    ecs.id AS connexion_synthetise_id,
    ens.rang AS rang,
    ec.nom AS culture_nom,
    ec.code AS culture_code,
    ec.id AS culture_id,
    ec.type AS culture_type,
    etcod.typodirodur_espece AS especes,  -- (typologie d'espece utilisée pour DiRoDur)
    etcc.nb_typocan_esp AS nb_espece, -- Quelle différence avec nb_typo_espece ?
    etcc.typocan_espece AS typo_especes,
    etcc.nb_typocan_esp as nb_typo_espece, --nb composant culture ?
    etcod.typodirodur_culture AS typo_culture,
    ec_intermediaire.id AS ci_id,
    ec_intermediaire.nom AS ci_nom,
    ec_intermediaire.code AS ci_code,
    ec_prec.nom AS precedent_nom,
    ec_prec.code AS precedent_code,
    ec_prec.id AS precedent_id,
    null as unite_rendement, -- que faire si il y a plusieurs opérations de récolte dans l'itk ? Quelle unité ?
    null as Rdt_Toutes_catego_Tous_condition, -- idem ?
    null as Rdt_Autre, -- idem ?
    null as Rdt_Production_semences,-- idem ?
    null as Rdt_Fraiches_Primeur,-- idem ?
    null as Rdt_Exportation,-- idem ?
    null as Rdt_Circuit_Long,-- idem ?
    null as Rdt_Circuit_Court,-- idem ?
    null as Rendement_total,-- idem ?
    eisp.ift_histo_chimique_tot        AS ift_histo_chimique_tot_CP,
    eisp.ift_histo_chim_tot_hts        AS ift_histo_chim_tot_hts_CP,
    eisp.ift_histo_biocontrole         AS ift_histo_biocontrole_CP,
    eisp.ift_histo_hh                  AS ift_histo_hh_CP,
    eisp.ift_histo_f                   AS ift_histo_f_CP,
    eisp.ift_histo_i                   AS ift_histo_i_CP,
    eisp.ift_histo_a                   AS ift_histo_a_CP,
    eisp.ift_histo_ts                  AS ift_histo_ts_CP,
    eisp.ift_cible_mil_chimique_tot     AS ift_cible_mil_chimiq_tot_CP,
    eisp.ift_cible_mil_biocontrole      AS ift_cible_mil_biocontrole_CP,
    eisp.ift_cible_mil_h                 AS ift_cible_mil_h_CP,
    eisp.ift_cible_mil_hh                AS ift_cible_mil_hh_CP,
    eisp.ift_cible_mil_f                 AS ift_cible_mil_f_CP,
    eisp.ift_cible_mil_i                 AS ift_cible_mil_i_CP,
    eisp.ift_cible_mil_a                 AS ift_cible_mil_a_CP,
    eisp.ift_cible_mil_ts                AS ift_cible_mil_ts_CP,
    eisp.ift_cible_non_mil_chimique_tot  AS ift_cible_non_mil_chimiq_tot_CP,
    eisp.ift_cible_non_mil_biocontrole   AS ift_cible_non_mil_biocontrole_CP,
    eisp.ift_cible_non_mil_h              AS ift_cible_non_mil_h_CP,
    eisp.ift_cible_non_mil_hh             AS ift_cible_non_mil_hh_CP,
    eisp.ift_cible_non_mil_f              AS ift_cible_non_mil_f_CP,
    eisp.ift_cible_non_mil_i              AS ift_cible_non_mil_i_CP,
    eisp.ift_cible_non_mil_a              AS ift_cible_non_mil_a_CP,
    eisp.ift_cible_non_mil_ts             AS ift_cible_non_mil_ts_CP,
    eisp.ift_culture_mil_chim_tot_hts     AS ift_culture_mil_chim_tot_hts_CP,
    eisp.ift_culture_mil_biocontrole      AS ift_culture_mil_biocontrole_CP,
    eisp.ift_culture_mil_h                 AS ift_culture_mil_h_CP,
    eisp.ift_culture_mil_hh                AS ift_culture_mil_hh_CP,
    eisp.ift_culture_mil_f                 AS ift_culture_mil_f_CP,
    eisp.ift_culture_mil_i                 AS ift_culture_mil_i_CP,
    eisp.ift_culture_mil_ts                AS ift_culture_mil_ts_CP,
    eisp.ift_culture_non_mil_chim_tot_hts  AS ift_culture_non_mil_chim_tot_hts_CP,
    eisp.ift_culture_non_mil_biocontrole   AS ift_culture_non_mil_biocontrole_CP,
    eisp.ift_culture_non_mil_h              AS ift_culture_non_mil_h_CP,
    eisp.ift_culture_non_mil_hh             AS ift_culture_non_mil_hh_CP,
    eisp.ift_culture_non_mil_f              AS ift_culture_non_mil_f_CP,
    eisp.ift_culture_non_mil_i              AS ift_culture_non_mil_i_CP,
    eisp.ift_culture_non_mil_ts             AS ift_culture_non_mil_ts_CP,
    eisp.qsa_tot                            AS quantite_mat_active_CP,
    eisp.qsa_danger_environnement          AS quantite_mat_active_danger_CP,
    eisp.qsa_danger_environnement_hts      AS qte_mat_active_danger_env_CP,
    eisp.qsa_cmr                            AS quantite_mat_active_CMR_CP,
    eisp.qsa_cmr_hts                        AS quantite_mat_active_glypho_CP,
    eisp.qsa_cuivre_phyto_hts               AS quantite_mat_active_neonic_CP,
    eisp.qsa_cuivre_metal_tot                 AS quantite_cuivre_CP,
    eisp.qsa_cuivre_metal_ferti               AS qte_cuivre_engrais_CP,
    eisp.qsa_cuivre_metal_phyto               AS qte_cuivre_phyto_CP,
    eisp.qsa_soufre_tot                      AS quantite_soufre_CP,
    eisp.qsa_soufre_ferti                     AS qte_soufre_engrais_CP,
    eisp.qsa_soufre_phyto_hts                 AS qte_soufre_phyto_CP,
    null AS nb_intrants_verif_biocontrole, -- à venir sur Agrosyst
	eisp.recours_produits_danger_environnement AS Nb_intrant_dang_env_CP,
	eisp.recours_produits_toxiques_utilisateurs AS Nb_intrant_dang_CP,
	eisp.recours_produits_cmr AS Nb_intrant_CMR_CP,
    eisp.c_main_oeuvre_manuelle_reelle      AS c_main_oeuvre_manuelle_reelle_CP,
    eisp.c_main_oeuvre_manuelle_reelle_tx_comp  AS c_main_oeuvre_manuelle_reelle_tx_comp_CP,
    eisp.c_main_oeuvre_tractoriste_reelle  AS c_main_oeuvre_tractoriste_reelle_CP,
    eisp.c_main_oeuvre_tractoriste_reelle_tx_comp  AS c_main_oeuvre_tractoriste_reelle_tx_comp_CP,
    eisp.c_main_oeuvre_tot_reelle          AS c_main_oeuvre_tot_reelle_CP,
    eisp.c_main_oeuvre_tot_reelle_tx_comp  AS c_main_oeuvre_tot_reelle_tx_comp_CP,
    eisp.c_main_oeuvre_manuelle_reelle      AS charges_totale_CP,
    eisp.cm_reelles                           AS CM_reelles_CP,
    eisp.co_tot_reelles                       AS CO_reelles_CP,
    eisp.conso_carburant                      AS conso_carburant_CP,
    eisp.conso_carburant_tx_comp              AS conso_carburant_tx_comp_CP,
    eisp.energie_ferti_min                    AS energie_ferti_min_CP,
    eisp.energie_ferti_orga                    AS energie_ferti_orga_CP,
    eisp.energie_phyto                        AS energie_phyto_CP,
    eisp.energie_ferti_min                   AS GES_CP,                     -- CO2 equivalente
    eisp.energie_ferti_orga                   AS GES_directes_CP,           -- direct
    eisp.energie_ferti_min                    AS GES_indirectes_CP,         -- indirect
    eisp.tps_utilisation_materiel            AS tps_util_materiel_CP,
    eisp.tps_utilisation_materiel_tx_comp    AS tps_util_materiel_tx_comp_CP,
    eisp.tps_utilisation_materiel_janvier    AS tps_util_materiel_janvier_CP,
    eisp.tps_utilisation_materiel_fevrier    AS tps_util_materiel_fevrier_CP,
    eisp.tps_utilisation_materiel_mars       AS tps_util_materiel_mars_CP,
    eisp.tps_utilisation_materiel_avril      AS tps_util_materiel_avril_CP,
    eisp.tps_utilisation_materiel_mai        AS tps_util_materiel_mai_CP,
    eisp.tps_utilisation_materiel_juin       AS tps_util_materiel_juin_CP,
    eisp.tps_utilisation_materiel_juillet     AS tps_util_materiel_juillet_CP,
    eisp.tps_utilisation_materiel_aout      AS tps_util_materiel_aout_CP,
    eisp.tps_utilisation_materiel_sept       AS tps_util_materiel_sept_CP,
    eisp.tps_utilisation_materiel_oct         AS tps_util_materiel_oct_CP,
    eisp.tps_utilisation_materiel_nov         AS tps_util_materiel_nov_CP,
    eisp.tps_utilisation_materiel_dec         AS tps_util_materiel_dec_CP,
    eisp.tps_travail_manuel                  AS tps_travail_manuel_CP,
    eisp.tps_travail_manuel_tx_comp          AS tps_travail_manuel_tx_comp_CP,
    eisp.tps_travail_manuel_janvier          AS tps_travail_manuel_janvier_CP,
    eisp.tps_travail_manuel_fevrier          AS tps_travail_manuel_fevrier_CP,
    eisp.tps_travail_manuel_mars             AS tps_travail_manuel_mars_CP,
    eisp.tps_travail_manuel_avril            AS tps_travail_manuel_avril_CP,
    eisp.tps_travail_manuel_mai              AS tps_travail_manuel_mai_CP,
    eisp.tps_travail_manuel_juin             AS tps_travail_manuel_juin_CP,
    eisp.tps_travail_manuel_juillet           AS tps_travail_manuel_juillet_CP,
    eisp.tps_travail_manuel_aout            AS tps_travail_manuel_aout_CP,
    eisp.tps_travail_manuel_septembre        AS tps_travail_manuel_septembre_CP,
    eisp.tps_travail_manuel_octobre          AS tps_travail_manuel_octobre_CP,
    eisp.tps_travail_manuel_novembre         AS tps_travail_manuel_novembre_CP,
    eisp.tps_travail_manuel_decembre        AS tps_travail_manuel_decembre_CP,
    eisp.qsa_tot                   AS quantite_mat_active_CP,
    eisp.ferti_n_tot                        AS N_CP,
    eisp.ferti_n_mineral                    AS N_Mineral_CP,
    eisp.ferti_n_organique                  AS N_Orga_CP,
    eisp.ferti_p2o5_tot                     AS P_CP,
    eisp.ferti_p2o5_mineral                 AS P_Mineral_CP,
    eisp.ferti_p2o5_organique               AS P_Orga_CP,
    eisp.ferti_k2o_tot                      AS K_CP,
    eisp.ferti_k2o_mineral                  AS K_Mineral_CP,
    eisp.ferti_k2o_organique                AS K_Orga_CP,
    eisp.ges_carburants_directes_ch4        AS GES_CP,
    eisp.ges_carburants_directes_co2        AS GES_directes_CP,
    eisp.ges_carburants_directes_n2o        AS GES_indirectes_CP,
    eisp.ges_carburants_indirectes_ch4      AS GES_CP,
    eisp.ges_carburants_indirectes_co2      AS GES_directes_CP,
    eisp.ges_carburants_indirectes_n2o      AS GES_indirectes_CP,
    eisp.alertes_charges                 AS Alerte_Phyto_CP,
    eisp.alerte_ferti_n_tot              AS Alerte_ferti_azotee_CP,
    eisp.alerte_co_irrigation_std_mil    AS Alerte_semis_culture_principale,
    eisp.alerte_msn_std_mil_avec_autoconso AS Alerte_recolte_cult_princi,
    null AS Alerte_travail_sol, -- à venir sur Agrosyst
    eisp.c_main_oeuvre_manuelle_reelle    AS cout_mo_manuelle_CP,
    eisp.c_main_oeuvre_manuelle_reelle_tx_comp  AS cout_mo_manuelle_cp_tx_comp,
    eisp.c_main_oeuvre_tractoriste_reelle    AS cout_mo_tractoriste_CP,
    eisp.c_main_oeuvre_tractoriste_reelle_tx_comp  AS cout_mo_tractoriste_cp_tx_comp,
    eisp.alerte_nombre_interventions_phyto  AS rec_moyens_biologiques_CP,
    eisp.recours_macroorganismes          AS recours_macroorganismes_CP,
    eisp.recours_produits_biotiques_sansamm  AS rec_pdts_biot_sansamm_CP,
    eisp.recours_produits_abiotiques_sansamm AS rec_pdts_abiot_sansamm_CP,
    eisp.ift_cible_non_mil_chimique_tot     AS ift_cible_non_mil_chimiq_tot_CP,
    eisp.ift_cible_non_mil_biocontrole     AS ift_cible_non_mil_biocontrole_CP,
    eisp.ift_cible_non_mil_h                AS ift_cible_non_mil_h_CP,
    eisp.ift_cible_non_mil_hh               AS ift_cible_non_mil_hh_CP,
    eisp.ift_cible_non_mil_f                AS ift_cible_non_mil_f_CP,
    eisp.ift_cible_non_mil_i                AS ift_cible_non_mil_i_CP,
    eisp.ift_cible_non_mil_a                AS ift_cible_non_mil_a_CP,
    eisp.ift_cible_non_mil_ts               AS ift_cible_non_mil_ts_CP,
    null      								AS ift_cible_non_mil_rec_moy_bio_CP, -- à venir sur Agrosyst ? 
    eisp.ift_cible_mil_chimique_tot         AS ift_cible_mil_chimiq_tot_CP,
    eisp.ift_cible_mil_biocontrole          AS ift_cible_mil_biocontrole_CP,
    eisp.ift_cible_mil_h                    AS ift_cible_mil_h_CP,
    eisp.ift_cible_mil_hh                   AS ift_cible_mil_hh_CP,
    eisp.ift_cible_mil_f                    AS ift_cible_mil_f_CP,
    eisp.ift_cible_mil_i                    AS ift_cible_mil_i_CP,
    eisp.ift_cible_mil_a                    AS ift_cible_mil_a_CP,
    eisp.ift_cible_mil_ts                   AS ift_cible_mil_ts_CP,
    null           							AS ift_cible_mil_rec_moy_bio_CP, -- à venir sur Agrosyst ? 
    eisp.co_tot_reelles                      AS co_tot_reelles_CP,
    eisp.co_tot_reelles_tx_comp              AS co_tot_reelles_tx_comp_CP,
	--
	eisp.recours_produits_toxiques_utilisateurs AS Nb_intrant_dang_CP,
	eisp.recours_produits_danger_environnement AS Nb_intrant_dang_env_CP,
	eisp.recours_produits_cmr AS Nb_intrant_CMR_CP,
	--
	eisp.co_tot_reelles + eisp.cm_reelles AS charges_totale_CP, 
	eisp.nbre_uth_necessaires AS nbre_uth_CP, 
	--
	null AS IFT_h_smethola_CP, -- à venir sur Agrosyst --> jugé non prioritaire.
	null AS IFT_h_chlorto_CP, -- à venir sur Agrosyst
	null AS IFT_h_diflufeni_CP, -- à venir sur Agrosyst
	null AS IFT_h_dicamba_CP, -- à venir sur Agrosyst
	null AS IFT_h_prosulfo_CP, -- à venir sur Agrosyst
	null AS IFT_f_bixafen_CP, -- à venir sur Agrosyst
	null AS IFT_f_boscalid_CP, -- à venir sur Agrosyst
	null AS IFT_f_mancozebe_CP, -- à venir sur Agrosyst
	null AS IFT_f_tebuco_CP, -- à venir sur Agrosyst
	null AS IFT_i_phosmet_CP -- à venir sur Agrosyst
FROM entrepot_noeuds_realise enr
LEFT JOIN entrepot_itk_realise_agrege eira ON eira.itk_id = enr.id
LEFT JOIN entrepot_itk_realise_performance eirp ON eirp.itk_realise_id = enr.id
LEFT JOIN entrepot_connection_realise ecr ON ecr.cible_noeuds_realise_id = enr.id
LEFT JOIN entrepot_culture ec ON enr.culture_id = ec.id
LEFT JOIN entrepot_culture ec_intermediaire ON  ec_intermediaire.id = ecr.culture_intermediaire_id 
LEFT JOIN entrepot_noeuds_realise_restructure enrr ON enrr.id = enr.id
LEFT JOIN entrepot_noeuds_realise enr_prec ON enrr.precedent_noeuds_realise_id = enr_prec.id
LEFT JOIN entrepot_culture ec_prec ON ec_prec.id = enr_prec.culture_id
LEFT JOIN entrepot_typologie_culture_outils_dirodur etcod ON ec.id = etcod.culture_id
LEFT JOIN entrepot_typologie_can_culture etcc ON ec.id = etcc.culture_id 
LEFT JOIN entrepot_sdc sdc ON sdc.id = eira.sdc_id
LEFT JOIN entrepot_dispositif dispo ON dispo.id = eira.dispositif_id
LEFT JOIN entrepot_domaine dom ON dom.id   = eira.domaine_id
LEFT JOIN entrepot_commune comm ON dom.commune_id = comm.id
LEFT JOIN entrepot_parcelle ep ON eira.parcelle_id = ep.id
LEFT JOIN entrepot_zone ez ON eira.zone_id = ez.id
LEFT JOIN entrepot_entite_unique_par_sdc_nettoyage eeupsn ON sdc.id = eeupsn.sdc_id
LEFT JOIN entrepot_reseaux_rattachement_sdc_outils_tableau_de_bord_can errsotdbc ON sdc.id = errsotdbc.id 
LEFT JOIN entrepot_sdc_realise_outils_tableau_de_bord_can esrotdbc ON sdc.id = esrotdbc.id
LEFT JOIN entrepot_typologie_assol_can_realise etacr ON etacr.sdc_id = sdc.id
LEFT JOIN entrepot_stc_sdc_realise_outils_tableau_de_bord_can essrotdbc ON sdc.id = essrotdbc.id
LEFT JOIN entrepot_sdc_realise_performance esrp ON sdc.id = esrp.sdc_id 
LEFT JOIN entrepot_itk_rendement_gcpe_outils_tableau_de_bord_can eirgotdbc ON eirgotdbc.id = enr.id
WHERE (sdc.filiere = 'MARAICHAGE')
AND eeupsn.entite_retenue = 'realise_retenu'
AND not dispo.type = 'NOT_DEPHY';












