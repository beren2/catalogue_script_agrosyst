select 
	ed.code as domaine_code, 
	ed.id as domaine_id, 
	ed.nom as domaine_nom, 
	ed.campagne as domaine_campagne,
	esdc.code as sdc_code,
	esdc.id as sdc_id,
	esdc.nom as sdc_nom,
	ep.id as parcelle_id,
	ep.nom as parcelle_nom,
	ez.id as zone_id, 
	ez.nom as zone_nom, 
	ec.id as culture_id, 
	ec.nom as culture_nom,
	ecoc.complet_espece_edi as culture_especes_edi,
	epppr.id as phase_id, 
	epppr.type as phase, 
	epppr.duree as duree_phase_ans,
	eppr.plantation_annee as annee_plantation,
	eppr.plantation_espacement_interrang_cm as inter_rang,
	eppr.plantation_espacement_intrarang_cm as espacement_sur_le_rang,
	eppr.plantation_densite_p_ha as densite_plantation, 
	eppr.verger_forme_fruitiere as forme_fruitiere_verger,
	eppr.feuillage_hauteur_cm as hauteur_frondaison, 
	eppr.feuillage_epaisseur_cm as epaisseur_frondaison,
	eppr.vigne_forme_fruitiere as forme_fruitiere_vigne,
	eppr.orientation_rang_id as orientation_rangs,
	eppr.taux_mortalite_pct as taux_mortalite_plantation, 
	eppr.taux_mortalite_annee_mesure as annee_mesure_taux_mortalite,
	eppr.type_enherbement,
	CASE eppr.pollinisateurs, WHEN true THEN 'oui' WHEN false THEN 'non' END pollinisateurs,
	eppr.pollinisateurs_pct as pourcentage_de_pollinisateurs,
	eppr.mode_repartition_pollinisateurs,
	eppr.autre_caracteristiques_couvert_vegetal as couvert_vegetal_commentaire
from entrepot_plantation_perenne_phases_realise epppr
left join entrepot_plantation_perenne_realise eppr on epppr.plantation_perenne_realise_id = eppr.id 
left join entrepot_zone ez on ez.id = eppr.zone_id
left join entrepot_parcelle ep on ep.id = ez.parcelle_id
left join entrepot_sdc esdc on esdc.id = ep.sdc_id
left join entrepot_domaine ed on ed.id = ep.domaine_id
left join entrepot_culture ec on ec.id = eppr.culture_id
left join entrepot_culture_outils_can ecoc on ecoc.id = ec.id
join entrepot_dispositif_filtres_outils_can edfoc on esdc.dispositif_id = edfoc.id;