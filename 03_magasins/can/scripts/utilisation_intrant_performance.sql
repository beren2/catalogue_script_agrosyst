create temporary table utilisation_intrant_performance_test as
-- SYNTHETISE 
select 
	euip.*,
	sdc_context.domaine_nom as nom_domaine_exploitation,
	sdc_context.domaine_id as id_domaine, 
	sdc_context.domaine_campagne,
	sdc_context.domaine_type,
	sdc_context.domaine_departement as departement, 
	sdc_context.nom_reseau_it,
	sdc_context.nom_reseau_ir,
	sdc_context.dispositif_id,
	sdc_context.dispositif_type,
	sdc_context.sdc_id,
	sdc_context.sdc_filiere, 
	sdc_context.sdc_nom,
	sdc_context.sdc_num_dephy,
	sdc_context.sdc_type_conduite, 
	sdc_context.sdc_valide, 
	sdc_context.sdc_modalite_suivi_dephy, 
	es.nom as nom_systeme_synthetise,
	es.id as id_systeme_synthetise,
	es.valide as synthetise_valide,
	es.campagnes as synthetise_campagnes,
	null as parcelle_id,
	null as parcelle,
	null as zone_id,
	null as zone,
	ec.nom as culture, 
	ec.id as culture_id, 
	ec.code as culture_code,
	ecoc.complet_espece_edi_nettoye as especes,
	eisoc.precedent_nom as culture_precedente, 
	eisoc.precedent_id as culture_precedente_id, 
	eisoc.precedent_code as culture_precedente_code,
	eppps.id as phase_id,
	eppps."type" as phase,
	epps.pct_occupation_sol,
	ens.rang as rang,
	eisoc.interventions_actions as action,
	ei.nom_utilisateur as intrant_nom,
	eis.nom as intervention,
	eis.id as intervention_id,
	cast(eis.date_debut as text) as debut_intervention,
	cast(eis.date_fin as text) as fin_intervention,
	eisoc.interventions_cibles_trait as cibles_traitement
from entrepot_utilisation_intrant_performance euip 
join entrepot_utilisation_intrant_synthetise euis on euis.id = euip.utilisation_intrant_id 
join entrepot_utilisation_intrant_synthetise_agrege euisa on euis.id = euisa.id
join entrepot_intervention_synthetise_outils_can eisoc on euisa.intervention_synthetise_id = eisoc.id
join entrepot_intervention_synthetise_agrege_extanded eismae on eismae.id = euisa.intervention_synthetise_id 
join entrepot_intervention_synthetise eis on eis.id = euisa.intervention_synthetise_id 
join entrepot_synthetise es on euisa.synthetise_id = es.id
join entrepot_context_performance_sdc sdc_context on euisa.sdc_id = sdc_context.sdc_id
join entrepot_culture ec on ec.id = eismae.culture_id
join entrepot_culture_outils_can ecoc on ecoc.id = ec.id
left join entrepot_intrant ei on euis.intrant_id = ei.id
left join entrepot_noeuds_synthetise ens on ens.id = eismae.cible_noeuds_synthetise_id
left join entrepot_plantation_perenne_phases_synthetise eppps on eppps.id = eismae.plantation_perenne_phases_synthetise_id
left join entrepot_plantation_perenne_synthetise epps on eismae.plantation_perenne_synthetise_id = epps.id
UNION
-- REALISE 
select 
	euip.*,
	sdc_context.domaine_nom as nom_domaine_exploitation,
	sdc_context.domaine_id as id_domaine, 
	sdc_context.domaine_campagne,
	sdc_context.domaine_type,
	sdc_context.domaine_departement as departement, 
	sdc_context.nom_reseau_it,
	sdc_context.nom_reseau_ir,
	sdc_context.dispositif_id,
	sdc_context.dispositif_type,
	sdc_context.sdc_id,
	sdc_context.sdc_filiere, 
	sdc_context.sdc_nom,
	sdc_context.sdc_num_dephy,
	sdc_context.sdc_type_conduite, 
	sdc_context.sdc_valide, 
	sdc_context.sdc_modalite_suivi_dephy, 
	null as nom_systeme_synthetise,
	null as id_systeme_synthetise,
	null as synthetise_valide,
	null as synthetise_campagnes,
	ep.id as parcelle_id,
	ep.nom as parcelle,
	ez.id as zone_id,
	ez.nom as zone,
	ec.nom as culture, 
	ec.id as culture_id, 
	ec.code as culture_code,
	ecoc.complet_espece_edi_nettoye as especes,
	eiroc.precedent_nom as culture_precedente, 
	eiroc.precedent_id as culture_precedente_id, 
	null as culture_precedente_code,
	epppr.id as phase_id,
	epppr."type" as phase,
	null as pct_occupation_sol,
	enr.rang as rang,
	eiroc.interventions_actions as action,
	ei.nom_utilisateur as intrant_nom,
	eir.nom as intervention,
	eir.id as intervention_id,
	cast(eir.date_debut as text) as debut_intervention,
	cast(eir.date_fin as text) as fin_intervention,
	eiroc.interventions_cibles_trait as cibles_traitement
from entrepot_utilisation_intrant_performance euip 
join entrepot_utilisation_intrant_realise euir on euir.id = euip.utilisation_intrant_id 
join entrepot_utilisation_intrant_realise_agrege euira on euir.id = euira.id
join entrepot_intervention_realise_outils_can eiroc on euira.intervention_realise_id = eiroc.id
join entrepot_intervention_realise eir on eir.id = euira.intervention_realise_id 
join entrepot_context_performance_sdc sdc_context on euira.sdc_id = sdc_context.sdc_id
join entrepot_culture ec on ec.id = euira.culture_id
join entrepot_culture_outils_can ecoc on ecoc.id = ec.id
left join entrepot_parcelle ep on euira.parcelle_id = ep.id
left join entrepot_zone ez on euira.zone_id = ez.id
left join entrepot_intrant ei on euir.intrant_id = ei.id
left join entrepot_noeuds_realise enr on enr.id = euira.noeuds_realise_id
left join entrepot_plantation_perenne_phases_realise epppr on epppr.id = euira.plantation_perenne_phases_realise_id
left join entrepot_plantation_perenne_realise eppr on euira.plantation_perenne_realise_id = eppr.id;