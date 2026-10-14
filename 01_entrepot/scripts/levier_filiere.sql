DROP TABLE IF EXISTS entrepot_levier_filiere CASCADE;
CREATE TABLE entrepot_levier_filiere AS
select
r.owner as levier_id,
r.sector as filiere
from refstrategylever_sector r;

DO $$
BEGIN
    BEGIN
        alter table entrepot_levier_filiere
        ADD CONSTRAINT levier_filiere_PK
        primary key (levier_id,filiere);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;