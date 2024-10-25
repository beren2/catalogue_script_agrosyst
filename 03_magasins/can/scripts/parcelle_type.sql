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
	CASE CAST(ept.hors_zonage AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END parcelle_type_hors_zonage,
	ept.equipement_commentaire as equipement_commentaire,
	CASE CAST(ept.drainage AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END drainage,
	ept.drainage_annee_realisation as drainage_annee_realisation,
	CASE CAST(ept.protection_antigel AS BOOLEAN)  WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_gel,
	ept.protection_antigel_type as protection_anti_gel_type,
	CASE CAST(ept.protection_antipluie AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_pluie,
	CASE CAST(ept.protection_antiinsecte AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_insectes,
	ept.equipement_autre as autre_equipement,
	ept.commentaire_sol as sol_commentaire,
	ept.texture_surface_id as texture_surface, --attention, on ne veut pas un référentiel !
	ept.texture_sous_sol_id as texture_sous_sol, 					--attention, on ne veut pas un référentiel ! 
	ept.ph as sol_ph,
	ept.pierrosite_moyenne,
	ept.sol_profondeur_max_enracinement as sol_profondeur_max,
	ept.teneur_MO_pct as teneur_mo,
	CASE CAST(ept.hydromorphie AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END hydromorphie,
	CASE CAST(ept.calcaire AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END calcaire,
	ept.proportion_calcaire_total,
	CASE CAST(ept.battance AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END battance,
	CASE CAST(ept.systeme_irrigation AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END irrigation,
	CASE CAST(ept.systeme_fertirrigation AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END fertirrigation,
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
join entrepot_dispositif_filtres_outils_can edifoc on ed.id = edifoc.id;