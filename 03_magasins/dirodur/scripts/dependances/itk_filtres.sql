-- On constitue un jeu de données qui nous permet de savoir quels sont les itks conservés d'après les filtres
-- celui-ci sera modifié lorsque 
create temporary table if not exists entrepot_itk_filtre as
select 
	eirp.noeuds_realise_id, 
	eirp.culture_id,
    null as connection_synthetise_id
from entrepot_itk_realise_performance eirp
left join entrepot_itk_filtres_outils_dirodur eifod on (eirp.noeuds_realise_id = eifod.noeuds_realise_id and eirp.culture_id = eifod.culture_id)
join entrepot_sdc_statut_temporel_outils_dirodur esstod on esstod.sdc_id = eifod.sdc_id
where (eifod.filtre_alerte is false)
UNION 
select 
    null as noeuds_realise_id,
    null as culture_id,
	eisp.connection_synthetise_id
from entrepot_itk_synthetise_performance eisp
left join entrepot_itk_filtres_outils_dirodur eifod on (eisp.connection_synthetise_id = eifod.connection_synthetise_id)
join entrepot_sdc_statut_temporel_outils_dirodur esstod on esstod.sdc_id = eifod.sdc_id
where (eifod.filtre_alerte is false);


