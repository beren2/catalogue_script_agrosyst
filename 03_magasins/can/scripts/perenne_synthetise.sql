select 
	ed.code as domaine_code, 
	ed.id as domaine_id, 
	ed.nom as domaine_nom, 
	ed.campagne as domaine_campagne,
	esdc.code as sdc_code,
	esdc.id as sdc_id, 
	esdc.nom as sdc_nom,
	es.id as systeme_synthetise_id,
	es.nom as systeme_synthetise_nom,
	es.campagnes as systeme_synthetise_campagnes,
	CASE CAST(es.valide AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END systeme_synthetise_validation,
	ec.code as culture_code, 
	ec.nom as culture_nom,
	eppps.id as phase_id, 
	eppps."type" as phase, 
	eppps.duree as duree_phase_ans,
	epps.plantation_annee as annee_plantation,
	epps.plantation_espacement_interrang_cm as inter_rang,
	epps.plantation_espacement_intrarang_cm as espacement_sur_le_rang,
	epps.pct_occupation_sol as pourcentage_sole_sdc,
	epps.plantation_densite_p_ha as densite_plantation, 
	epps.verger_forme_fruitiere as forme_fruitiere_verger,
	epps.feuillage_hauteur_cm as hauteur_frondaison, 
	epps.feuillage_epaisseur_cm as epaisseur_frondaison,
	epps.vigne_forme_fruitiere as forme_fruitiere_vigne,
	epps.orientation_rang as orientation_rangs,
	epps.taux_mortalite_pct as taux_mortalite_plantation, 
	epps.taux_mortalite_annee_mesure as annee_mesure_taux_mortalite,
	epps.type_enherbement,
	CASE CAST(epps.pollinisateurs AS BOOLEAN) WHEN true THEN 'oui' WHEN false THEN 'non' END pollinisateurs,
	epps.pollinisateurs_pct as pourcentage_de_pollinisateurs,
	epps.mode_repartition_pollinisateurs,
	epps.autre_caracteristiques_couvert_vegetal as couvert_vegetal_commentaire
from entrepot_plantation_perenne_phases_synthetise eppps
left join entrepot_plantation_perenne_synthetise epps on eppps.plantation_perenne_synthetise_id = epps.id 
left join entrepot_plantation_perenne_synthetise_restructure eppsr on eppsr.id = epps.id
left join entrepot_synthetise es on es.id = epps.synthetise_id 
left join entrepot_sdc esdc on esdc.id = es.sdc_id
left join entrepot_dispositif edi on edi.id = esdc.dispositif_id
left join entrepot_domaine ed on ed.id = edi.domaine_id
left join entrepot_culture ec on ec.id = eppsr.culture_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;