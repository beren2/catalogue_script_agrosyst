select 
	ed.code as domaine_code, 
	ed.id as domaine_id,
	ed.nom as domaine_nom, 
	ed.campagne as domaine_campagne, 
	ec.code as culture_code, 
	ec.id as culture_id, 
	ec.nom as culture_nom, 
	CASE ec.type
      	WHEN 'MAIN' then 'PRINCIPALE'
      	WHEN 'CATCH' then 'DEROBEE'
      	WHEN 'INTERMEDIATE' then 'INTERMEDIAIRE' end culture_type,
	case ec.melange_especes
		when true then 'oui'
		when false then 'non' end culture_melange_especes,
	case ec.melange_varietes
		when true then 'oui'
		when false then 'non' end culture_melange_varietes,
	ecc.id as espece_id, 
	ecc.code as espece_code, 
	ecc.surface_relative,
	ee.code_espece_botanique,
	ee.code_qualifiant_aee as code_edi_qualifiant,
	ee.code_type_saisonnier_aee as code_edi_type_saisonnier,
	ee.code_destination_aee as code_edi_destination,
	ee.libelle_espece_botanique as espece_edi_nom_botanique,
	ee.libelle_qualifiant_aee as espece_edi_qualifiant,
	ee.libelle_type_saisonnier_aee as espece_edi_type_saisonnier,
	ee.libelle_destination_aee as espece_edi_destination,
	ev.nom
from entrepot_composant_culture ecc
inner join entrepot_culture ec on ecc.culture_id  = ec.id
left join entrepot_espece ee on ecc.espece_id = ee.id 
left join entrepot_variete ev on ecc.variete_id = ev.id
left join entrepot_domaine ed on ec.domaine_id = ed.id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;