CREATE TABLE entrepot_prix_produit_phyto_sanitaire AS
select
r.topiaid as id,
r.id_produit ,
r.id_traitement ,
r.code_amm ,
r.nom_produit ,
r.campaign as campagne,
r.price as prix,
r.unit as unite,
r."source" 
from refprixphyto r
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_prix_produit_phyto_sanitaire
        add constraint prix_produit_phyto_sanitaire_pk
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
