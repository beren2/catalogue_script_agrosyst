
CREATE TEMPORARY TABLE IF NOT EXISTS entrepot_rendement_realise_dirodur  AS
select 
	'realise' as mode_saisie,
	errp.id as recolte_id,
	errp.rendement_moy as recolte_rendement,
	errp.rendement_unite as recolte_unite,
	errp.destination_id as recolte_destination_id,
	errp.destination as recolte_destination,
	errpr.composant_culture_id as composant_culture_id,
	ee.id as espece_id,
	ee.code_espece_botanique as espece_code_botanique,
	ee.libelle_espece_botanique as espece_libelle_botanique,
	ee.code_qualifiant_aee as espece_code_qualifiant_aee, 
	ee.libelle_qualifiant_aee as espece_libelle_qualifiant_aee,
	ee.code_type_saisonnier_aee as espece_code_type_saisonnier_aee,
	ee.libelle_type_saisonnier_aee as espece_libelle_type_saisonnier_aee,
	ee.code_destination_aee as espece_code_destination_aee,
	ee.libelle_destination_aee as espece_libelle_destination_aee,
	ee.typodirodur_espece as typodirodur_espece,
	ee.typodirodur_espece_precise as typodirodur_espece_precise,
	ee.typodirodur_espece_famille_bota as typodirodur_espece_famille_bota,
	ee.typodirodur_espece_periode_semis as typodirodur_espece_periode_semis,
	etcod.typodirodur_culture as typodirodur_culture,
	ve.id as variete_id,
	ve.denomination as variete_libelle, 
	ec.id as culture_id,
	ec.nom as culture_nom,
	ec.melange_especes as culture_est_melange_especes, 
	ec.melange_varietes as culture_est_melange_varietes,
	etcc.nb_composant_culture as culture_typo_can_nbre_composant,
	errp.action_id,
	ear.type as action_type,
	cast(eir.date_debut as text) as intervention_date_debut,
	cast(eir.date_fin as text) as intervention_date_fin,
	eir.type as intervention_type,
	eara.intervention_realise_id as intervention_id,
	eara.noeuds_realise_id as noeud_id,
	null as connexion_id,
	errfod.destination_have_match_in_ref_dirodur as destination_est_conforme,
	not errfod.unite_problematic as unite_est_conforme,
	not errfod.espece_is_na as espece_est_conforme
from entrepot_recolte_rendement_prix errp
join entrepot_action_realise ear on errp.action_id = ear.id
left join entrepot_recolte_rendement_prix_restructure errpr on errp.id = errpr.id
left join entrepot_composant_culture ecc on errpr.composant_culture_id = ecc.id
left join entrepot_espece ee on ecc.espece_id = ee.id
left join entrepot_variete ve on ecc.variete_id = ve.id
left join entrepot_culture ec on ecc.culture_id = ec.id
left join entrepot_typologie_can_culture etcc on etcc.culture_id = ec.id
left join entrepot_action_realise_agrege eara on ear.id = eara.id
left join entrepot_intervention_realise eir on eir.id = ear.intervention_realise_id
left join entrepot_rendement_realise_filtre_outils_dirodur errfod on errp.id = errfod.id
left join entrepot_sdc_realise_filtre_outils_dirodur esrfod on eara.sdc_id = esrfod.sdc_id
left join entrepot_typologie_culture_outils_dirodur etcod on etcod.culture_id = ec.id
where esrfod.in_dirodur is true;