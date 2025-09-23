CREATE TABLE entrepot_destination_valorisation AS
select
r.topiaid as id,
r.code_destination_a ,
r.destination as libelle,
r.code_espece_botanique ,
r.code_qualifiant_aee , 
r.espece as libelle_espece,
r.winevalorisation as valorisation_vin,
r.sector as filiere,
r.yealdunit as rendement_unite,
r."source"
from 
refdestination r 
where active is true
;

DO $$
BEGIN
    BEGIN
        alter table entrepot_destination_valorisation
        add constraint destination_valorisation_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;