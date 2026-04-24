[
        'code_dephy',
        'realized',
        'sdc_id',
        'synthetise_id',
        'entite_id',
        'dispositif_id',
        'domaine_id',
        'commune_id',

        'new_campagne',
        'pz0',
        'c103_networkYears',

        'codeinsee',
        'departement',
        'region',
        'bassin_viticole',
        'ancienne_region',
        'latitude',
        'longitude',
        'arrondissement',

        'filiere',
        'type_production',
        'type_agriculture',

        'reseaux_ir',
        'reseaux_it',

        'c111_species',
        'c112_variety',
        'c113_grapeVar',

        'c120_arboriculture_typo_sdc',
        'c121_maraichage_typo_sdc',
        'c122_horticulture_typo_sdc',
        'c123_cult_tropicales_typo_sdc',
        'c124_gcpe_typo_sdc',

        'ift_cible_non_mil_chimique_tot',
        'ift_cible_non_mil_chim_tot_hts',
        'ift_cible_non_mil_hh',
        'c602_IFT_hh_hts',
        'ift_cible_non_mil_h',
        'ift_cible_non_mil_f',
        'ift_cible_non_mil_i',
        'ift_cible_non_mil_ts',
        'ift_cible_non_mil_a',
        'ift_cible_non_mil_biocontrole',
        'recours_aux_moyens_biologiques',

        'hri1_hts',
        'hri1_g1_hts',
        'hri1_g2_hts',
        'hri1_g3_hts',
        'hri1_g4_hts',
        
        'qsa_tot_hts',
        'qsa_danger_environnement_hts',
        'qsa_toxique_utilisateur_hts',
        'qsa_cmr_hts',
        'qsa_glyphosate_hts',
        'qsa_cuivre_tot_hts',
        'qsa_soufre_tot_hts',

        'ferti_n_tot',
        'ferti_n_mineral',
        'ferti_n_organique',
        'ferti_p2o5_tot',
        'ferti_p2o5_mineral',
        'ferti_p2o5_organique',
        'ferti_k2o_tot',
        'ferti_k2o_mineral',
        'ferti_k2o_organique',

        'pb_std_mil_avec_autoconso',
        'mb_std_mil_avec_autoconso',
        'msn_reelle_avec_autoconso',
        'md_std_mil_avec_autoconso',

        'c504_outLabourTotalExpenses',
        'co_tot_std_mil',
        'cm_std_mil',
        'c_main_oeuvre_tot_std_mil',
        'c_main_oeuvre_tractoriste_std_mil',
        'c_main_oeuvre_manuelle_std_mil',
        'conso_carburant',

        'tps_utilisation_materiel',
        'tps_travail_manuel',
        'tps_travail_total',

        'surface_par_unite_de_travail_humain',
        'nombre_uth_necessaires',
        'nbre_de_passages_desherbage_meca',
        'utili_desherbage_meca',
        'type_de_travail_du_sol',

        'c701_totalIFT_evol_diff',
        'c702_IFT_hh_hts_evol_diff',
        'c703_biocontrolIFT_evol_diff',
        'c705_herbicideIFT_evol_diff',
        'c707_insecticideIFT_evol_diff',
        'c708_fungicideIFT_evol_diff',
        'c709_otherIFT_evol_diff',
        'c710_biologicalWaysSolution_evol_diff'
    ]
    


    # Renommer les colonnes et ajouter les nécessaires

