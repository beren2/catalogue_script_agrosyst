CREATE TABLE entrepot_reseau AS
select 
	n.topiaid as id,
	n.name as nom, 
	n.description as description,
	n.codeconventiondephy as code_convention_dephy
from network n
where n.active is true;

alter table entrepot_reseau
add constraint entrepot_reseau_PK_
PRIMARY KEY (id);