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
	--es.validation as systeme_synthetie_validation --> attention, à rajouter dans l'entrepôt
	ecs.id as culture_rotation_id, 
	ens.id as culture_rotation_id,
	--rajouter culture_indicateur_branche
	ec.code as culture_code, 
	ec.nom as culture_nom,
	ens.fin_cycle as fin_rotation,
	ens.memecampagne_noeudprecedent as meme_campagne_culture_precedente,
	ecs.culture_absente,
	ecoc.complet_espece_edi as culture_especes_edi,
	ecs.culture_intermediaire_code,
	eci.nom,
	ens_prec.id as precedent_rotation_id,
	ens_prec.rang as precedent_rang,
	--ens_prec.indicateur_branche --> précédent indicateur branche
	ec_prec.code as precedent_code, 
	ec_prec.nom as precedent_nom,
	ecoc_prec.complet_espece_edi as precedent_especes_edi
from entrepot_connection_synthetise ecs
left join entrepot_noeuds_synthetise ens_prec on ecs.source_noeuds_synthetise_id = ens_prec.id
left join entrepot_noeuds_synthetise ens on ecs.cible_noeuds_synthetise_id = ens.id
left join entrepot_synthetise es on es.id = ens.synthetise_id
left join entrepot_sdc esdc on esdc.id = es.sdc_id
left join entrepot_dispositif edi on edi.id = esdc.dispositif_id
left join entrepot_domaine ed on ed.id = edi.domaine_id
left join entrepot_noeuds_synthetise_restructure ensr on ensr.id = ens.id
left join entrepot_noeuds_synthetise_restructure ensr_prec on ensr_prec.id = ens_prec.id
left join entrepot_culture ec on ec.id = ensr.culture_id
left join entrepot_culture ec_prec on ec_prec.id = ensr_prec.culture_id
left join entrepot_culture_outils_can ecoc on ec.id = ecoc.id
left join entrepot_culture_outils_can ecoc_prec on ec_prec.id = ecoc_prec.id
left join entrepot_connection_synthetise_restructure ecsr on ecsr.id = ecs.id
left join entrepot_culture eci on eci.id = ecsr.culture_intermediaire_id
join entrepot_dispositif_filtres_outils_can edifoc on edi.id = edifoc.id;