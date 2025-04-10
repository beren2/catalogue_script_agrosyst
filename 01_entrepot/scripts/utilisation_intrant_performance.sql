--------------------
-- performances à l'échelle intrant
--------------------

create table entrepot_utilisation_intrant_performance AS
SELECT
    replace(replace(id_usage,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS utilisation_intrant_id,
    approche_de_calcul AS approche_de_calcul,
	-- IFT
    ift_a_l_ancienne_ift_chimique_total AS ift_histo_chimique_tot,
    ift_a_l_ancienne_ift_chimique_tot_hts AS ift_histo_chim_tot_hts,
    ift_a_l_ancienne_ift_h AS ift_histo_h,
    ift_a_l_ancienne_ift_f AS ift_histo_f,
    ift_a_l_ancienne_ift_i AS ift_histo_i,
    ift_a_l_ancienne_ift_ts AS ift_histo_ts,
    ift_a_l_ancienne_ift_a AS ift_histo_a,
    ift_a_l_ancienne_ift_hh AS ift_histo_hh,
    ift_a_l_ancienne_ift_biocontrole AS ift_histo_biocontrole,
    ift_a_l_ancienne_tx_completion AS ift_histo_tx_comp,
    replace(replace(ift_a_l_ancienne_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_histo_chmps_non_rens,
    replace(replace(ift_a_l_ancienne_dose_reference,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_histo_dose_ref,
    replace(replace(ift_a_l_ancienne_dose_reference_unite,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_histo_dose_ref_unite,
    ift_a_la_cible_non_mil_ift_chimique_total AS ift_cible_non_mil_chimique_tot,
    ift_a_la_cible_non_mil_ift_chimique_tot_hts AS ift_cible_non_mil_chim_tot_hts,
    ift_a_la_cible_non_mil_ift_h AS ift_cible_non_mil_h,
    ift_a_la_cible_non_mil_ift_f AS ift_cible_non_mil_f,
    ift_a_la_cible_non_mil_ift_i AS ift_cible_non_mil_i,
    ift_a_la_cible_non_mil_ift_ts AS ift_cible_non_mil_ts,
    ift_a_la_cible_non_mil_ift_a AS ift_cible_non_mil_a,
    ift_a_la_cible_non_mil_ift_hh AS ift_cible_non_mil_hh,
    ift_a_la_cible_non_mil_ift_biocontrole AS ift_cible_non_mil_biocontrole,
    ift_a_la_cible_non_mil_taux_de_completion AS ift_cible_non_mil_tx_comp,
    replace(replace(ift_a_la_cible_non_mil_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_cible_non_mil_chmps_non_rens,
    replace(replace(ift_a_la_cible_non_mil_dose_reference,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_cible_non_mil_dose_ref,
    replace(replace(ift_a_la_cible_non_mil_dose_reference_unite,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_cible_non_mil_dose_ref_unite,
    ift_a_la_cible_mil_ift_chimique_total AS ift_cible_mil_chimique_tot,
    ift_a_la_cible_mil_ift_chimique_tot_hts AS ift_cible_mil_chim_tot_hts,
    ift_a_la_cible_mil_ift_h AS ift_cible_mil_h,
    ift_a_la_cible_mil_ift_f AS ift_cible_mil_f,
    ift_a_la_cible_mil_ift_i AS ift_cible_mil_i,
    ift_a_la_cible_mil_ift_ts AS ift_cible_mil_ts,
    ift_a_la_cible_mil_ift_a AS ift_cible_mil_a,
    ift_a_la_cible_mil_ift_hh AS ift_cible_mil_hh,
    ift_a_la_cible_mil_ift_biocontrole AS ift_cible_mil_biocontrole,
    ift_a_la_cible_mil_taux_de_completion AS ift_cible_mil_tx_comp,
    replace(replace(ift_a_la_cible_mil_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_cible_mil_chmps_non_rens,
    replace(replace(ift_a_la_cible_mil_dose_reference,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_cible_mil_dose_ref,
    replace(replace(ift_a_la_cible_mil_dose_reference_unite,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_cible_mil_dose_ref_unite,
    ift_a_la_culture_non_mil_ift_chimique_total AS ift_culture_non_mil_chimique_tot,
    ift_a_la_culture_non_mil_ift_chimique_tot_hts AS ift_culture_non_mil_chim_tot_hts,
    ift_a_la_culture_non_mil_ift_h AS ift_culture_non_mil_h,
    ift_a_la_culture_non_mil_ift_f AS ift_culture_non_mil_f,
    ift_a_la_culture_non_mil_ift_i AS ift_culture_non_mil_i,
    ift_a_la_culture_non_mil_ift_ts AS ift_culture_non_mil_ts,
    ift_a_la_culture_non_mil_ift_a AS ift_culture_non_mil_a,
    ift_a_la_culture_non_mil_ift_hh AS ift_culture_non_mil_hh,
    ift_a_la_culture_non_mil_ift_biocontrole AS ift_culture_non_mil_biocontrole,
    ift_a_la_culture_non_mil_taux_de_completion AS ift_culture_non_mil_tx_comp,
    replace(replace(ift_a_la_culture_non_mil_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_culture_non_mil_chmp_no_rens,
    replace(replace(ift_a_la_culture_non_mil_dose_reference,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_culture_non_mil_dose_ref,
    replace(replace(ift_a_la_culture_non_mil_dose_reference_unite,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_culture_non_mil_dose_ref_unite,
    ift_a_la_culture_mil_ift_chimique_total AS ift_culture_mil_chimique_tot,
    ift_a_la_culture_mil_ift_chimique_tot_hts AS ift_culture_mil_chim_tot_hts,
    ift_a_la_culture_mil_ift_h AS ift_culture_mil_h,
    ift_a_la_culture_mil_ift_f AS ift_culture_mil_f,
    ift_a_la_culture_mil_ift_i AS ift_culture_mil_i,
    ift_a_la_culture_mil_ift_ts AS ift_culture_mil_ts,
    ift_a_la_culture_mil_ift_a AS ift_culture_mil_a,
    ift_a_la_culture_mil_ift_hh AS ift_culture_mil_hh,
    ift_a_la_culture_mil_ift_biocontrole AS ift_culture_mil_biocontrole,
    ift_a_la_culture_mil_taux_de_completion AS ift_culture_mil_tx_comp,
    replace(replace(ift_a_la_culture_mil_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_culture_mil_chmps_non_rens,
    replace(replace(ift_a_la_culture_mil_dose_reference,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_culture_mil_dose_ref,
    replace(replace(ift_a_la_culture_mil_dose_reference_unite,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS ift_culture_mil_dose_ref_unite,
    -- Recours aux moyens bio
    recours_moyens_biologiques AS recours_aux_moyens_biologiques,
    recours_macroorganismes,
    recours_produits_biotiques_sansamm,
    recours_produits_abiotiques_sansamm,
    -- CO
    charges_operationnelles_tot_reelles AS CO_tot_reelles,
    charges_operationnelles_tot_reelles_taux_de_completion AS CO_tot_reelles_tx_comp,
    replace(replace(charges_operationnelles_tot_reelles_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS CO_tot_reell_chmps_non_rens,
    charges_operationnelles_tot_std_mil AS CO_tot_std_mil,
    charges_operationnelles_tot_std_mil_taux_de_completion AS CO_tot_std_mil_tx_comp,
    replace(replace(charges_operationnelles_tot_std_mil_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS CO_tot_std_mil_chp_non_rens,
    -- CO decomposees
    charges_operationnelles_semis_reelles as CO_semis_reel,
    charges_operationnelles_semis_std_mil as CO_semis_std_mil,
    charges_operationnelles_fertimin_reelles as CO_fertimin_reel,
    charges_operationnelles_fertimin_std_mil as CO_fertimin_std_mil,
    charges_operationnelles_epandage_orga_reelles as CO_epandage_orga_reelles,
    charges_operationnelles_epandage_orga_std_mil as CO_epandage_orga_std_mil,
    charges_operationnelles_phyto_sans_amm_reelles as CO_phyto_sans_amm_reelles,
    charges_operationnelles_phyto_sans_amm_std_mil as CO_phyto_sans_amm_std_mil,
    charges_operationnelles_phyto_avec_amm_reelles as CO_phyto_avec_amm_reelles,
    charges_operationnelles_phyto_avec_amm_std_mil as CO_phyto_avec_amm_std_mil,
    charges_operationnelles_trait_semence_reelles as CO_trait_semence_reelles,
    charges_operationnelles_trait_semence_std_mil as CO_trait_semence_std_mil,
    charges_operationnelles_irrigation_reelles as CO_irrigation_reelles,
    charges_operationnelles_irrigation_std_mil as CO_irrigation_std_mil,
    charges_operationnelles_substrats_reelles as CO_substrats_reelles,
    charges_operationnelles_substrats_std_mil as CO_substrats_std_mil,
    charges_operationnelles_pots_reelles as CO_pots_reelles,
    charges_operationnelles_pots_std_mil as CO_pots_std_mil,
    charges_operationnelles_intrants_autres_reelles as CO_intrants_autres_reelles,
    charges_operationnelles_intrants_autres_std_mil as CO_intrants_autres_std_mil,
    charges_operationnelles_reelles_decomposees_taux_de_completion as CO_decomposees_reel_tx_comp,
    charges_operationnelles_std_mil_decomposees_taux_de_completion as CO_decomposees_std_mil_tx_comp,
    replace(replace(charges_operationnelles_reelles_decomposees_detail_champs_non_r,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS CO_decomposees_reel_chp_non_rens,
    replace(replace(charges_operationnelles_std_mil_decomposees_detail_champs_non_r,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS CO_decomposees_std_mil_chp_non_rens,
	-- Ferti
    ferti_N_tot,
    ferti_N_mineral,
    ferti_N_organique,
    ferti_P2O5_tot,
    ferti_P2O5_mineral,
    ferti_P2O5_organique,
    ferti_K2O_tot,
    ferti_K2O_mineral,
    ferti_K2O_organique,
    ferti_Ca_mineral,
    ferti_CaO_organique,
    ferti_MgO_mineral,
    ferti_MgO_organique,
    ferti_SO3_mineral,
    ferti_S_organique,
    ferti_B_mineral,
    ferti_Cu_mineral,
    ferti_Fe_mineral,
    ferti_Mn_mineral,
    ferti_Mo_mineral,
    ferti_Na2O_mineral,
    ferti_Zn_mineral,
    -- Substances actives
    hri1_tot,
    hri1_hts,
    hri1_tot_taux_de_completion,
    replace(replace(hri1_tot_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') as hri1_tot_detail_champs_non_renseig,
    hri1_g1_tot,
    hri1_g1_hts,
    hri1_g1_tot_taux_de_completion,
    replace(replace(hri1_g1_tot_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') as hri1_g1_tot_detail_champs_non_renseig,
    hri1_g2_tot,
    hri1_g2_hts,
    hri1_g2_tot_taux_de_completion,
    replace(replace(hri1_g2_tot_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') as hri1_g2_tot_detail_champs_non_renseig,
    hri1_g3_tot,
    hri1_g3_hts,
    hri1_g3_tot_taux_de_completion,
    replace(replace(hri1_g3_tot_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') as hri1_g3_tot_detail_champs_non_renseig,
    hri1_g4_tot,
    hri1_g4_hts,
    hri1_g4_tot_taux_de_completion,
    replace(replace(hri1_g4_tot_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') as hri1_g4_tot_detail_champs_non_renseig,
    qsa_tot,
    qsa_tot_hts,
    qsa_tot_taux_de_completion,
    replace(replace(qsa_tot_detail_champs_non_renseig,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') as qsa_tot_detail_champs_non_renseig,
    qsa_danger_environnement,
    qsa_danger_environnement_hts,
    qsa_toxique_utilisateur,
    qsa_toxique_utilisateur_hts,
    qsa_cmr,
    qsa_cmr_hts,
    qsa_substances_candidates_substitution,
    qsa_substances_candidates_substitution_hts,
    qsa_substances_faible_risque,
    qsa_substances_faible_risque_hts,
    qsa_glyphosate,
    qsa_glyphosate_hts,
    qsa_chlortoluron,
    qsa_chlortoluron_hts,
    qsa_diflufenican,
    qsa_diflufenican_hts,
    qsa_prosulfocarbe,
    qsa_prosulfocarbe_hts,
    qsa_smetolachlore,
    qsa_smetolachlore_hts,
    qsa_boscalid,
    qsa_boscalid_hts,
    qsa_fluopyram,
    qsa_fluopyram_hts,
    qsa_lambda_cyhalothrine,
    qsa_lambda_cyhalothrine_hts,
    qsa_cuivre_tot,
    qsa_cuivre_tot_hts,
    qsa_cuivre_phyto,
    qsa_cuivre_phyto_hts,
    qsa_cuivre_ferti,
    qsa_soufre_tot,
    qsa_soufre_tot_hts,
    qsa_soufre_phyto,
    qsa_soufre_phyto_hts,
    qsa_soufre_ferti,
    qsa_bixafen,
	qsa_dicamba,
	qsa_mancozeb,
	qsa_phosmet,
	qsa_tebuconazole,
	qsa_dimethenamidp,
	qsa_pendimethalin,
	qsa_flufenacet,
	qsa_aclonifen,
	qsa_isoxaben,
	qsa_beflutamid,
	qsa_isoproturon ,
	qsa_clothianidine,
	qsa_imidaclopride,
	qsa_thiamethoxam,
	qsa_acetamipride,
	qsa_thiaclopride,
	qsa_neonicotinoides
    FROM echelle_intrant ei
    LEFT JOIN entrepot_utilisation_intrant_realise euir on euir.id = ei.id_usage
    LEFT JOIN entrepot_utilisation_intrant_synthetise euis on euis.id = ei.id_usage
    where (euir.id is not null and euis.id is null) OR (euir.id is null and euis.id is not null);

alter table entrepot_utilisation_intrant_performance
add constraint utilisation_intrant_performance_PK
PRIMARY KEY (utilisation_intrant_id);
