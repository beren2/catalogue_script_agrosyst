DROP TABLE IF EXISTS entrepot_levier CASCADE;

CREATE TABLE entrepot_levier AS
select
r.topiaid as id,
r.code,
r.lever as libelle,
r.sectiontype as type_section,
r.strategytype as type_strategie,
r.sector as filiere
from refstrategylever r 
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_levier
        ADD CONSTRAINT levier_PK
        primary key (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;