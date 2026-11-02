DROP TABLE IF EXISTS entrepot_criteres_selection CASCADE;

create table entrepot_criteres_selection as 
select 
d.topiaid domaine_id,
d.campaign campagne,
gp.topiaid dispositif_id
from domain d
join (select * from growingplan where active = true) gp on gp."domain" = d.topiaid 
where d.active = true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_criteres_selection
        add constraint criteres_selection_PK
        PRIMARY KEY (dispositif_id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;