# 1. Renommer les colonnes
df = df.rename(columns={
    'synthetise_id' 				            : "systeme_synthetise_id",
	'approche_de_calcul' 				        : "realized",
	# 'ift_cible_non_mil_chimique_tot' 			: "aaaaa",
    'ift_cible_non_mil_chim_tot_hts' 			: "c601_totalIFT",
	'ift_cible_non_mil_h' 				        : "c605_herbicideIFT",
    'ift_cible_non_mil_f' 				        : "c608_fungicideIFT",
	'ift_cible_non_mil_i' 				        : "c607_insecticideIFT",
	# 'ift_cible_non_mil_ts' 				    : "aaaaa",
    'ift_cible_non_mil_a' 				        : "c609_otherIFT",
	# 'ift_cible_non_mil_hh' 				    : "aaaaa",
    'ift_cible_non_mil_biocontrole' 			: "c603_biocontrolIFT",
	# 'ift_cible_non_mil_tx_comp' 				: "aaaaa",
    'recours_aux_moyens_biologiques' 			: "c610_biologicalWaysSolution",
    # 'c701_totalIFT_evol_diff'		            : "aaaaa" # Garde le même nom
    # 'c702_IFT_hh_hts_evol_diff'		        : "aaaaa" # Garde le même nom
    # 'c703_biocontrolIFT_evol_diff'		    : "aaaaa" # Garde le même nom
    # 'c705_herbicideIFT_evol_diff'		        : "aaaaa" # Garde le même nom
    # 'c707_insecticideIFT_evol_diff'		    : "aaaaa" # Garde le même nom
    # 'c708_fungicideIFT_evol_diff'		        : "aaaaa" # Garde le même nom
    # 'c709_otherIFT_evol_diff'		            : "aaaaa" # Garde le même nom
	'tps_utilisation_materiel' 			    	: "c302_mechanizationTime",
    'tps_travail_manuel' 				        : "c303_labourTime",
	'tps_travail_total' 				        : "c301_workingTime",
    'nbre_de_passages_desherbage_meca' 			: "c204_mechanicalWeedingInterventionFrequency",
	'utili_desherbage_meca' 			       	: "c203_mechanicalWeeding",
    'type_de_travail_du_sol' 			    	: "c201_groundWorkType",
	'co_tot_std_mil' 			            	: "c505_operatingExpenses",
	'cm_std_mil' 				                : "c507_mechanizationExpenses",
    'c_main_oeuvre_tot_std_mil' 				: "c506_labourExpenses",
	# 'c_main_oeuvre_tractoriste_std_mil' 		: "aaaaa",
    # 'c_main_oeuvre_manuelle_std_mil' 			: "aaaaa",
	'pb_std_mil_avec_autoconso' 				: "c501_grossProceeds",
    'mb_std_mil_avec_autoconso' 				: "c502_grossProfit",
	'msn_reelle_avec_autoconso' 				: "c503_semiNetMargin",
    # 'c504_outLabourTotalExpenses'				: "aaaaa" # Garde le même nom
	'md_std_mil_avec_autoconso' 				: "c508_DirectMargin", # A ajouter en invisible
	# 'surface_par_unite_de_travail_humain' 	: "aaaaa",
    # 'nombre_uth_necessaires' 				    : "aaaaa",
	'conso_carburant' 				            : "c304_fuelConsumption",
	'ferti_n_tot' 				                : "c401_fertilizationUnityN",
    'ferti_n_mineral' 			            	: "c402_fertilizationMineralUnityN",
	'ferti_n_organique' 				        : "c403_fertilizationOrganicUnityN",
	'ferti_p2o5_tot' 	            			: "c404_fertilizationUnityP",
    'ferti_p2o5_mineral' 	        			: "c405_fertilizationMineralUnityP",
	'ferti_p2o5_organique' 		        		: "c406_fertilizationOrganicUnityP",
	'ferti_k2o_tot' 				            : "c407_fertilizationUnityK",
    'ferti_k2o_mineral' 			        	: "c408_fertilizationMineralUnityK",
	'ferti_k2o_organique' 				        : "c409_fertilizationOrganicUnityK",
	'hri1_hts' 				                    : "c633_hri1tothts",
	'hri1_g1_hts' 			                	: "c634_hri1g1hts",
    'hri1_g2_hts' 			                	: "c635_hri1g2hts",
	'hri1_g3_hts' 			                	: "c636_hri1g3hts",
	'hri1_g4_hts' 		                		: "c637_hri1g4hts",
	'qsa_tot_hts' 			                	: "c640_qteSubstActive", # A ajouter en invisible
    'qsa_danger_environnement_hts' 				: "c644_qteSubstdangerenvironnement",
	'qsa_toxique_utilisateur_hts' 				: "c642_qteSubsttoxique",
    'qsa_cmr_hts' 				                : "c641_qteSubstCMR",
	'qsa_glyphosate_hts' 			            : "c643_qteSubstglyphosate",
	'qsa_cuivre_tot_hts' 				        : "c645_qteSubstcuivre",
    'qsa_soufre_tot_hts' 			          	: "c646_qteSubstsoufre",
	# 'nom' 				                    : "aaaaa",
	# 'synthetise_campagne' 				    : "aaaaa",
	# 'sdc_id' 				                    : "aaaaa", # Garde le même nom
	# 'code' 				                    : "aaaaa",
    # 'nom_sdc' 				                : "aaaaa",
	# 'modalite_suivi_dephy' 			        : "aaaaa",
	'code_dephy' 				                : "dephyNb",
	# 'validite' 				                : "aaaaa",
	'filiere' 				                    : "c101_sector",
    # 'type_production' 			            : "aaaaa",
	'type_agriculture' 			            	: "c110_managementType",
	'part_sau_domaine' 			            	: "aaaaa",
    'dispositif_id' 			            	: "aaaaa",
	# 'reseaux_ir' 				                : "aaaaa", # A laisser pour DEPHY dans Ags-team
	# 'reseaux_it' 			                	: "aaaaa", # A laisser pour DEPHY dans Ags-team
	# 'type' 				                    : "aaaaa",
	# 'domaine_id' 			                	: "aaaaa",
    # 'code_domaine' 				            : "aaaaa",
	# 'nom_domaine' 			                : "aaaaa",
	# 'campagne' 			                    : "aaaaa",
	# 'commune_id' 		                		: "aaaaa",
	# 'sau_totale' 		                		: "aaaaa",
    'pz0' 				                        : "c102_pz0",
	'new_campagne' 		                		: "c104_campaign_dis",
    # 'c103_networkYears'						: "aaaaa", # Garde le même nom
	# 'group_id' 				                : "aaaaa",
	# 'c111_species' 			                : "aaaaa", # Garde le même nom
	# 'c112_variety' 			                : "aaaaa", # Garde le même nom
    # 'c113_grapeVar' 			            	: "aaaaa", # Garde le même nom
	# 'c120_arboriculture_typo_sdc'             : "aaaaa", # Garde le même nom
    # 'c121_maraichage_typo_sdc' 		        : "aaaaa", # Garde le même nom
	# 'c122_horticulture_typo_sdc' 				: "aaaaa", # Garde le même nom
    # 'c123_cult_tropicales_typo_sdc' 	 		: "aaaaa", # Garde le même nom
	# 'c124_gcpe_typo_sdc' 				        : "aaaaa", # Garde le même nom
	# 'codeinsee' 				                : "aaaaa",
    'departement' 				                : "c107_departement",
	'region' 				                    : "c105_administrativeRegion",
	'bassin_viticole' 			            	: "c108_wineBasin",
	'ancienne_region' 			            	: "c106_regionPre2015",
    # 'latitude' 				                : "aaaaa", # Garde le même nom
	# 'longitude' 			                	: "aaaaa", # Garde le même nom
	# 'c602_IFT_hh_hts' 			            : "aaaaa" # Garde le même nom
})

