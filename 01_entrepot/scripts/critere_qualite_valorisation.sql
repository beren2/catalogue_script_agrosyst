DROP TABLE IF EXISTS entrepot_critere_qualite_valorisation CASCADE;

CREATE TABLE entrepot_critere_qualite_valorisation AS
select
r.topiaid as id,
r.code,
r.qualitycriterialabel as libelle,
r.qualityattributetype as "type" ,
r.code_espece_botanique,
r.code_qualifiant_aee ,
r.espece ,
r.winevalorisation as valorisation_vin,
r.sector as filiere,
r.criteriaunit unite_critere,
r."source" 
from 
refqualitycriteria r 
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_critere_qualite_valorisation
        add constraint critere_qualite_valorisation_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;