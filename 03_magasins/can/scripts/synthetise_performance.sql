SELECT 
    essp.*,
    sdc_context.domaine_nom,
   	sdc_context.domaine_id,
   	sdc_context.domaine_campagne,
   	sdc_context.domaine_type,
   	sdc_context.domaine_departement as departement,
   	sdc_context.dispositif_id,
   	sdc_context.dispositif_type,
   	sdc_context.nom_reseau_it,
   	sdc_context.nom_reseau_ir,
   	sdc_context.sdc_filiere,
	sdc_context.sdc_num_dephy as sdc_code_dephy,
	sdc_context.sdc_type_conduite as sdc_type_agriculture,
   	sdc_context.sdc_nom,
   	sdc_context.sdc_id,
	sdc_context.sdc_valide
FROM entrepot_synthetise_synthetise_performance essp
left join entrepot_synthetise es on essp.synthetise_id = es.id
left join entrepot_context_performance_sdc sdc_context on sdc_context.sdc_id = es.sdc_id;