# 2. Ajout des colonnes dont on a besoin pour IPM ou même pour DG
df['validation'] = True
df['c100_networksource'] = "DEPHY Ferme"
df['c1001_networksource'] = "DEPHY Ferme"
df['c109_country'] = "France"

df['c9303_labourTime'] = 		None # df['c303_labourTime']
df['c9502_grossProfit'] = 		None # df['c502_grossProfit']
df['c9503_semiNetMargin'] = 	None # df['c503_semiNetMargin']
df['c9506_labourExpenses'] = 	None # df['c506_labourExpenses']
df['c9633_hri1tothts_ipm'] = 	None # df['c633_hri1tothts']
df['c9634_hri1g1hts_ipm'] = 	None # df['c634_hri1g1hts']
df['c9635_hri1g2hts_ipm'] = 	None # df['c635_hri1g2hts']
df['c9636_hri1g3hts_ipm'] = 	None # df['c636_hri1g3hts']
df['c9637_hri1g4hts_ipm'] = 	None # df['c637_hri1g4hts']


# 3. Sélectionner les colonnes
list_needed_columns = [
	'dephyNb',
	'latitude',
	'longitude',
	'realized',
	'sdc_id',
	'systeme_synthetise_id',
	'validation',
	'arrondissement',
    'reseaux_ir', # metadata : que Agsteam
    'reseaux_it', # metadata : que Agsteam
	'c100_networksource',
	'c1001_networksource',
	'c101_sector',
	'c102_pz0',
	'c104_campaign_dis',
	'c105_administrativeRegion',
	'c106_regionPre2015',
	'c107_departement',
	'c108_wineBasin',
	'c109_country',
	'c110_managementType',
	'c111_species',
	'c112_variety',
	'c113_grapeVar',
	'c120_arboriculture_typo_sdc',
	'c121_maraichage_typo_sdc',
	'c122_horticulture_typo_sdc',
	'c123_cult_tropicales_typo_sdc',
	'c124_gcpe_typo_sdc',
	'c201_groundWorkType',
	'c203_mechanicalWeeding',
	'c204_mechanicalWeedingInterventionFrequency',
	'c301_workingTime',
	'c302_mechanizationTime',
	'c303_labourTime',
	'c304_fuelConsumption',
	'c401_fertilizationUnityN',
	'c402_fertilizationMineralUnityN',
	'c403_fertilizationOrganicUnityN',
	'c404_fertilizationUnityP',
	'c405_fertilizationMineralUnityP',
	'c406_fertilizationOrganicUnityP',
	'c407_fertilizationUnityK',
	'c408_fertilizationMineralUnityK',
	'c409_fertilizationOrganicUnityK',
	'c501_grossProceeds',
	'c502_grossProfit',
	'c503_semiNetMargin',
	'c504_outLabourTotalExpenses',
	'c505_operatingExpenses',
	'c506_labourExpenses',
	'c507_mechanizationExpenses',
    'c508_DirectMargin', # metadata : que pour Agsteam
	'c601_totalIFT',
	'c602_IFT_hh_hts',
	'c603_biocontrolIFT',
	'c605_herbicideIFT',
	'c607_insecticideIFT',
	'c608_fungicideIFT',
	'c609_otherIFT',
	'c610_biologicalWaysSolution',
	'c633_hri1tothts',
	'c634_hri1g1hts',
	'c635_hri1g2hts',
	'c636_hri1g3hts',
	'c637_hri1g4hts',
	'c640_qteSubstActive', # metadata : remplace IFTnormé, ne mettre dispo que sur Agsteam
	'c641_qteSubstCMR',
	'c642_qteSubsttoxique',
	'c643_qteSubstglyphosate',
	'c644_qteSubstdangerenvironnement',
	'c645_qteSubstcuivre',
	'c646_qteSubstsoufre',
	'c9303_labourTime',
	'c9502_grossProfit',
	'c9503_semiNetMargin',
	'c9506_labourExpenses',
	'c9633_hri1tothts_ipm',
	'c9634_hri1g1hts_ipm',
	'c9635_hri1g2hts_ipm',
	'c9636_hri1g3hts_ipm',
	'c9637_hri1g4hts_ipm'
]
