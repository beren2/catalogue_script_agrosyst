select 
	d.code as domaine_code, 
	d.id as domaine_id, 
	d.nom as domaine_nom, 
	d.campagne as domaine_campagne, 
	ed.id as dispositif_id, 
	ed.code as dispositif_code,
	ed.nom as dispositif_nom, 
	ed.type as dispositif_type
from entrepot_dispositif ed
join entrepot_domaine d on d.id = ed.domaine_id
join dispositif_filtre df on ed.id = df.dispositif_id;