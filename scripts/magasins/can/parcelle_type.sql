select 
	edo.id as domaine_id, 
	edo.code as domaine_code, 
	edo.nom as domaine_nom,
	edo.campagne as domaine_campagne,
	esdc.id as sdc_id,
	es.id as systeme_syntehtise_id, 
	es.nom as systeme_synthetise_nom, 
	es.campagnes as systeme_synthetise_campagnes,
	ept.id as parcelle_type_id, 
	ept.nom as parcelle_type_nom,
	ept.surface as parcelle_type_surface,
	ept.commentaire as parcelle_type_commentaire,
	ept.hors_zonage as parcelle_type_hors_zonage,
	ept.equipement_commentaire as esquipement_commentaire,
	ept.drainage as drainage,
	ept.drainage_annee_realisation as drainage_annee_realisation,
	ept.protection_antigel as protection_anti_gel,
	ept.protection_antigel_type as protection_anti_gel_type,
	ept.protection_antipluie as protection_anti_pluie,
	ept.protection_antiinsecte as protection_anti_insectes,
	ept.equipement_autre as autre_equipement,
	ept.commentaire_sol as sol_commentaire,
	ept.texture_surface as texture_surface,
	ept.texture_sous_sol, 
	ept.ph as sol_ph,
	ept.pierrosite_moyenne,
	ept.sol_profondeur_max_enracinement as sol_profondeur_max,
	ept.teneur_MO_pct as teneur_mo,
	ept.hydromorphie as hydromorphie, 
	ept.calcaire as calcaire,
	ept.proportion_calcaire_total,
	ept.battance as battance,
	ept.systeme_irrigation as irrigation,
	ept.systeme_fertirrigation as fertirrigation,
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
-- attention, il manque calcaire actif ET profondeur.