-- SYNTHETISE
SELECT
	ecs.id AS itk_id,
    'synthetise' AS approche_de_calcul,
    sdc.campagne AS campagne_donnees,
  	etcc.typocan_espece || ' ; ' || sdc.type_agriculture AS groupe_typologique_de_la_culture, -- Concaténation situation de production et typologiqe culture
	sdc.code_dephy AS sdc_code_dephy,
    dispo."type" AS dispositif_type,
    errsotdbc.reseaux_it AS reseaux_it,
    errsotdbc.reseaux_ir AS reseaux_ir,
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS departement,
    dom.otex_18_nom AS otex_18_nom, 
    dom.campagne AS domaine_campagne,
    sdc.filiere AS sdc_filiere,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.type_production AS sdc_type_production, 
    sdc.validite AS sdc_valide,
    sdc.type_agriculture AS sdc_type_agricutlure,
    sdc.type_agriculture AS ab_conv, --doublon avec la variable précédente
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
    ecs.id AS connexion_synthetise_id,
    -- culture_precedent_rang_id --> supprimer
    -- culture_rang --> supprimer
    ens.rang AS rang,
    ec.nom AS culture_nom,
    ec.code AS culture_code,
    ec.id AS culture_id,
    ec.type AS culture_type,
   	etcod.typodirodur_espece_precise AS especes_destination,  -- (typologie d'espèce avec destination pour DiRoDur)
    null AS especes,  -- ???
    etcc.nb_composant_culture AS nb_espece, 
    etcc.typocan_espece AS typo_especes,
    etcc.nb_typocan_esp as nb_typo_espece,
    etcc.typocan_culture AS typo_culture
    null AS typo_culture_2, --> de quoi s'agit-il ? 
    ec_intermediaire.id AS ci_id,
    ec_intermediaire.nom AS ci_nom,
    ec_intermediaire.code AS ci_code,
    ec_prec.nom AS precedent_nom,
    ec_prec.code AS precedent_code,
    ec_prec.id AS precedent_id,
    etcod.typodirodur_espece_precise || ' ; ' || sdc.type_agriculture AS situation_production_cp, -- Concaténation ESPECES_DESTINATIon et type_agriculture
	eirgotdbc.grain_rend_mean AS rendement_moyen_grain,
	eirgotdbc.grain_unit AS unite_rendement_grain,
	eirgotdbc.paille_rend_mean AS rendement_moyen_paille,
	eirgotdbc.paille_unit AS unite_rendement_paille,
	eirgotdbc.fourrage_rend_mean AS rendement_moyen_fourrage,
	eirgotdbc.fourrage_unit AS unite_rendement_fourrage,
	eirgotdbc.sucre_rend_mean AS rendement_moyen_sucre,
	eirgotdbc.sucre_unit AS unite_rendement_sucre,
	eirgotdbc.fibre_rend_mean AS rendement_moyen_fibre,
	eirgotdbc.fibre_unit AS unite_rendement_fibre,
	eirgotdbc.semences_rend_mean AS rendement_moyen_semences,
	eirgotdbc.semences_unit AS unite_rendement_semences,
	eirgotdbc.bioenergie_rend_mean AS rendement_moyen_bioenergie,
	eirgotdbc.bioenergie_unit AS unite_rendement_bioenergie,
	eirgotdbc.ttes_categ_rend_mean AS rendement_moyen_ttes_categ,
	eirgotdbc.ttes_categ_unit AS unite_rendement_ttes_categ,
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
WHERE (sdc.filiere = 'GRANDES_CULTURES' or sdc.filiere = 'POLYCULTURE_ELEVAGE')
AND eeupsn.entite_retenue != 'realise_retenu'
AND NOT dispo.type = 'NOT_DEPHY'
union
-- REALISE
SELECT
	enr.id AS itk_id,
    'realise' AS approche_de_calcul,
    sdc.campagne AS campagne_donnees,
  	etcc.typocan_espece || ' ; ' || sdc.type_agriculture AS groupe_typologique_de_la_culture, -- Concaténation situation de production et typologiqe culture
	sdc.code_dephy AS sdc_code_dephy,
    dispo."type" AS dispositif_type,
    errsotdbc.reseaux_it AS reseaux_it,
    errsotdbc.reseaux_ir AS reseaux_ir,
    dom.id AS domaine_id,
    dom.nom AS domaine_nom,
    dom.departement AS departement,
    dom.otex_18_nom AS otex_18_nom, 
    dom.campagne AS domaine_campagne,
    sdc.filiere AS sdc_filiere,
    sdc.id AS sdc_id,
    sdc.nom AS sdc_nom,
    sdc.type_production AS sdc_type_production, 
    sdc.validite AS sdc_valide,
    sdc.type_agriculture AS sdc_type_agricutlure,
    sdc.type_agriculture AS ab_conv, --doublon avec la variable précédente
    null AS systeme_synthetise_id,
    null AS systeme_synthetise_nom,
    null AS systeme_synthetise_campagnes,
    null AS systeme_synthetise_validation,
   	null AS assolement_culture_CP,
    ep.nom AS parcelle_nom,
    ep.id AS parcelle_id,
    ep.surface AS parcelle_surface,
    ez.nom AS zone_nom,
    ez.id AS zone_id, 
    ez.surface AS zone_surface,
    null AS connexion_synthetise_id,
    enr.rang AS rang,
    ec.nom AS culture_nom,
    ec.code AS culture_code,
    ec.id AS culture_id,
    ec.type AS culture_type,
   	etcod.typodirodur_espece_precise AS especes_destination,  -- (typologie d'espèce avec destination pour DiRoDur)
    null AS especes,  -- ???
    etcc.nb_composant_culture AS nb_espece, 
    etcc.typocan_espece AS typo_especes,
    etcc.nb_typocan_esp as nb_typo_espece,
    etcc.typocan_culture AS typo_culture,
    null AS typo_culture_2, --> de quoi s'agit-il ? 
    ec_intermediaire.id AS ci_id,
    ec_intermediaire.nom AS ci_nom,
    ec_intermediaire.code AS ci_code,
    ec_prec.nom AS precedent_nom,
    ec_prec.code AS precedent_code,
    ec_prec.id AS precedent_id,
    etcod.typodirodur_espece_precise || ' ; ' || sdc.type_agriculture AS situation_production_cp, -- Concaténation ESPECES_DESTINATIon et type_agriculture
	eirgotdbc.grain_rend_mean AS rendement_moyen_grain,
	eirgotdbc.grain_unit AS unite_rendement_grain,
	eirgotdbc.paille_rend_mean AS rendement_moyen_paille,
	eirgotdbc.paille_unit AS unite_rendement_paille,
	eirgotdbc.fourrage_rend_mean AS rendement_moyen_fourrage,
	eirgotdbc.fourrage_unit AS unite_rendement_fourrage,
	eirgotdbc.sucre_rend_mean AS rendement_moyen_sucre,
	eirgotdbc.sucre_unit AS unite_rendement_sucre,
	eirgotdbc.fibre_rend_mean AS rendement_moyen_fibre,
	eirgotdbc.fibre_unit AS unite_rendement_fibre,
	eirgotdbc.semences_rend_mean AS rendement_moyen_semences,
	eirgotdbc.semences_unit AS unite_rendement_semences,
	eirgotdbc.bioenergie_rend_mean AS rendement_moyen_bioenergie,
	eirgotdbc.bioenergie_unit AS unite_rendement_bioenergie,
	eirgotdbc.ttes_categ_rend_mean AS rendement_moyen_ttes_categ,
	eirgotdbc.ttes_categ_unit AS unite_rendement_ttes_categ,
	--
	eirp.recours_produits_toxiques_utilisateurs AS Nb_intrant_dang_CP,
	eirp.recours_produits_danger_environnement AS Nb_intrant_dang_env_CP,
	eirp.recours_produits_cmr AS Nb_intrant_CMR_CP,
	--
	eirp.co_tot_reelles + eirp.cm_reelles AS charges_totale_CP, 
	eirp.nbre_uth_necessaires AS nbre_uth_CP, 
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
WHERE (sdc.filiere = 'GRANDES_CULTURES' or sdc.filiere = 'POLYCULTURE_ELEVAGE')
AND eeupsn.entite_retenue = 'realise_retenu'
AND not dispo.type = 'NOT_DEPHY';