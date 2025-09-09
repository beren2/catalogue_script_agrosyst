CREATE TABLE entrepot_culture AS
SELECT
    cpe.topiaid AS id,
    cpe.name AS nom,
    cpe.mixspecies AS melange_especes,
    cpe.mixvariety AS melange_varietes,
    cpe.pasturedmeadow as prairie_paturee,
    cpe.temporarymeadow as prairie_temporaire,
    cpe.mowedmeadow as prairie_fauchee,
    cpe.code AS code,
    cpe.type AS type,
    cpe.domain as domaine_id
FROM croppingplanentry cpe
JOIN entrepot_domaine d on cpe."domain" = d.id;

DO $$
BEGIN
    BEGIN
        alter table entrepot_culture
        add constraint culture_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_culture
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
