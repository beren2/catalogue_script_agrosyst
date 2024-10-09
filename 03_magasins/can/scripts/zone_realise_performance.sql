select 
	ezrp.*,
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
	ep.id as parcelle_id, 
	ez.nom as zone_nom, 
	ezroc.culture_especes_edi, 
	ezroc.variete_nom, 
	ezroc.rendement_culture
from entrepot_zone_realise_performance ezrp 
join entrepot_zone_realise_outils_can ezroc on ezroc.id = ezrp.zone_id 
join entrepot_zone ez on ezroc.id = ez.id
join entrepot_parcelle ep on ep.id = ez.parcelle_id
join entrepot_context_performance_sdc ecps on ecps.sdc_id = ep.sdc_id;