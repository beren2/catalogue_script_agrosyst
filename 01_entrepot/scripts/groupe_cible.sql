CREATE TABLE entrepot_groupe_cible AS
select
	r.topiaid as id,
	r.reference_param as type,
	r.cible_generique,
	r.cible_edi_ref_id ,
	r.cible_edi_ref_code ,
	r.cible_edi_ref_label ,
	r.code_groupe_cible_maa ,
	r.groupe_cible_maa 
from refciblesagrosystgroupesciblesmaa r 
where active is true;

alter table entrepot_groupe_cible
add constraint groupe_cible_PK
PRIMARY KEY (id);
