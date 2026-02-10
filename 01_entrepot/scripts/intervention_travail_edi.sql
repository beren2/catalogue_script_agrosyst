DROP TABLE IF EXISTS entrepot_intervention_travail_edi CASCADE;

CREATE TABLE entrepot_intervention_travail_edi AS
select topiaid id,
reference_code code_reference,
intervention_agrosyst action_type,
reference_label action_label,
"source" ,
active actif
from refinterventionagrosysttravailedi refint  ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_intervention_travail_edi
        add constraint intervention_travail_edi_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
