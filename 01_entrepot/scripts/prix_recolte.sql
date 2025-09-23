CREATE TABLE entrepot_prix_recolte AS
select
r.topiaid as id,
r.code_destination_a, --code_destination_a dans destination_valorisation 
r.code_qualifiant_aee,
r.produitrecolte as libelle_espece_botanique,
r.organic as bio,
r.campaign as campagne,
r.priceunit as prix_unite,
r.price as prix,
r.code_scenario as code_scenario,
r.scenario as scenario, 
r."source"
from refharvestingprice r
where active is true
and code_scenario = '';

DO $$
BEGIN
    BEGIN
        alter table entrepot_prix_recolte
        add constraint prix_recolte_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;