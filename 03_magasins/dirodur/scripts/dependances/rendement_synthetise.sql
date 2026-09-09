CREATE TEMPORARY TABLE IF NOT EXISTS entrepot_rendement_synthetise_dirodur  AS
select 
	'synthetise' as mode_saisie,
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
	ve.id as variete_id,
	ve.denomination as variete_libelle, 
	ec.id as culture_id,
	ec.nom as culture_nom,
	ec.melange_especes as culture_est_melange_especes, 
	ec.melange_varietes as culture_est_melange_varietes,
	ee.typodirodur_espece as typodirodur_espece,
	ee.typodirodur_espece_precise as typodirodur_espece_precise,
	ee.typodirodur_espece_famille_bota as typodirodur_espece_famille_bota,
	ee.typodirodur_espece_periode_semis as typodirodur_espece_periode_semis,
	etcod.typodirodur_culture as typodirodur_culture,
	errp.action_id,
	eas.type as action_type,
	eis.date_debut as intervention_date_debut,
	eis.date_fin as intervention_date_fin,
	eis.type as intervention_type,
	easa.intervention_synthetise_id as intervention_id,
	easa.cible_noeuds_synthetise_id as noeud_id,
	easa.connection_synthetise_id as connexion_id,
	ersfod.destination_have_match_in_ref_dirodur as destination_est_conforme,
	not ersfod.unite_problematic as unite_est_conforme,
	not ersfod.espece_is_na as espece_est_conforme,
	null as zone_id,
	null as parcelle_id,
	easa.sdc_id as sdc_id,
	easa.domaine_id as domaine_id,
	ecom.id as domaine_position_commune_id,
    ecom.codeinsee as domaine_position_code_insee,
	ecom.commune as domaine_position_nom_commune,
	ecom.departement as domaine_position_departement,
	CASE ecom.region
		WHEN 11 THEN '11_Île-de-France'
		WHEN 24 THEN '24_Centre-Val de Loire'
		WHEN 27 THEN '27_Bourgogne-Franche-Comté'
		WHEN 28 THEN '28_Normandie'
		WHEN 32 THEN '32_Hauts-de-France'
		WHEN 44 THEN '44_Grand Est'
		WHEN 52 THEN '52_Pays de la Loire'
		WHEN 53 THEN '53_Bretagne'
		WHEN 75 THEN '75_Nouvelle-Aquitaine'
		WHEN 76 THEN '76_Occitanie'
		WHEN 84 THEN '84_Auvergne-Rhône-Alpes'
		WHEN 93 THEN '93_Provence-Alpes-Côte d''Azur'
		WHEN 94 THEN '94_Corse'
		WHEN 1  THEN '01_Guadeloupe'
		WHEN 2  THEN '02_Martinique'
		WHEN 3  THEN '03_Guyane'
		WHEN 4  THEN '04_La Réunion'
		WHEN 6  THEN '06_Mayotte'
		ELSE 'Inconnu'
	END AS domaine_position_region,
	ecom.ancienne_region as domaine_position_ancienne_region
from entrepot_recolte_rendement_prix errp
join entrepot_action_synthetise eas on errp.action_id = eas.id
left join entrepot_recolte_rendement_prix_restructure errpr on errp.id = errpr.id
left join entrepot_composant_culture ecc on errpr.composant_culture_id = ecc.id
left join entrepot_espece ee on ecc.espece_id = ee.id
left join entrepot_variete ve on ecc.variete_id = ve.id
left join entrepot_culture ec on ecc.culture_id = ec.id
left join entrepot_typologie_can_culture etcc on etcc.culture_id = ec.id
left join entrepot_action_synthetise_agrege easa on eas.id = easa.id
left join entrepot_domaine edom on easa.domaine_id = edom.id
left join entrepot_commune ecom on edom.commune_id = ecom.id
left join entrepot_intervention_synthetise eis on eis.id = eas.intervention_synthetise_id 
left join entrepot_rendement_synthetise_filtre_outils_dirodur ersfod on errp.id = ersfod.id
left join entrepot_synthetise_filtre_outils_dirodur esfod on easa.synthetise_id = esfod.synthetise_id
left join entrepot_typologie_culture_outils_dirodur etcod on etcod.culture_id = ec.id
where esfod.in_dirodur is true;