-- Noeuds du cycle de culture
DROP TABLE IF EXISTS entrepot_noeuds_realise CASCADE;
CREATE TABLE entrepot_noeuds_realise AS
select
ecn.topiaid id,
ecn.rank rang,
ecn.croppingplanentry culture_id,
esc.zone zone_id
from effectivecropcyclenode ecn 
join effectiveseasonalcropcycle esc on esc.topiaid = ecn.effectiveseasonalcropcycle
join entrepot_culture ec on ec.id = ecn.croppingplanentry 
join entrepot_zone ez on ez.id = esc.zone;

DO $$
BEGIN
    BEGIN
        alter table entrepot_noeuds_realise
        add constraint noeuds_realise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_noeuds_realise
ADD FOREIGN KEY (culture_id) REFERENCES entrepot_culture(id);

alter table entrepot_noeuds_realise
ADD FOREIGN KEY (zone_id) REFERENCES entrepot_zone(id);

-- Connections du cycle de culture
DROP TABLE IF EXISTS entrepot_connection_realise CASCADE;
CREATE TABLE entrepot_connection_realise AS
select
ecc.topiaid id,
ecc.source source_noeuds_realise_id,
ecc.target cible_noeuds_realise_id,
ecc.intermediatecroppingplanentry culture_intermediaire_id
from effectivecropcycleconnection ecc 
join entrepot_noeuds_realise enr on enr.id = ecc.target 
left join entrepot_noeuds_realise enr2 on enr2.id = ecc.source;

DO $$
BEGIN
    BEGIN
        alter table entrepot_connection_realise
        add constraint connection_realise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_connection_realise
ADD FOREIGN KEY (source_noeuds_realise_id) REFERENCES entrepot_noeuds_realise(id);

alter table entrepot_connection_realise
ADD FOREIGN KEY (cible_noeuds_realise_id) REFERENCES entrepot_noeuds_realise(id);

alter table entrepot_connection_realise
ADD FOREIGN KEY (culture_intermediaire_id) REFERENCES entrepot_culture(id);
