select 
	ei.id as intrant_local_id,
	ei.type as intrant_type, 
	ei.type_produit as intrant_type_produit,
	ed.id as domaine_id, 
	ed.code as domaine_code, 
	ed.nom as domaine_nom, 
	ed.campagne as campagne, 
	ei.ref_id as intrant_ref_id,
	ei.ref_nom as intrant_ref_nom, 
	ei.nom_utilisateur as intrant_nom_utilisateur, 
	ei.code_amm as intrant_code_amm, 
	ei.semence_id, 
	ei.lot_semence_bio,
	ei.lot_semence_culture_id,
	ei.lot_semence_type,
	ei.biocontrole,
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
	ei.cao,
	ei.s,
	ei.unite_teneur_fert,
	ei.unite_application,
	ei.effet_sdn,
	ei.forme_fert_min,
	ei.caracteristique_1,
	ei.caracteristique_2,
	ei.caracteristique_3,
	ei.type_intrant_autre,
	ei.duree_de_vie,
	ei.type_produit_sans_amm,
	ei.prix_saisi,
	ei.prix_saisi_unite,
	ei.prix_ref,
	ei.prix_ref_unite,
	ei.prix_ref_bio,
	ei.prix_ref_bio_unite
from entrepot_intrant ei
left join entrepot_domaine ed on ei.domaine_id = ed.id
JOIN domaine_filtre df on df.domaine_id = ed.id;