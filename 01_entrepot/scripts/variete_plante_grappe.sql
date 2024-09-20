CREATE TABLE entrepot_variete_plante_grappe AS
select 
r.topiaid as id ,
r.codevar ,
r.variete as libelle,
r.utilisation ,
r.couleur ,
r.code_gnis ,
r."source"
from refvarieteplantgrape r
where active is true;

alter table entrepot_variete_plante_grappe
ADD CONSTRAINT variete_plante_grappe_PK
primary key (id);