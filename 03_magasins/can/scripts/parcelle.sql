-- TODO : ajouter la colonne "zonage_parcelle" une fois que le référentiel sera accessible (grace au lien avec entrepot_parcelle_zonage)
-- 
select 
	ed.code as domaine_code, 
	ed.id as domaine_id, 
	ed.nom as domaine_nom,
	ed.campagne as domaine_campagne,
	es.id as sdc_id,
	ep.code as parcelle_code,
	ep.id as parcelle_id,
	ep.nom as parcelle_nom,
	ep.surface as parcelle_surface,
	ec.codepostal as code_postal, 
	ec.commune as commune,
	ep.commentaire as parcelle_commentaire,
	ep.nombre_de_zones,
	epz.libelle_zonage as zonages_parcelle,
	ep.commentaire_sol as sol_commentaire,
	ep.texture_surface as texture_surface,
	ep.texture_sous_sol as texture_sous_sol,
	ep.sol_ph,
	ep.sol_pierrosite_moyenne as pierrosite_moyenne,
	ep.sol_profondeur_max_enracinement_classe as sol_profondeur,
	ep.sol_profondeur_max_enracinement as sol_profondeur_max,
	ep.teneur_mo_pct as teneur_mo,
	ep.hydromorphie,
	ep.calcaire, 
	ep.proportion_calcaire_total,
	ep.proportion_calcaire_actif,
	ep.battance,
	ep.systeme_irrigation as irrigation, 
	ep.systeme_fertirrigation as fertirrigation,
	ep.eau_origine as origine_eau,
	ep.systeme_irrigation_type as irrigation_type,
	ep.pompe_type as irrigation_pompe,
	ep.positionnement_tuyaux_arrosage as irrigation_position_tuyaux,
	ep.pente,
	ep.distance_cours_eau,
	ep.bande_enherbee as bande_enherbe,
	ep.sol_nom_ref,
	CASE CAST(ep.dans_zonage AS BOOLEAN) WHEN true THEN 'non' WHEN false THEN 'oui' END parcelle_hors_zonage,
	ep.equip_commentaire as equipement_commentaire,
	CASE CAST(ep.drainage AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END drainage,
	ep.drainage_annee_realisation,
	CASE CAST(ep.protection_antigel AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END protection_antigel,
	ep.protection_antigel_type,
	CASE CAST(ep.protection_antigrele AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END protection_antigrele,
	CASE CAST(ep.protection_antipluie AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END protection_antipluie,
	CASE CAST(ep.protection_antiinsecte AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END protection_antiinsectes,
	ep.equip_autre as autre_equipement
from entrepot_parcelle ep
left join entrepot_domaine ed on ep.domaine_id = ed.id
left join entrepot_sdc es on ep.sdc_id = es.id
left join entrepot_commune ec on ep.commune_id = ec.id
left join entrepot_parcelle_zonage epz on epz.parcelle_id = ep.id
join entrepot_dispositif_filtres_outils_can edfoc on es.dispositif_id = edfoc.id;


--sol_nom_ref (Sol limono-argileux profond sur argiles)
