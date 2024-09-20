CREATE TABLE entrepot_otex AS
select 
r.topiaid as id ,
r.code_otex_70_postes ,
r.libelle_otex_70_postes ,
r.code_otex_18_postes ,
r.libelle_otex_18_postes ,
r."source"
from refotex r 
where active is true;

alter table entrepot_otex
add constraint otext_PK
PRIMARY KEY (id);
