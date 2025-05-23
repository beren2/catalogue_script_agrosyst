
select -- requête spécifique aux cultures assolées
	eisp.*,
	ecps.domaine_nom,
	ecps.domaine_id,
	ecps.domaine_campagne,
	ecps.domaine_type,
	ecps.domaine_departement as departement,
	ecps.nom_reseau_it,
	ecps.nom_reseau_ir,
	ecps.dispositif_id,
	ecps.dispositif_type,
	ecps.sdc_filiere,
	ecps.sdc_nom,
	ecps.sdc_id,
	es.id as synthetise_id, 
	sdc_num_dephy as sdc_code_dephy,
	sdc_type_conduite as sdc_type_agriculture,
	sdc_valide,
	ec.nom as culture_nom, 
	ec.code as culture_code,
	ens_cible.rang as culture_rang,
	ecoc.complet_espece_edi as culture_especes_edi,
	ecoc.variete_nom, 
	ec_prec.nom as precedent_nom, 
	ec_prec.id as precedent_id,
	ec_prec.code as precedent_code,
	eps.id as connexion_id, 
	null as phase,
	null as phase_id
from entrepot_itk_synthetise_performance eisp
join entrepot_connection_synthetise eps on (eps.id = eisp.connection_synthetise_id)
left join entrepot_noeuds_synthetise ens_cible on (ens_cible.id = eps.cible_noeuds_synthetise_id)
left join entrepot_noeuds_synthetise_restructure ens_cible_restructure on (ens_cible.id = ens_cible_restructure.id)
left join entrepot_noeuds_synthetise ens_source on (ens_source.id = eps.cible_noeuds_synthetise_id)
left join entrepot_noeuds_synthetise_restructure ens_source_restructure on (ens_source.id = ens_source_restructure.id)
left join entrepot_culture_outils_can ecoc on (ens_cible_restructure.culture_id = ecoc.id )
left join entrepot_synthetise es ON (ens_cible.synthetise_id = es.id)
left join entrepot_culture ec on ec.id = ecoc.id
left join entrepot_context_performance_sdc ecps on ecps.sdc_id = es.sdc_id
left join entrepot_culture ec_prec on ens_source_restructure.culture_id = ec_prec.id
UNION ALL
select -- requête spécifiques aux cultures perennes
	eisp.*,
	ecps.domaine_nom,
	ecps.domaine_id,
	ecps.domaine_campagne,
	ecps.domaine_type,
	ecps.domaine_departement as departement,
	ecps.nom_reseau_it,
	ecps.nom_reseau_ir,
	ecps.dispositif_id,
	ecps.dispositif_type,
	ecps.sdc_filiere,
	ecps.sdc_nom,
	ecps.sdc_id,
	es.id as synthetise_id, 
	sdc_num_dephy as sdc_code_dephy,
	sdc_type_conduite as sdc_type_agriculture,
	sdc_valide,
	ec.nom as culture_nom, 
	ec.code as culture_code,
	null as culture_rang,
	ecoc.complet_espece_edi as culture_especes_edi,
	ecoc.variete_nom, 
	null as precedent_nom, 
	null as precedent_id,
	null as precedent_code,
	eppps."type" as phase,
	eppps.id as phase_id,
	null as connexion_id
from entrepot_itk_synthetise_performance eisp
join entrepot_plantation_perenne_phases_synthetise eppps on (eppps.id = eisp.plantation_perenne_phases_synthetise_id)
left join entrepot_plantation_perenne_synthetise epps on (epps.id = eppps.plantation_perenne_synthetise_id)
left join entrepot_plantation_perenne_synthetise_restructure epps_restructure on (epps.id = epps_restructure.id)
left join entrepot_culture_outils_can ecoc on (epps_restructure.culture_id = ecoc.id)
left join entrepot_synthetise es ON (epps.synthetise_id = es.id)
left join entrepot_culture ec on ec.id = ecoc.id
left join entrepot_context_performance_sdc ecps on ecps.sdc_id = es.sdc_id;