select 
	esrp.*,
	ecps.domaine_nom,
	ecps.domaine_id,
	ecps.domaine_campagne,
	ecps.domaine_departement as departement,
	ecps.domaine_type,
	ecps.dispositif_id,
	ecps.dispositif_type,
	ecps.nom_reseau_it,
	ecps.nom_reseau_ir,
	ecps.sdc_filiere,
	ecps.sdc_nom,
	ecps.sdc_num_dephy as sdc_code_dephy,
	ecps.sdc_type_conduite as sdc_type_agriculture,
	ecps.sdc_valide,
	esroc.especes
from entrepot_sdc_realise_performance esrp
join entrepot_context_performance_sdc ecps on esrp.sdc_id =ecps.sdc_id
join entrepot_sdc_realise_outils_can esroc on esroc.id = esrp.sdc_id;