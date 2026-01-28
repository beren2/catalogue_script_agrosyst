
-- Voisinage de la parcelle
drop table if exists entrepot_parcelle_voisinage cascade;

CREATE TABLE entrepot_parcelle_voisinage AS
select
ab.basicplot parcelle_id,
r.iae_nom as libelle_voisinage
from adjacentelements_basicplot ab 
join entrepot_parcelle ep on ep.id = ab.basicplot 
join refelementvoisinage r on r.topiaid = ab.adjacentelements ;

alter table entrepot_parcelle_voisinage
ADD FOREIGN KEY (parcelle_id) REFERENCES entrepot_parcelle(id);

DO $$
BEGIN
    BEGIN
        alter table entrepot_parcelle_voisinage
        add constraint parcelle_voisinage_PK
        PRIMARY KEY (parcelle_id,libelle_voisinage);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;