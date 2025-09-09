-- Noeuds du cycle de culture
DROP TABLE IF EXISTS entrepot_noeuds_synthetise CASCADE;
CREATE TABLE entrepot_noeuds_synthetise AS
select
pcn.topiaid id,
pcn.rank rang,
pcn.endcycle fin_cycle,
pcn.croppingplanentrycode culture_code,
pcn.samecampaignaspreviousnode memecampagne_noeudprecedent,
pcn.initnodefrequency fq_initial_noeud,
pc.practicedsystem synthetise_id,
pcn.y ordonnee_interface
from practicedcropcyclenode pcn 
join practicedseasonalcropcycle psc on psc.topiaid = pcn.practicedseasonalcropcycle 
join practicedcropcycle pc on pc.topiaid = psc.topiaid 
join entrepot_synthetise es on es.id = pc.practicedsystem ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_noeuds_synthetise
        add constraint noeuds_synthetise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_noeuds_synthetise
ADD FOREIGN KEY (synthetise_id) REFERENCES entrepot_synthetise(id);

-- Connections du cycle de culture
DROP TABLE IF EXISTS entrepot_connection_synthetise CASCADE;
CREATE TABLE entrepot_connection_synthetise AS
select 
pcc.topiaid id,
pcc.intermediatecroppingplanentrycode culture_intermediaire_code,
pcc.croppingplanentryfrequency frequence_source, -- A VERIFIER
pcc.notusedforthiscampaign culture_absente,
pcc.source source_noeuds_synthetise_id,
pcc.target cible_noeuds_synthetise_id
from practicedcropcycleconnection pcc
join entrepot_noeuds_synthetise ens on ens.id = pcc.source
join entrepot_noeuds_synthetise ens2 on ens2.id = pcc.target ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_connection_synthetise
        add constraint connection_synthetise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_connection_synthetise
ADD FOREIGN KEY (source_noeuds_synthetise_id) REFERENCES entrepot_noeuds_synthetise(id);

alter table entrepot_connection_synthetise
ADD FOREIGN KEY (cible_noeuds_synthetise_id) REFERENCES entrepot_noeuds_synthetise(id);


