DROP TABLE IF EXISTS entrepot_groupe_cible CASCADE;

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

DO $$
BEGIN
    BEGIN
		alter table entrepot_groupe_cible
		add constraint groupe_cible_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
