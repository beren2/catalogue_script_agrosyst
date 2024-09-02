select 
	ed.code as domaine_code, 
	ed.id as domaine_id,
	ed.nom as domaine_nom,
	ed.campagne as domaine_campagne, 
	esdc.id as sdc_id,
	esdc.code as sdc_code,
	esdc.nom as sdc_nom,
	ep.id as parcelle_id,
	ep.nom as parcelle_nom,
	ez.id as zone_id,
	ez.nom as zone_nom,
	euir.id as utilisation_intrant_id,
	eir.id as intervention_id,
	ei.id as intrant_id,
	ei."type" as intrant_type,
	ei.ref_id as intrant_ref_id,
	ei.ref_nom as intrant_ref_nom,
	ei.nom_utilisateur as intrant_nom_utilisateur,
	euir.dose,
	euir.profondeur_semis_cm,
	euir.volume_bouillie_hl,
	euir.unite,
	ei.biocontrole,
	ei.type_produit as intrant_phyto_type,
	euir.intrant_phyto_cible_nom,
	ei.forme_fert_min,
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
	ei.prix_ref as prix,
	ei.prix_ref_unite as prix_unite,
	ei.cao,
	ei.s
from entrepot_utilisation_intrant_realise euir
left join entrepot_utilisation_intrant_realise_agrege euira on euir.id = euira.id
left join entrepot_domaine ed on ed.id = euira.domaine_id
left join entrepot_sdc esdc on esdc.id = euira.sdc_id
left join entrepot_parcelle ep on ep.id = euira.parcelle_id
left join entrepot_zone ez on ez.id = euira.zone_id
left join entrepot_intervention_realise eir on eir.id = euir.intervention_realise_id
left join entrepot_intrant ei on euir.intrant_id = ei.id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;
