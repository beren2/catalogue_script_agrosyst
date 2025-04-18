select 
	ed.code as domaine_code, 
	ed.id as domaine_id,
	ed.nom as domaine_nom,
	ed.campagne as domaine_campagne, 
	esdc.id as sdc_id,
	esdc.code as sdc_code,
	esdc.nom as sdc_nom,
	esy.id as systeme_synthetise_id,
	esy.nom as systeme_synthetise_nom,
	esy.campagnes as systeme_synthetise_campagnes,
	euir.id as usage_id,
	eir.id as intervention_id,
	ei.id as intrant_id,
	ei."type" as intrant_type,
	COALESCE(ei.ref_id, es.id) as intrant_ref_id,
	COALESCE(ei.ref_nom , efm.type_produit, efo.libelle, ee.libelle_espece_botanique, eatp.nom_produit) as intrant_ref_nom,
	ei.nom_utilisateur as intrant_nom_utilisateur,
	euir.dose,
	euir.profondeur_semis_cm,
	euir.volume_bouillie_hl,
	euir.unite,
	CASE CAST(ei.biocontrole AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END biocontrole,
	ei.type_produit as intrant_phyto_type,
	euir.intrant_phyto_cible_nom,
	ei.forme_fert_min as forme_ferti_min,
	ei.n, 
	ei.p2o5,
	ei.k2o,
	ei.bore,
	ei.calcium,
	ei.fer,
	ei.manganese,
	ei.molybdene,
	ei.mgo,
	ei.oxyde_de_sodium,
	ei.so3,
	ei.cuivre,
	ei.zinc,
	ei.unite_teneur_fert as unite_teneur_ferti_orga,
	--attention ferti_effet_phyto_attendu --> kesako ?
	COALESCE(ei.prix_saisi, es.prix_saisi) as prix,
	COALESCE(ei.prix_saisi_unite, es.prix_saisi_unite) as prix_unite,
	ei.cao,
	ei.s
from entrepot_utilisation_intrant_synthetise euir
left join entrepot_utilisation_intrant_synthetise_agrege euira on euir.id = euira.id
left join entrepot_domaine ed on ed.id = euira.domaine_id
left join entrepot_sdc esdc on esdc.id = euira.sdc_id
left join entrepot_synthetise esy on esy.id = euira.synthetise_id
left join entrepot_intervention_synthetise eir on eir.id = euir.intervention_synthetise_id
left join entrepot_intrant ei on euir.intrant_id = ei.id
left join entrepot_fertilisation_minerale efm on ei.ref_id = efm.id
left join entrepot_fertilisation_organique efo on ei.ref_id = efo.id
left join entrepot_acta_traitement_produit eatp on ei.ref_id = eatp.id
left join entrepot_semence es on es.id = euir.semence_id
left join entrepot_composant_culture ecc on ecc.id = es.composant_culture_id
left join entrepot_espece ee on ecc.espece_id = ee.id
join entrepot_dispositif_filtres_outils_can edfoc on esdc.dispositif_id = edfoc.id;