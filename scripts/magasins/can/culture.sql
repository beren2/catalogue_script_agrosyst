SELECT 
  d.code as domaine_code,
  d.id as domaine_id, 
  d.nom as domaine_nom,
  d.campagne as domaine_campagne,
  c.code as culture_code,
  c.id as culture_id,
  c.nom as culture_nom,
  c.type as culture_type, 
  c.melange_especes as culture_melange_especes,
  c.melange_varietes as culture_melange_varietes,
  cc.id as espece_id,
  cc.code as espece_code, 
  cc.surface_relative,
  e.code_espece_botanique as code_edi_espece_botanique,
  e.code_qualifiant_aee as code_edi_qualifiant,
  e.code_type_saisonnier_aee as code_edi_type_saisonnier, 
  e.code_destination_aee as code_edi_destination, 
  e.libelle_espece_botanique as espece_edi_nom_botanique, 
  e.libelle_qualifiant_aee as espece_edi_qualifiant, 
  e.libelle_type_saisonnier_aee as espece_edi_type_saisonnier,
  e.libelle_destination_aee as espece_edi_destination, 
  v.nom_botanique as variete_nom
from entrepot_composant_culture cc
left join entrepot_variete v on cc.variete_id = v.id
left join entrepot_espece e on cc.espece_id = e.id
left join entrepot_culture c on cc.culture_id = c.id
left join entrepot_domaine d on c.domaine_id = d.id;