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
	enr.rang+1 as culture_rang,
	ec.id as culture_id,
	ec.nom as culture_nom,
	ecoc.complet_espece_edi as culture_especes_edi,
	eci.id as ci_id,
	eci.nom as ci_nom,
	ec_prec.id as precedent_id, 
	ec_prec.nom as precedent_nom,
	ecoc_prec.complet_espece_edi as precedent_especes_edi
from entrepot_noeuds_realise enr
left join entrepot_zone ez on ez.id = enr.zone_id
left join entrepot_connection_realise ecr on ecr.cible_noeuds_realise_id = enr.id
left join entrepot_noeuds_realise enr_prec on ecr.source_noeuds_realise_id = enr_prec.id
left join entrepot_parcelle ep on ep.id = ez.parcelle_id
left join entrepot_domaine ed on ed.id = ep.domaine_id
left join entrepot_culture ec on ec.id = enr.culture_id
left join entrepot_culture ec_prec on enr_prec.culture_id = ec_prec.id -- c'est celle ligne 
left join entrepot_culture eci on eci.id = ecr.culture_intermediaire_id
left join entrepot_sdc esdc on esdc.id = ep.sdc_id
left join entrepot_culture_outils_can ecoc on ecoc.id = enr.culture_id
left join entrepot_culture_outils_can ecoc_prec on ecoc_prec.id = enr_prec.culture_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id;