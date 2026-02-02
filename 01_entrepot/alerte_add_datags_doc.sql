-- ENTREPOT_TABLE
INSERT INTO public.entrepot_table (id,"label",explication,category_id,is_active,"order",required_right,"generated")
	VALUES ('alerte',
	'alerte',
	'référentiel qui identifie les alertes recensées par la CAN (Cellule d''Animation Nationale du réseau DEPHY) et leurs spécifications pour créer une alerte dans les performances. Elles dépendent principalement de l''échelle de calcul et de la variable qui est concernée, mais peuvent aussi dépendre de la filière, du type d''agriculture, de l''espèce de la culture au sens large et de l''unité du rendement.',
	'referentiel',true,21,0,false);


-- ENTREPOT_COLUMN
-- itk_synthetise_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_ferti_N_tot',
'alerte_ferti_N_tot',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de fertilisation azotée',false,'itk_synthetise_performance',true,1128);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_ift_cible_non_mil_chim_tot_hts',
'alerte_ift_cible_non_mil_chim_tot_hts',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT chimique total hors traitement de semence (à la cible et non millésimé)',false,'itk_synthetise_performance',true,1129);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_ift_cible_non_mil_f',
'alerte_ift_cible_non_mil_f',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT fongicide (à la cible et non millésimé)',false,'itk_synthetise_performance',true,1130);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_ift_cible_non_mil_h',
'alerte_ift_cible_non_mil_h',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT herbicide (à la cible et non millésimé)',false,'itk_synthetise_performance',true,1131);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_ift_cible_non_mil_i',
'alerte_ift_cible_non_mil_i',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT insecticide (à la cible et non millésimé)',false,'itk_synthetise_performance',true,1132);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_ift_cible_non_mil_biocontrole',
'alerte_ift_cible_non_mil_biocontrole',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT total sans taitement de semence mais avec biocontrole (à la cible et non millésimé)',false,'itk_synthetise_performance',true,1133);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_CO_irrigation_std_mil',
'alerte_CO_irrigation_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de consommation d''eau',false,'itk_synthetise_performance',true,1134);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_MSN_std_mil_avec_autoconso',
'alerte_MSN_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de marge semi-nette (standardisé, non millésimé, avec autoconsommation)',false,'itk_synthetise_performance',true,1135);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_nombre_interventions_phyto',
'alerte_nombre_interventions_phyto',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur du nombre d''intervention de traitements phytosanitaires',false,'itk_synthetise_performance',true,1136);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_PB_std_mil_avec_autoconso',
'alerte_PB_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de produit brut (standardisé, non millésimé, avec autoconsommation)',false,'itk_synthetise_performance',true,1137);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'itk_synthetise_performance',true,1138);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_CM_std_mil',
'alerte_CM_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge de mécanisation (standardisé et non millésimé)',false,'itk_synthetise_performance',true,1139);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alerte_CO_semis_std_mil',
'alerte_CO_semis_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge opérationnelle de semis (standardisé et non milléismé)',false,'itk_synthetise_performance',true,1140);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_synthetise_performance_alertes_charges',
'alertes_charges',
'alertes se déclenchant si les conditions ne sont pas respectées pour la somme de l''indicateurs de charges opérationnelles totales et de celui de mécanisation (standardisé et non millésimé)',false,'itk_synthetise_performance',true,1141);


