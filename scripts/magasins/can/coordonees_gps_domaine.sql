select 
	ecgd.domaine_id,
	ecgd.nom_coordonnees_centre_operationnel as coordonnees_nom_centre_operationnel,
	ecgd.coordonnees_description_centre_operationnel,
	ecgd.longitude,
	ecgd.latitude
from entrepot_coordonees_gps_domaine ecgd
join domaine_filtre df on df.domaine_id = ecgd.domaine_id