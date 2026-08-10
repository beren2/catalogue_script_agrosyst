
-- SYNTHETISE
select
	ecs.id as itk_id,
    'synthetise' as approche_de_calcul,
    sdc.campagne as campagne_donnees,
  	etcc.typocan_espece || ' ; ' || sdc.type_agriculture as groupe_typologique_de_la_culture, -- Concaténation situation de production et typologiqe culture
	sdc.code_dephy as sdc_code_dephy,
    dispo."type" as dispositif_type,
    errsotdbc.reseaux_it as reseaux_it,
    errsotdbc.reseaux_ir as reseaux_ir,
    dom.id as domaine_id,
    dom.nom as domaine_nom,
    dom.departement as departement,
    dom.otex_18_nom as otex_18_nom, 
    dom.campagne as domaine_campagne,
    sdc.filiere as sdc_filiere,
    sdc.id as sdc_id,
    sdc.nom as sdc_nom,
    sdc.type_production as sdc_type_production, 
    sdc.validite as sdc_valide,
    sdc.type_agriculture as sdc_type_agricutlure,
    sdc.type_agriculture as ab_conv, --doublon avec la variable précédente
    es.id as systeme_synthetise_id,
    es.nom as systeme_synthetise_nom,
    es.campagnes as systeme_synthetise_campagnes,
    es.valide as systeme_synthetise_validation,
    epcsr.poids_conx_agregation as assolement_culture_CP,
    null as parcelle_nom,
    null as parcelle_id,
    null as parcelle_surface,
    null as zone_nom,
    null as zone_id, 
    null as zone_surface,
    ecs.id as connection_synthetise,
    ens.rang as rang,
    ec.nom as culture_nom,
    ec.code as culture_code,
    ec.id as culture_id,
    ec.type as culture_type,
   	etcod.typodirodur_espece_precise as especes_destination,  -- (typologie d'espèce avec destination pour DiRoDur)
    etcod.typodirodur_espece as especes,  -- (typologie d'espece utilisée pour DiRoDur)
    etcc.nb_typocan_esp, --nb composant culture ?
    etcc.typocan_espece as typo_especes,
    etcc.nb_typocan_esp as nb_typo_espece,
    etcod.typodirodur_culture as typo_culture,
    null as typo_culture_2, --> de quoi s'agit-il ? 
    ec_intermediaire.id as ci_id,
    ec_intermediaire.nom as ci_nom,
    ec_intermediaire.code as ci_code,
    ec_prec.nom as precedent_nom,
    ec.code as precedent_code,
    ec.id as precedent_id,
    etcod.typodirodur_espece_precise || ' ; ' || sdc.type_agriculture as situation_production_cp, -- Concaténation ESPECES_DESTINATION et type_agriculture
	null as rendement_moyen_grain,
	null as unite_rendement_grain,
	null as rendement_moyen_paille,
	null as unite_rendement_paille,
	null as rendement_moyen_fourrage,
	null as unite_rendement_fourrage,
	null as rendement_moyen_sucre,
	null as unite_rendement_sucre,
	null as rendement_moyen_fibre,
	null as unite_rendement_fibre,
	null as rendement_moyen_semences,
	null as unite_rendement_semences,
	null as rendement_moyen_bioenergie,
	null as unite_rendement_bioenergie,
	null as rendement_moyen_ttes_categ,
	null as unite_rendement_ttes_categ,
	--
	eisp.recours_produits_toxiques_utilisateurs as Nb_intrant_dang_CP,
	eisp.recours_produits_danger_environnement as Nb_intrant_dang_env_CP,
	eisp.recours_produits_cmr as Nb_intrant_CMR_CP,
	--
	eisp.co_tot_reelles + eisp.cm_reelles as charges_totale_CP, 
	null as nbre_uth_CP, -- à venir sur Agrosyst
	--
	null as IFT_h_smethola_CP, -- à venir sur Agrosyst
	null as IFT_h_chlorto_CP, -- à venir sur Agrosyst
	null as IFT_h_diflufeni_CP, -- à venir sur Agrosyst
	null as IFT_h_dicamba_CP, -- à venir sur Agrosyst
	null as IFT_h_prosulfo_CP, -- à venir sur Agrosyst
	null as IFT_f_bixafen_CP, -- à venir sur Agrosyst
	null as IFT_f_boscalid_CP, -- à venir sur Agrosyst
	null as IFT_f_mancozebe_CP, -- à venir sur Agrosyst
	null as IFT_f_tebuco_CP, -- à venir sur Agrosyst
	null as IFT_i_phosmet_CP -- à venir sur Agrosyst
FROM entrepot_connection_synthetise ecs
LEFT JOIN entrepot_itk_synthetise_agrege eisa ON eisa.itk_id = ecs.id
left join entrepot_itk_synthetise_performance eisp on ecs.id = eisp.itk_synthetise_id
left join entrepot_noeuds_synthetise ens on ecs.cible_noeuds_synthetise_id = ens.id
left join entrepot_noeuds_synthetise_restructure ensr on ensr.id = ecs.cible_noeuds_synthetise_id
left join entrepot_noeuds_synthetise_restructure ensr_prec on ensr_prec.id = ecs.source_noeuds_synthetise_id 
left join entrepot_noeuds_synthetise ens_prec on ecs.source_noeuds_synthetise_id = ens_prec.id
left join entrepot_connection_synthetise_restructure ecsr on ecsr.id = ecs.id
LEFT JOIN entrepot_culture ec ON ensr.culture_id = ec.id
left join entrepot_culture ec_intermediaire on  ec_intermediaire.id = ecsr.culture_intermediaire_id 
left join entrepot_culture ec_prec on ec_prec.id = ensr_prec.culture_id
LEFT JOIN entrepot_typologie_culture_outils_dirodur etcod ON ec.id = etcod.culture_id
left join entrepot_typologie_can_culture etcc on ec.id = etcc.culture_id 
LEFT JOIN entrepot_sdc sdc on sdc.id = eisa.sdc_id
LEFT JOIN entrepot_dispositif  dispo ON dispo.id = eisa.dispositif_id
LEFT JOIN entrepot_domaine     dom   ON dom.id   = eisa.domaine_id
LEFT JOIN entrepot_commune    comm   ON dom.commune_id = comm.id
left join entrepot_synthetise es on eisa.synthetise_id = es.id
left join entrepot_entite_unique_par_sdc_nettoyage eeupsn on sdc.id = eeupsn.sdc_id
left join entrepot_reseaux_rattachement_sdc_outils_tableau_de_bord_can errsotdbc on sdc.id = errsotdbc.id 
left join entrepot_sdc_realise_outils_tableau_de_bord_can esrotdbc on sdc.id = esrotdbc.id
left join entrepot_typologie_assol_can_realise etacr on etacr.sdc_id = sdc.id
left join entrepot_stc_sdc_realise_outils_tableau_de_bord_can essrotdbc on sdc.id = essrotdbc.id
left join entrepot_sdc_realise_performance esrp on sdc.id = esrp.sdc_id 
left join entrepot_poids_connexions_synthetise_rotation epcsr on epcsr.connexion_id = ecs.id
WHERE (sdc.filiere = 'GRANDES_CULTURES' or sdc.filiere = 'POLYCULTURE_ELEVAGE')
and eeupsn.entite_retenue != 'realise_retenu'
and not dispo.type = 'NOT_DEPHY';
and eisa.synthetise_id like '%fr.inra.agrosyst.api.entities.practiced.PracticedSystem_3eb8abb1-03cc-4e45-9d25-ba1b4bc74da5%';

