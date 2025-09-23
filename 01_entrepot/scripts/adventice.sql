CREATE TABLE entrepot_adventice AS
select 
	r.topiaid as id, 
	r.adventice as label,
	r.identifiant as code,
	r.famille_de_culture
from refadventice r;

DO $$
BEGIN
    BEGIN
		alter table entrepot_adventice
		ADD CONSTRAINT entrepot_adventice_PK
		primary key (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;