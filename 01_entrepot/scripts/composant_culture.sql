
CREATE TABLE entrepot_composant_culture AS
SELECT 
	cps.topiaid AS id,
	cps.code AS code,
	cps.species AS espece_id,
	cps.speciesarea AS surface_relative, -- si non saisie alors on suppose que c'est équiréparti dans la culture (100 / nb d'espèces ou variété dans la culture)
	cps.variety AS variete_id,
	cps.croppingplanentry AS culture_id
FROM croppingplanspecies cps;

alter table entrepot_composant_culture
add constraint composant_culture_PK
PRIMARY KEY (id);
