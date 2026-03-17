-- En réalisé
select 
	'realise' as mode_saisie,
	errp.id as recolte_id,
	errp.rendement_moy as recolte_rendement,
	errp.rendement_unite as recolte_unite,
	errpr.composant_culture_id as composant_culture_id,
	ee.id as espece_id,
	ee.code_espece_botanique as espece_code_botanique,
	ee.libelle_espece_botanique as espece_libelle_botanique,
	ee.code_qualifiant_aee as espece_code_qualifiant_aee, 
	ee.libelle_qualifiant_aee as espece_libelle_qualifiant_aee,
	ee.code_type_saisonnier_aee as espece_code_type_saisonnier_aee,
	ee.code_destination_aee as espece_code_destination_aee,
	ee.libelle_destination_aee as espece_libelle_destination_aee,
	ee.typocan_espece as espece_typo_can,
	ve.id as variete_id,
	ve.denomination as variete_libelle, 
	ec.id as culture_id,
	ec.nom as culture_nom,
	ec.melange_especes as culture_est_melange_espece, 
	ec.melange_varietes as culture_est_melange_variete,
	etcc.typocan_culture_sans_compagne as culture_typo_can_sans_compagne,
	etcc.typocan_espece as culture_typo_can_espece,
	etcc.typocan_esp_sans_compagne as culture_typo_can_espece_sans_compagne,
	etcc.nb_composant_culture as culture_typo_can_nbre_composant,
	etcc.nb_typocan_esp as culture_typo_can_nbre_espece,
	errp.action_id,
	ear.type as action_type,
	cast(eir.date_debut as text) as intervention_date_debut,
	cast(eir.date_fin as text) as intervention_date_fin,
	eir.type as intervention_type,
	eara.intervention_realise_id,
	eara.noeuds_realise_id as noeud_id,
	null as connexion_id
from entrepot_recolte_rendement_prix errp
left join entrepot_recolte_rendement_prix_restructure errpr on errp.id = errpr.id
left join entrepot_composant_culture ecc on errpr.composant_culture_id = ecc.id
left join entrepot_espece ee on ecc.espece_id = ee.id
left join entrepot_variete ve on ecc.variete_id = ve.id
left join entrepot_culture ec on ecc.culture_id = ec.id
left join entrepot_typologie_can_culture etcc on etcc.culture_id = ec.id
join entrepot_action_realise ear on errp.action_id = ear.id
left join entrepot_action_realise_agrege eara on ear.id = eara.id
left join entrepot_intervention_realise eir on eir.id = ear.intervention_realise_id
left join entrepot_rendement_realise_filtre_outils_dirodur errfod on errp.id = errfod.id
-- conditions de présence dans le magasin
where errfod.destination_have_match_in_ref_dirodur = true
and errfod.unite_problematic = false
and errfod.espece_is_na = false
union
select 
	'synthetise' as mode_saisie,
	errp.id as recolte_id,
	errp.rendement_moy as recolte_rendement,
	errp.rendement_unite as recolte_unite,
	errpr.composant_culture_id as composant_culture_id,
	ee.id as espece_id,
	ee.code_espece_botanique as espece_code_botanique,
	ee.libelle_espece_botanique as espece_libelle_botanique,
	ee.code_qualifiant_aee as espece_code_qualifiant_aee, 
	ee.libelle_qualifiant_aee as espece_libelle_qualifiant_aee,
	ee.code_type_saisonnier_aee as espece_code_type_saisonnier_aee,
	ee.code_destination_aee as espece_code_destination_aee,
	ee.libelle_destination_aee as espece_libelle_destination_aee,
	ee.typocan_espece as espece_typo_can,
	ve.id as variete_id,
	ve.denomination as variete_libelle, 
	ec.id as culture_id,
	ec.nom as culture_nom,
	ec.melange_especes as culture_est_melange_espece, 
	ec.melange_varietes as culture_est_melange_variete,
	etcc.typocan_culture_sans_compagne as culture_typo_can_sans_compagne,
	etcc.typocan_espece as culture_typo_can_espece,
	etcc.typocan_esp_sans_compagne as culture_typo_can_espece_sans_compagne,
	etcc.nb_composant_culture as culture_typo_can_nbre_composant,
	etcc.nb_typocan_esp as culture_typo_can_nbre_espece,
	errp.action_id,
	eas.type as action_type,
	eis.date_debut as intervention_date_debut,
	eis.date_fin as intervention_date_fin,
	eis.type as intervention_type,
	easa.intervention_synthetise_id,
	easa.cible_noeuds_synthetise_id as noeud_id,
	easa.connection_synthetise_id as connexion_id
	from entrepot_recolte_rendement_prix errp
left join entrepot_recolte_rendement_prix_restructure errpr on errp.id = errpr.id
left join entrepot_composant_culture ecc on errpr.composant_culture_id = ecc.id
left join entrepot_espece ee on ecc.espece_id = ee.id
left join entrepot_variete ve on ecc.variete_id = ve.id
left join entrepot_culture ec on ecc.culture_id = ec.id
left join entrepot_typologie_can_culture etcc on etcc.culture_id = ec.id
join entrepot_action_synthetise eas on errp.action_id = eas.id
left join entrepot_action_synthetise_agrege easa on eas.id = easa.id
left join entrepot_intervention_synthetise eis on eis.id = eas.intervention_synthetise_id 
left join entrepot_rendement_synthetise_filtre_outils_dirodur ersfod on errp.id = ersfod.id
-- conditions de présence dans le magasin
where ersfod.destination_have_match_in_ref_dirodur = true
and ersfod.unite_problematic = false
and ersfod.espece_is_na = false;