-- itk_realise_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_ferti_N_tot',
'alerte_ferti_N_tot',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de fertilisation azotée',false,'itk_realise_performance',true,1128);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_ift_cible_non_mil_chim_tot_hts',
'alerte_ift_cible_non_mil_chim_tot_hts',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT chimique total hors traitement de semence (à la cible et non millésimé)',false,'itk_realise_performance',true,1129);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_ift_cible_non_mil_f',
'alerte_ift_cible_non_mil_f',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT fongicide (à la cible et non millésimé)',false,'itk_realise_performance',true,1130);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_ift_cible_non_mil_h',
'alerte_ift_cible_non_mil_h',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT herbicide (à la cible et non millésimé)',false,'itk_realise_performance',true,1131);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_ift_cible_non_mil_i',
'alerte_ift_cible_non_mil_i',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT insecticide (à la cible et non millésimé)',false,'itk_realise_performance',true,1132);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_ift_cible_non_mil_biocontrole',
'alerte_ift_cible_non_mil_biocontrole',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT total sans taitement de semence mais avec biocontrole (à la cible et non millésimé)',false,'itk_realise_performance',true,1133);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_CO_irrigation_std_mil',
'alerte_CO_irrigation_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de consommation d''eau',false,'itk_realise_performance',true,1134);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_MSN_std_mil_avec_autoconso',
'alerte_MSN_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de marge semi-nette (standardisé, non millésimé, avec autoconsommation)',false,'itk_realise_performance',true,1135);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_nombre_interventions_phyto',
'alerte_nombre_interventions_phyto',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur du nombre d''intervention de traitements phytosanitaires',false,'itk_realise_performance',true,1136);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_PB_std_mil_avec_autoconso',
'alerte_PB_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de produit brut (standardisé, non millésimé, avec autoconsommation)',false,'itk_realise_performance',true,1137);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'itk_realise_performance',true,1138);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_CM_std_mil',
'alerte_CM_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge de mécanisation (standardisé et non millésimé)',false,'itk_realise_performance',true,1139);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alerte_CO_semis_std_mil',
'alerte_CO_semis_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge opérationnelle de semis (standardisé et non milléismé)',false,'itk_realise_performance',true,1140);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('itk_realise_performance_alertes_charges',
'alertes_charges',
'alertes se déclenchant si les conditions ne sont pas respectées pour la somme de l''indicateurs de charges opérationnelles totales et de celui de mécanisation (standardisé et non millésimé)',false,'itk_realise_performance',true,1141);


-- sdc_realise_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_ferti_N_tot',
'alerte_ferti_N_tot',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de fertilisation azotée',false,'sdc_realise_performance',true,1128);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_ift_cible_non_mil_chim_tot_hts',
'alerte_ift_cible_non_mil_chim_tot_hts',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT chimique total hors traitement de semence (à la cible et non millésimé)',false,'sdc_realise_performance',true,1129);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_ift_cible_non_mil_f',
'alerte_ift_cible_non_mil_f',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT fongicide (à la cible et non millésimé)',false,'sdc_realise_performance',true,1130);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_ift_cible_non_mil_h',
'alerte_ift_cible_non_mil_h',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT herbicide (à la cible et non millésimé)',false,'sdc_realise_performance',true,1131);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_ift_cible_non_mil_i',
'alerte_ift_cible_non_mil_i',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT insecticide (à la cible et non millésimé)',false,'sdc_realise_performance',true,1132);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_ift_cible_non_mil_biocontrole',
'alerte_ift_cible_non_mil_biocontrole',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT total sans taitement de semence mais avec biocontrole (à la cible et non millésimé)',false,'sdc_realise_performance',true,1133);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_CO_irrigation_std_mil',
'alerte_CO_irrigation_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de consommation d''eau',false,'sdc_realise_performance',true,1134);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_MSN_std_mil_avec_autoconso',
'alerte_MSN_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de marge semi-nette (standardisé, non millésimé, avec autoconsommation)',false,'sdc_realise_performance',true,1135);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_nombre_interventions_phyto',
'alerte_nombre_interventions_phyto',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur du nombre d''intervention de traitements phytosanitaires',false,'sdc_realise_performance',true,1136);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_PB_std_mil_avec_autoconso',
'alerte_PB_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de produit brut (standardisé, non millésimé, avec autoconsommation)',false,'sdc_realise_performance',true,1137);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'sdc_realise_performance',true,1138);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_CM_std_mil',
'alerte_CM_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge de mécanisation (standardisé et non millésimé)',false,'sdc_realise_performance',true,1139);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_CO_semis_std_mil',
'alerte_CO_semis_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge opérationnelle de semis (standardisé et non milléismé)',false,'sdc_realise_performance',true,1140);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alertes_charges',
'alertes_charges',
'alertes se déclenchant si les conditions ne sont pas respectées pour la somme de l''indicateurs de charges opérationnelles totales et de celui de mécanisation (standardisé et non millésimé)',false,'sdc_realise_performance',true,1141);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_realise_performance_alerte_tps_travail_total',
'alerte_tps_travail_total',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de temps de travail total',false,'sdc_realise_performance',true,1142);

