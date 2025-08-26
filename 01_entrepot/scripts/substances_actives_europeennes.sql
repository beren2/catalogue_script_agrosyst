CREATE TABLE entrepot_substance_active_europeenne AS
SELECT 
    r.topiaid as id , 
    r.id_sa, 
    r.libelle_sa_eu,
    r.statut_regl_1107_2009 ,
    r.libelle_sa_fr,
    r.libelle_sa_variant_fr,
    r.numero_cas ,
    r.autorisation_fr ,
    r.coef_ponderation , 
    r.campagne ,
    r.date_approbation_eu ,
    r.date_expiration_eu ,
    r.sa_candidates_substitution ,
    r.substances_de_base ,
    r.sa_faible_risque ,
    r.pays ,
    r.cuivre ,
    r.soufre ,
    r."source"
from refsubstancesactivescommissioneuropeenne r
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_substance_active_europeenne
        add constraint substance_active_europeenne_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
