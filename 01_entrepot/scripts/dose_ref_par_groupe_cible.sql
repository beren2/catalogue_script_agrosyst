CREATE TABLE entrepot_dose_ref_par_groupe_cible AS
select
r.topiaid as id, 
r.traitement_maa as type_traitement,
r.code_amm ,
r.code_culture_maa ,
r.culture_maa ,
r.code_groupe_cible_maa ,
r.groupe_cible_maa ,
r.campagne ,
r.dose_ref_maa ,
r.unit_dose_ref_maa ,
r.volume_max_bouillie
from refmaadosesrefpargroupecible r 
where active is true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_dose_ref_par_groupe_cible
        add constraint dose_ref_par_groupe_cible_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;