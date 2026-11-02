DROP TABLE IF EXISTS entrepot_utilisation_intrant_cible cascade; -- rattachement dispositif DEPHY actif

-------------------------------------
-- utilisation_intrant_cible
--------------------------------------
CREATE TABLE entrepot_utilisation_intrant_cible (
	id character varying(255),
	utilisation_intrant_id character varying(255),
	intrant_id character varying(255),
  	ref_cible_id character varying(255),
  	categorie character varying(255),
  	code_groupe_cible_maa character varying(255)
);


INSERT INTO entrepot_utilisation_intrant_cible (
	id,
	utilisation_intrant_id,
	intrant_id,
	ref_cible_id, 
	categorie, 
	code_groupe_cible_maa
)
select
	ppt.topiaid as id, 
	ppt.abstractphytoproductinputusage as utilisation_intrant_id,
	ppt.phytoproductinput as intrant_id, 
	ppt.target as ref_cible_id,
	ppt.category as categorie, 
	ppt.codegroupeciblemaa as code_groupe_cible_maa
	from phytoproducttarget ppt
	where ppt.abstractphytoproductinputusage is not null;

DO $$
BEGIN
    BEGIN
		alter table entrepot_utilisation_intrant_cible
		add constraint utilisation_intrant_cible_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;