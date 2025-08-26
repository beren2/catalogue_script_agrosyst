-- Zonage de la parcelle
drop table if exists entrepot_parcelle_zonage;

CREATE TABLE entrepot_parcelle_zonage AS
select
bp.basicplot parcelle_id,
r.libelle_engagement_parcelle as libelle_zonage
from basicplot_plotzonings bp
join entrepot_parcelle ep on ep.id = bp.basicplot 
join refparcellezonageedi r on r.topiaid = bp.plotzonings ;

alter table entrepot_parcelle_zonage
ADD FOREIGN KEY (parcelle_id) REFERENCES entrepot_parcelle(id);

DO $$
BEGIN
    BEGIN
        alter table entrepot_parcelle_zonage
        add constraint parcelle_zonage_PK
        PRIMARY KEY (parcelle_id,libelle_zonage);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
