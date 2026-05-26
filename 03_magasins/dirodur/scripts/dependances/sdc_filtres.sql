-- On ne veut conserver que les sdc qui n'ont que des itk qui passent les filtres
create temporary table if not exists count_itk_dirodur as
select sdc_id, count(*) from entrepot_itk_filtres_outils_dirodur eifod 
group by sdc_id;

create temporary table if not exists count_itk_realise as
select sdc_id, count(*) from entrepot_noeuds_realise enr
left join entrepot_zone z on enr.zone_id = z.id
left join entrepot_parcelle p on z.parcelle_id = p.id
left join entrepot_sdc sdc on p.sdc_id = sdc.id
group by sdc_id;

create temporary table if not exists count_itk_synthetise as
select sdc_id, count(*) from entrepot_connection_synthetise ecs 
left join entrepot_noeuds_synthetise ens on ecs.cible_noeuds_synthetise_id = ens.id
left join entrepot_synthetise es on es.id = ens.synthetise_id
left join entrepot_sdc sdc on sdc.id = es.sdc_id
group by sdc_id;

create temporary table if not exists filtre_sdc_from_itk_dirodur as
select 
	sdc.id as sdc_id,
    COALESCE(cird.count, 0) as count_itk_realise,
    COALESCE(cisd.count, 0) as count_itk_synthetise,
    COALESCE(cid.count, 0) as count_itk_dirodur
from entrepot_sdc sdc
left join count_itk_realise cird on sdc.id = cird.sdc_id
left join count_itk_synthetise cisd on sdc.id = cisd.sdc_id
left join count_itk_dirodur cid on sdc.id = cid.sdc_id
WHERE (COALESCE(cird.count, 0) + COALESCE(cisd.count, 0)) = COALESCE(cid.count, 0) and cid.count > 0;