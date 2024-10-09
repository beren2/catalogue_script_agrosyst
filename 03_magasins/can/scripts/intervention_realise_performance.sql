SELECT
    eirp.*,
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
   	sdc_context.sdc_nom,
   	sdc_context.sdc_id,
   	eirma.parcelle_id,
   	ez.nom as zone_nom,
   	eirma.zone_id,
   	sdc_context.sdc_num_dephy as sdc_code_dephy, 
   	sdc_context.sdc_valide,
   	sdc_context.sdc_type_conduite as sdc_type_agriculture,
   	ec.nom as culture_nom,
   	ec.id as culture_id, 
   	ens.rang as culture_rang,
    ecoc.complet_espece_edi_nettoye as culture_especes_edi,
    ecoc.variete_nom,
    eiroc.precedent_nom as precedent_nom,
    eiroc.precedent_id as precedent_code,
    epppr.type as phase,
    epppr.id as phase_id,
    eis.nom,
    eis.id,
    eis.date_debut,
    eis.date_fin,
    eiroc.interventions_actions,
    eiroc.interventions_intrants,
    eiroc.interventions_cibles_trait,
    eiroc.precedent_id as precedent_id,
    ez.surface as zonearea,
    eiroc.esp as especes_intervention,
    eiroc.var as varietes_intervention, 
    eiroc.rendement_total,
    eiroc.nb_intrants,
    eirma.plantation_perenne_realise_id as plantation_id
from entrepot_intervention_realise_performance eirp
join  entrepot_intervention_realise_outils_can eiroc on eiroc.id = eirp.intervention_realise_id
join entrepot_intervention_realise eis on eiroc.id = eis.id
join entrepot_intervention_realise_agrege eirma on eirma.id = eirp.intervention_realise_id 
join entrepot_zone ez on ez.id = eirma.zone_id
join entrepot_context_performance_sdc sdc_context on eirma.sdc_id = sdc_context.sdc_id
left join entrepot_noeuds_realise ens on ens.id = eirma.noeuds_realise_id
join entrepot_culture ec on ec.id = eirma.culture_id -- on utilise l'information dans le df agrégé pour avoir le cas à la fois des perennes et des assolées
join entrepot_culture_outils_can ecoc on ec.id = ecoc.id
left join entrepot_plantation_perenne_phases_realise epppr on epppr.id = eirma.plantation_perenne_phases_realise_id
left join entrepot_plantation_perenne_realise epps on eirma.plantation_perenne_realise_id = epps.id;