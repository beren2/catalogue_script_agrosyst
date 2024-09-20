create table entrepot_criteres_selection as 
select 
d.topiaid domaine_id,
d.campaign campagne,
gp.topiaid dispositif_id
from domain d
join (select * from growingplan where active = true) gp on gp."domain" = d.topiaid 
where d.active = true;
