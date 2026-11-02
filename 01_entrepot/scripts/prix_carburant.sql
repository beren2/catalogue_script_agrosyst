DROP TABLE IF EXISTS entrepot_prix_carburant cascade;

CREATE TABLE entrepot_prix_carburant AS
select
r.topiaid as id,
r.campaign as campagne,
r.price as prix,
r.unit as unite,
r."source" 
from refprixcarbu r
where active is true; -- les lignes ou les scenarios sont mentionnées ne sont pas retires puisque pas de valeurs sinon

DO $$
BEGIN
    BEGIN
        alter table entrepot_prix_carburant
        add constraint prix_carburant_pk
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