-- synthetise_synthetise_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_ferti_N_tot',
'alerte_ferti_N_tot',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de fertilisation azotée',false,'synthetise_synthetise_performance',true,1128);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_ift_cible_non_mil_chim_tot_hts',
'alerte_ift_cible_non_mil_chim_tot_hts',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT chimique total hors traitement de semence (à la cible et non millésimé)',false,'synthetise_synthetise_performance',true,1129);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_ift_cible_non_mil_f',
'alerte_ift_cible_non_mil_f',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT fongicide (à la cible et non millésimé)',false,'synthetise_synthetise_performance',true,1130);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_ift_cible_non_mil_h',
'alerte_ift_cible_non_mil_h',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT herbicide (à la cible et non millésimé)',false,'synthetise_synthetise_performance',true,1131);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_ift_cible_non_mil_i',
'alerte_ift_cible_non_mil_i',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT insecticide (à la cible et non millésimé)',false,'synthetise_synthetise_performance',true,1132);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_ift_cible_non_mil_biocontrole',
'alerte_ift_cible_non_mil_biocontrole',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur d''IFT total sans taitement de semence mais avec biocontrole (à la cible et non millésimé)',false,'synthetise_synthetise_performance',true,1133);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_CO_irrigation_std_mil',
'alerte_CO_irrigation_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de consommation d''eau',false,'synthetise_synthetise_performance',true,1134);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_MSN_std_mil_avec_autoconso',
'alerte_MSN_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de marge semi-nette (standardisé, non millésimé, avec autoconsommation)',false,'synthetise_synthetise_performance',true,1135);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_nombre_interventions_phyto',
'alerte_nombre_interventions_phyto',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur du nombre d''intervention de traitements phytosanitaires',false,'synthetise_synthetise_performance',true,1136);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_PB_std_mil_avec_autoconso',
'alerte_PB_std_mil_avec_autoconso',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de produit brut (standardisé, non millésimé, avec autoconsommation)',false,'synthetise_synthetise_performance',true,1137);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'synthetise_synthetise_performance',true,1138);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_CM_std_mil',
'alerte_CM_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge de mécanisation (standardisé et non millésimé)',false,'synthetise_synthetise_performance',true,1139);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_CO_semis_std_mil',
'alerte_CO_semis_std_mil',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de charge opérationnelle de semis (standardisé et non milléismé)',false,'synthetise_synthetise_performance',true,1140);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alertes_charges',
'alertes_charges',
'alertes se déclenchant si les conditions ne sont pas respectées pour la somme de l''indicateurs de charges opérationnelles totales et de celui de mécanisation (standardisé et non millésimé)',false,'synthetise_synthetise_performance',true,1141);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('synthetise_synthetise_performance_alerte_tps_travail_total',
'alerte_tps_travail_total',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de temps de travail total',false,'synthetise_synthetise_performance',true,1142);

-- intervention_realise_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('intervention_realise_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'intervention_realise_performance',true,1128);

-- intervention_synthetise_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('intervention_synthetise_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'intervention_synthetise_performance',true,1128);

-- utilisation_intrant_performance
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('utilisation_intrant_performance_alerte_rendement',
'alerte_rendement',
'alertes se déclenchant si les conditions ne sont pas respectées pour l''indicateur de rendement',false,'utilisation_intrant_performance',true,1128);
 
-- alerte
INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_id',
'id',
'identifiant de l''alerte',false,'alerte',true,0);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_nom_alerte',
'nom_alerte',
'nom de l''alerte',false,'alerte',true,1);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_num_alerte',
'num_alerte',
'numéro de l''alerte. Le numéro permet de grouper les alertes par même type de variable concernée. De plus les spécificités des alertes ayant le même numéro ne se chevauchent pas (par exemple les alertes ayant le numéro 15 portent toutes sur le rendement mais diffèrent par l''unité de rendement saisie)',false,'alerte',true,2);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_variable_concernee',
'variable_concernee',
'variable dans Agrosyst concernée par l''alerte',false,'alerte',true,3);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_echelle_calcul',
'echelle_calcul',
'échelle à partir de laquelle l''alerte est calculée ("SDC", "CROP", "INPUT"). Elle est souvent calculée à partir des autres indicateurs',false,'alerte',true,4);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_filiere',
'filiere',
'filière du système de culture pour laquelle vaut l''alerte',false,'alerte',true,5);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_bio',
'bio',
'booléen qui spécifie si le type d''agriculture pour laquelle vaut l''alerte est bio ou non. Les systèmes en conversion vers l''agriculture biologique sont considérés bio',false,'alerte',true,6);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_rendement_unite',
'rendement_unite',
'unité de rendement pour laquelle vaut l''alerte. Disponible uniquement pour les indicateurs de rendements',false,'alerte',true,7);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_code_espece_botanique',
'code_espece_botanique',
'code de l''espèce de la culture pour laquelle vaut l''alerte',false,'alerte',true,8);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_libelle_espece_botanique',
'libelle_espece_botanique',
'libellé de l''espèce de la culture pour laquelle vaut l''alerte',false,'alerte',true,9);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_code_qualifiant_aee',
'code_qualifiant_aee',
'code du qualifiant de la culture pour laquelle vaut l''alerte. Exemple de qualifiant : "Protéagineux" pour le Pois, "Fibre" pour le Lin',false,'alerte',true,10);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_libelle_qualifiant_aee',
'libelle_qualifiant_aee',
'libellé du qualifiant de la culture pour laquelle vaut l''alerte. Exemple de qualifiant : "Protéagineux" pour le Pois, "Fibre" pour le Lin',false,'alerte',true,11);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_code_type_saisonnier_aee',
'code_type_saisonnier_aee',
'code du type saisionier de la culture pour laquelle vaut l''alerte. Exemple de type saisonnier : "Hiver", "Printemps" ...',false,'alerte ',true,12);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_libelle_type_saisonnier_aee',
'libelle_type_saisonnier_aee',
'libellé du type saisionier de la culture pour laquelle vaut l''alerte. Exemple de type saisonnier : "Hiver", "Printemps" ...',false,'alerte',true,13);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_seuil_min',
'seuil_min',
'seuil minimum en dessous duquel l''alerte ''alerte_valeur_si_inferieur_a_seuil'' est déclenchée',false,'alerte',true,14);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_seuil_min_inclus',
'seuil_min_inclus',
'booléen qui spécifie si le seuil minimal est inclu ou non dans la condition qui déclenche l''alerte',false,'alerte',true,15);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_seuil_max',
'seuil_max',
'seuil maximum au dessus duquel l''alerte ''alerte_valeur_si_superieur_a_seuil'' est déclenchée',false,'alerte',true,16);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_seuil_max_inclus',
'seuil_max_inclus',
'booléen qui spécifie si le seuil maximum est inclu ou non dans la condition qui déclenche l''alerte',false,'alerte ',true,17);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_valeur_si_dans_seuil',
'valeur_si_dans_seuil',
'valeur à renvoyer si la variable considérée est bien contenue dans les seuils',false,'alerte',true,18);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_valeur_si_inferieur_a_seuil',
'valeur_si_inferieur_a_seuil',
'valeur de l''alerte si la variable considérée est en dessous du seuil minimum',false,'alerte',true,19);

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('alerte_valeur_si_superieur_a_seuil',
'valeur_si_superieur_a_seuil',
'valeur de l''alerte si la variable considérée est au dessus du seuil maximum',false,'alerte',true,20);



