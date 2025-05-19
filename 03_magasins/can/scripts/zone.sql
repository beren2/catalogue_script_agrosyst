select 
	ed.code as domaine_code,
	ed.id as domaine_id, 
	ed.nom as domaine_nom,
	ed.campagne as domaine_campagne, 
	ep.id as parcelle_id, 
	ez.id as zone_id, 
	ez.nom as zone_nom,
	ez.surface as zone_surface,
	ez.latitude,
	ez.longitude,
	ez."type" as zone_type
from entrepot_zone ez
left join entrepot_parcelle ep on ez.parcelle_id = ep.id
left join entrepot_sdc esdc on esdc.id = ep.sdc_id
left join entrepot_domaine ed on ep.domaine_id = ed.id
join entrepot_dispositif_filtres_outils_can edfoc on esdc.dispositif_id = edfoc.id;
