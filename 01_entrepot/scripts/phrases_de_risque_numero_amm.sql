CREATE TABLE entrepot_phraserisque_mentiondanger_numero_amm AS
SELECT 
r.topiaid as id,
r.code_amm , 
r.type_produit ,
r.type_info ,
r.code_info,
r.libelle_info , 
r.libelle_court_info ,
r.danger_environnement ,
r.toxique_utilisateur ,
r.cmr,
r."source" 
from refphrasesrisqueetclassesmentiondangerparamm r 
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_phraserisque_mentiondanger_numero_amm
        add constraint phraserisque_mentiondanger_numero_amm_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
