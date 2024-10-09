select 
	eprp.*,
	ecps.domaine_nom,
	ecps.domaine_id ,
	ecps.domaine_campagne,
	ecps.domaine_type,
	ecps.domaine_departement as departement,
	ecps.dispositif_id,
	ecps.dispositif_type,
	ecps.nom_reseau_it,
	ecps.nom_reseau_ir,
	ecps.sdc_filiere,
	ecps.sdc_nom,
	ecps.sdc_id,
	ecps.sdc_num_dephy as sdc_code_dephy,
	ecps.sdc_type_conduite as sdc_type_agriculture,
	ecps.sdc_valide,
	ep.nom as parcelle_nom, 
	eproc.especes, 
	eproc.varietes, 
	eproc.rendement
from entrepot_parcelle_realise_performance eprp 
join entrepot_parcelle_realise_outils_can eproc on eproc.id = eprp.parcelle_id 
join entrepot_parcelle ep on ep.id = eprp.parcelle_id
join entrepot_context_performance_sdc ecps on ecps.sdc_id = ep.sdc_id;