create temporary table test2 as
select 
	ed.code as domaine_code, 
	ed.id as domaine_id, 
	ed.nom as domaine_nom, 
	ed.campagne as domaine_campagne,
	sdc.code as sdc_code, 
	sdc.id as sdc_id, 
	sdc.nom as sdc_nom, 
	es.id as systeme_synthetise_id,
	es.nom as systeme_synthetise_nom,
	es.campagnes as systeme_synthetise_campagnes,
	es.valide as systeme_synthetise_validation,
	ecs.id as culture_precedent_rang_id,
	ens_cible.id as culture_rotation_id,
	ens_cible.rang+1 as culture_rang,
	null as culture_indicateur_branche, -- information non trouvée et à priori inutile
	ens_cible.culture_code as culture_code,
	ec.nom as culture_nom,
	CASE CAST(ens_cible.fin_cycle AS BOOLEAN) WHEN true THEN 'OUI' WHEN false THEN 'NON' END fin_rotation,
	CASE CAST(ens_cible.memecampagne_noeudprecedent AS BOOLEAN) WHEN true THEN 'OUI' WHEN false THEN 'NON' END meme_campagne_culture_precedente,
	CASE CAST(ecs.culture_absente AS BOOLEAN) WHEN true THEN 'OUI' WHEN false THEN 'NON' END culture_absente,
	ecoc.complet_espece_edi as culture_especes_edi,
	ec_intermediaire.code as ci_code,
	ec_intermediaire.nom as ci_nom,
	ens_source.id as precedent_rotation_id,
	ens_source.rang as precedent_rang,
	null as precedent_indicateur_branche, -- information non trouvée et à priori inutile
	ens_source.culture_code as precedent_code,
	ec_source.nom as precedent_nom,
	ecoc_source.complet_espece_edi as precedent_especes_edi,
	ecs.frequence_source as frequence_connexion
from entrepot_connection_synthetise ecs
left join entrepot_connection_synthetise_restructure ecsr on ecsr.id = ecs.id
left join entrepot_noeuds_synthetise ens_source on ecs.source_noeuds_synthetise_id = ens_source.id 
left join entrepot_noeuds_synthetise ens_cible on ecs.cible_noeuds_synthetise_id  = ens_cible.id
left join entrepot_noeuds_synthetise_restructure ensr on ensr.id = ens_cible.id
left join entrepot_noeuds_synthetise_restructure ensr_source on ensr_source.id = ens_source.id
left join entrepot_culture ec on ec.id = ensr.culture_id
left join entrepot_culture_outils_can ecoc on ecoc.id = ec.id
left join entrepot_culture ec_source on ec_source.id = ensr_source.culture_id 
left join entrepot_culture_outils_can ecoc_source on ecoc_source.id = ec_source.id
left join entrepot_culture ec_intermediaire on ecsr.culture_intermediaire_id = ec_intermediaire.id
left join entrepot_synthetise es on ens_cible.synthetise_id = es.id
left join entrepot_sdc sdc on es.sdc_id = sdc.id
left join entrepot_dispositif edisp on sdc.dispositif_id = edisp.id
left join entrepot_domaine ed on ed.id = edisp.domaine_id
join entrepot_dispositif_filtres_outils_can edfoc on edisp.id = edfoc.id;




select * from entrepot_culture;
select * from entrepot_noeuds_synthetise_restructure;