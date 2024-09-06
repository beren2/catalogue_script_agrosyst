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
	CASE ep.hors_zonage WHEN true THEN 'oui' WHEN false THEN 'non' END parcelle_hors_zonage,
	ep.equip_commentaire as equipement_commentaire,
	CASE ep.drainage WHEN true THEN 'oui' WHEN false THEN 'non' END drainage,
	ep.drainage_annee_realisation,
	CASE ep.protection_antigel WHEN true THEN 'oui' WHEN false THEN 'non' END protection_antigel,
	ep.protection_antigel_type,
	CASE ep.protection_antigrele WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_grele,
	CASE ep.protection_antipluie WHEN true THEN 'oui' WHEN false THEN 'non' END protection_antipluie,
	CASE ep.protection_antiinsecte WHEN true THEN 'oui' WHEN false THEN 'non' END protection_anti_insectes,
	ep.equip_autre as autre_equipement
from entrepot_parcelle ep
left join entrepot_domaine ed on ep.domaine_id = ed.id
left join entrepot_sdc es on ep.sdc_id = es.id
left join entrepot_commune ec on ep.commune_id = ec.id
join entrepot_dispositif_filtres_outils_can edfoc on es.dispositif_id = edfoc.id;