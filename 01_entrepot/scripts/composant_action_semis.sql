--------------------
-- SEMENCES
--------------------

-- Cette table pointe vers la table action
-- Elle correspond aux actions de types semis, pour lesquelles on peut saisir un détail par composant de culture de la profondeur.



create table entrepot_composant_action_semis(
	id character varying(255), 
	quantite float, 
	unite character varying(100),
	profondeur float,
	composant_culture_code character varying(500),
	action_id character varying(500),
	traitement_chimique boolean, --obsolète
	inoculation_biologique boolean	--obsolète
);


insert into entrepot_composant_action_semis(id, quantite, unite, profondeur, composant_culture_code, action_id, traitement_chimique, inoculation_biologique)
select 
	sas.topiaid as id, 
	sas.quantity as quantite,
	sas.seedplantunit as unite,
	sas.deepness as profondeur, 
	sas.speciescode as composant_culture_code, 
	sas.seedingaction as action_id,
	sas.treatment as traitement_chimique,
	sas.biologicalseedinoculation as inoculation_biologique
from seedingactionspecies sas;

alter table entrepot_composant_action_semis
add constraint composant_action_semis_PK
PRIMARY KEY (id);