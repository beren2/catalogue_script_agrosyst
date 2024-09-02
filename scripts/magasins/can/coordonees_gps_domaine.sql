select 
	ecgd.domaine_id,
	ecgd.nom_coordonnees_centre_operationnel as coordonnees_nom_centre_operationnel,
	ecgd.coordonnees_description_centre_operationnel,
	ecgd.longitude,
	ecgd.latitude
from entrepot_coordonees_gps_domaine ecgd
join entrepot_domaine_filtres_outils_can edifoc on ecgd.domaine_id = edifoc.id;