select 
	eirp.*,
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
	ep.nom as parcelle_nom, 
	ep.id as parcelle_id, 
	ez.nom as zone_nom,
	sdc_num_dephy as sdc_code_dephy,
	sdc_type_conduite as sdc_type_agriculture,
	sdc_valide,
	ec.nom as culture_nom, 
	ec.code as culture_code,
	enr.rang as culture_rang,
	ecoc.complet_espece_edi as culture_especes_edi,
	ecoc.variete_nom, 
	ec_prec.nom as precedent_nom, 
	ec_prec.id as precedent_id,
	ec_prec.code as precedent_code,
	epppr."type" as phase,
	epppr.id as phase_id
from entrepot_itk_realise_performance eirp
left join entrepot_culture_outils_can ecoc on eirp.culture_id = ecoc.id
left join entrepot_noeuds_realise enr on (enr.culture_id = eirp.culture_id and enr.zone_id = eirp.zone_id)
left join entrepot_plantation_perenne_realise eppr on (enr.culture_id = eppr.culture_id and enr.zone_id = eppr.zone_id)
left join entrepot_plantation_perenne_phases_realise epppr on (epppr.plantation_perenne_realise_id = eppr.id and eirp.plantation_perenne_phases_realise_id = epppr.id)
left join entrepot_culture ec on ec.id = eirp.culture_id 
left join entrepot_zone ez on ez.id = eirp.zone_id
left join entrepot_parcelle ep on ep.id = ez.parcelle_id
left join entrepot_context_performance_sdc ecps on ecps.sdc_id = ep.sdc_id
left join entrepot_connection_realise ecr on ecr.cible_noeuds_realise_id = enr.id
left join entrepot_noeuds_realise enr_prec on enr_prec.id = ecr.source_noeuds_realise_id
left join entrepot_culture ec_prec on enr_prec.culture_id = ec_prec.id;