CREATE TABLE entrepot_reseau AS
select 
	n.topiaid as id,
	n.name as nom, 
	n.description as description,
	n.codeconventiondephy as code_convention_dephy,
	n.active as actif
from network n;

DO $$
BEGIN
    BEGIN
		alter table entrepot_reseau
		add constraint entrepot_reseau_PK_
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
