select 
	edo.id as domaine_id, 
	edo.code as domaine_code, 
	edo.nom as domaine_nom,
	edo.campagne as domaine_campagne,
	esdc.id as sdc_id,
	es.id as systeme_synthetise_id, 
	es.nom as systeme_synthetise_nom, 
	es.campagnes as systeme_synthetise_campagnes,
	ept.id as parcelle_type_id, 
	ept.nom as parcelle_type_nom,
	ept.surface as parcelle_type_surface,
	ept.commentaire as parcelle_type_commentaire,
	CASE ept.hors_zonage WHEN true THEN 'oui' WHEN false THEN 'non' END parcelle_type_hors_zonage,
	ept.equipement_commentaire as equipement_commentaire,
	CASE ept.drainage WHEN true THEN 'oui' WHEN false THEN 'non' END drainage,
	ept.drainage_annee_realisation as drainage_annee_realisation,
	CASE ept.protection_antigel WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_gel,
	ept.protection_antigel_type as protection_anti_gel_type,
	CASE ept.protection_antipluie WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_pluie,
	CASE ept.protection_antiinsecte WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_insectes,
	ept.equipement_autre as autre_equipement,
	ept.commentaire_sol as sol_commentaire,
	ets_surface.id as texture_surface, --attention, on ne veut pas un référentiel !
	ets_profondeur.id as texture_sous_sol, 					--attention, on ne veut pas un référentiel ! 
	ept.ph as sol_ph,
	ept.pierrosite_moyenne,
	ept.sol_profondeur_max_enracinement as sol_profondeur_max,
	ept.teneur_MO_pct as teneur_mo,
	CASE ept.hydromorphie WHEN true THEN 'oui' WHEN false THEN 'non' END hydromorphie,
	CASE ept.calcaire WHEN true THEN 'oui' WHEN false THEN 'non' END calcaire,
	ept.proportion_calcaire_total,
	CASE ept.battance WHEN true THEN 'oui' WHEN false THEN 'non' END battance,
	CASE ept.systeme_irrigation WHEN true THEN 'oui' WHEN false THEN 'non' END irrigation,
	CASE ept.systeme_fertirrigation WHEN true THEN 'oui' WHEN false THEN 'non' END fertirrigation,
	ept.eau_origine as origine_eau,
	ept.systeme_irrigation_type as irrigation_type,
	ept.pompe_type as irrigation_pompe,
	ept.positionnement_tuyaux_arrosage as irrigation_position_tuyaux,
	ept.pente_max as pente,
	ept.distance_cours_eau,
	ept.bande_enherbe
from entrepot_synthetise es
join entrepot_parcelle_type ept on es.parcelle_type_id = ept.id
left join entrepot_sdc esdc on es.sdc_id = esdc.id 
left join entrepot_dispositif ed on ed.id = esdc.dispositif_id
left join entrepot_domaine edo on edo.id = ed.domaine_id
left join entrepot_texture_sol ets_surface on ets_surface.classe_indigo = ept.texture_surface
left join entrepot_texture_sol ets_profondeur on ets_profondeur.classe_indigo = ept.texture_sous_sol 
join entrepot_dispositif_filtres_outils_can edifoc on ed.id = edifoc.id;