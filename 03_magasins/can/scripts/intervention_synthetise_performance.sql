SELECT
    eisp.*,
   	sdc_context.domaine_nom,
   	sdc_context.domaine_id,
   	sdc_context.domaine_campagne,
   	sdc_context.domaine_type,
   	sdc_context.domaine_departement as departement,
   	sdc_context.dispositif_id,
   	sdc_context.dispositif_type,
   	sdc_context.nom_reseau_it,
   	sdc_context.nom_reseau_ir,
   	sdc_context.sdc_nom,
   	sdc_context.sdc_id,
   	sdc_context.sdc_num_dephy as sdc_code_dephy, 
   	sdc_context.sdc_filiere,
   	sdc_context.sdc_valide,
   	sdc_context.sdc_type_conduite as sdc_type_agriculture,
  	es.valide as synthetise_valide, 
  	es.campagnes as synthetise_campagnes,
   	ec.nom as culture_nom,
  	ec.id as culture_id,
    ens.rang as culture_rang,
    ecoc.complet_espece_edi_nettoye as culture_especes_edi,
    ecoc.variete_nom,
    eisoc.precedent_nom as precedent_nom,
    eisoc.precedent_code as precedent_code,
    eppps.type as phase,
    eppps.id as phase_id,
    epps.pct_occupation_sol as pourcentage_sole_sdc,
    eis.nom,
    eis.id,
    eis.date_debut,
    eis.date_fin,
    eisoc.interventions_actions,
    eisoc.interventions_intrants,
    eisoc.interventions_cibles_trait,
    ec.code as culture_code,
    eisoc.precedent_id as precedent_id,
    eisoc.esp as espece_intervention,
    eisoc.var as varietes_intervention, 
    eisoc.rendement_total,
    eisoc.nb_intrants,
    eismae.synthetise_id as systeme_synthetise_id,
    eismae.plantation_perenne_synthetise_id as plantation_id,
    eismae.cible_noeuds_synthetise_id as noeuds_synthetise_id
from entrepot_intervention_synthetise_performance eisp
join  entrepot_intervention_synthetise_outils_can eisoc on eisoc.id = eisp.intervention_synthetise_id
join entrepot_intervention_synthetise eis on eisoc.id = eis.id
join entrepot_intervention_synthetise_agrege_extanded eismae on eismae.id = eisp.intervention_synthetise_id 
join entrepot_synthetise es on es.id = eismae.synthetise_id
join entrepot_context_performance_sdc sdc_context on eismae.sdc_id = sdc_context.sdc_id
left join entrepot_noeuds_synthetise ens on ens.id = eismae.cible_noeuds_synthetise_id
left join entrepot_plantation_perenne_phases_synthetise eppps on eppps.id = eismae.plantation_perenne_phases_synthetise_id
left join entrepot_plantation_perenne_synthetise epps on eismae.plantation_perenne_synthetise_id = epps.id
join entrepot_culture ec on ec.id = eismae.culture_id
join entrepot_culture_outils_can ecoc on ecoc.id = ec.id;