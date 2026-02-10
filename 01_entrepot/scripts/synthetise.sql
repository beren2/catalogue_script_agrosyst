DROP TABLE IF EXISTS entrepot_synthetise CASCADE;

CREATE TABLE entrepot_synthetise AS
select
ps.topiaid id,
ps."name" nom,
ps.campaigns campagnes,
ps."source" source,
ps."comment" commentaire,
ps.practicedplot parcelle_type_id,
ps.growingsystem sdc_id,
ps.updatedate as derniere_maj,
ps.validated as valide
from practicedsystem ps
join entrepot_sdc es on es.id = ps.growingsystem 
where ps.active = true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_synthetise
        add constraint synthetise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

--alter table entrepot_synthetise
--ADD FOREIGN KEY (parcelle_type_id) REFERENCES entrepot_parcelle_type(id);

alter table entrepot_synthetise
ADD FOREIGN KEY (sdc_id) REFERENCES entrepot_sdc(id);


 


