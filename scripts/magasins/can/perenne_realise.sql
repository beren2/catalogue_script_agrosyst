select 
	ed.code as domaine_code, 
	ed.id as domaine_di, 
	ed.nom as domaine_nom, 
	ed.campagne as domaine_campagne,
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
	eppr.verger_forme_fruitiere as forme_fruitiere_verge,
	eppr.feuillage_hauteur_cm as hauteur_frondaison, 
	eppr.feuillage_epaisseur_cm as epaisseur_frondaison,
	eppr.vigne_forme_fruitiere as forme_fruitiere_vigne,
	eppr.orientation_rang as orientation_rangs,
	eppr.taux_mortalite_pct as taux_mortalite_plantation, 
	eppr.taux_mortalite_annee_mesure as annees_mesure_taux_mortalite,
	eppr.type_enherbement,
	eppr.autre_caracteristiques_couvert_vegetal as couvert_vegetal_commentaire
from entrepot_plantation_perenne_phases_realise epppr
left join entrepot_plantation_perenne_realise eppr on epppr.plantation_perenne_realise_id = eppr.id 
left join entrepot_zone ez on ez.id = eppr.zone_id
left join entrepot_parcelle ep on ep.id = ez.parcelle_id
left join entrepot_sdc esdc on esdc.id = ep.sdc_id
left join entrepot_domaine ed on ed.id = ep.domaine_id
left join entrepot_culture ec on ec.id = eppr.culture_id
left join entrepot_culture_outils_can ecoc on ecoc.id = ec.id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;