-- NEWS
-- news
INSERT INTO public.news (id,"date")
	VALUES ('news_20260202','2026-02-02');

-- news_section
INSERT INTO public.news_section (id,type_id,news_id)
	VALUES ('new_section_news_20260202_new_table','new_table','news_20260202');
INSERT INTO public.news_section (id,type_id,news_id)
	VALUES ('new_section_news_20260202_new_column','new_column','news_20260202');

-- news_section_item
INSERT INTO public.news_section_item (id,value,"order",source_id,news_section_id)
	VALUES (uuid_generate_v4(),
	'Nouvelle table de référentiel : alerte',
	0,'entrepot','new_section_news_20260202_new_table');
	
INSERT INTO public.news_section_item (id,value,"order",source_id,news_section_id)
	VALUES (uuid_generate_v4(),
	'Ajout de 15 colonnes d''alertes dans les tables de performances "itk_synthetise_performance", "itk_realise_performance", "sdc_realise_performance" et "synthetise_synthetise_performance":
	* ''alerte_ferti_N_tot''
	* ''alerte_ift_cible_non_mil_chim_tot_hts''
	* ''alerte_ift_cible_non_mil_f''
	* ''alerte_ift_cible_non_mil_h''
	* ''alerte_ift_cible_non_mil_i''
	* ''alerte_ift_cible_non_mil_biocontrole''
	* ''alerte_CO_irrigation_std_mil''
	* ''alerte_MSN_std_mil_avec_autoconso''
	* ''alerte_nombre_interventions_phyto''
	* ''alerte_PB_std_mil_avec_autoconso''
	* ''alerte_rendement''
	* ''alertes_charges''
	* ''alerte_CM_std_mil''
	* ''alerte_CO_semis_std_mil''',
	0,'entrepot','new_section_news_20260202_new_column');

INSERT INTO public.news_section_item (id,value,"order",source_id,news_section_id)
	VALUES (uuid_generate_v4(),
	'Ajout de la colonne d''alerte ''alerte_rendement'' dans les tables de performances "intervention_synthetise_performance", "intervention_realise_performance" et "utilisation_intrant_performance".',
	1,'entrepot','new_section_news_20260202_new_column');
