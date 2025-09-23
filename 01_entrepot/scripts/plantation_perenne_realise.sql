CREATE TABLE entrepot_plantation_perenne_realise AS
select
epc.topiaid id,
epc.plantingyear plantation_annee,
epc.plantinginterfurrow plantation_espacement_interrang_cm, -- Inter-rang de plantation
epc.plantingspacing plantation_espacement_intrarang_cm, -- Espacement de plantation sur le rang 
refo.reference_label orientation_rang,
epc.plantingdensity plantation_densite_p_ha,
epc.orchardfrutalform verger_forme_fruitiere,
epc.vinefrutalform vigne_forme_fruitiere,
epc.foliageheight feuillage_hauteur_cm,
epc.foliagethickness feuillage_epaisseur_cm,
epc.plantingdeathrate taux_mortalite_pct,
epc.plantingdeathratemeasureyear taux_mortalite_annee_mesure,
epc.pollinator pollinisateurs,
epc.pollinatorpercent pollinisateurs_pct,
epc.pollinatorspreadmode mode_repartition_pollinisateurs,
epc.weedtype type_enherbement,
epc.othercharacteristics autre_caracteristiques_couvert_vegetal,
epc.croppingplanentry culture_id,
epc.zone zone_id
from effectiveperennialcropcycle epc 
join entrepot_zone z on z.id = epc.zone
left join reforientationedi refo on refo.topiaid = epc.orientation ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_plantation_perenne_realise
        add constraint plantation_perenne_realise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_plantation_perenne_realise
ADD FOREIGN KEY (zone_id) REFERENCES entrepot_zone(id);

alter table entrepot_plantation_perenne_realise
ADD FOREIGN KEY (culture_id) REFERENCES entrepot_culture(id);

drop table if exists entrepot_plantation_perenne_phases_realise;
CREATE TABLE entrepot_plantation_perenne_phases_realise AS
select
ecp.topiaid id,
ecp.duration duree,
ecp."type",
eppr.id plantation_perenne_realise_id -- pour être de meme format que les synthetises, on met ce lien là pour simplifier par rapport a la bdd operationnelle agrosyst
from effectivecropcyclephase ecp
join effectiveperennialcropcycle epc on epc.phase = ecp.topiaid 
join entrepot_plantation_perenne_realise eppr on eppr.id = epc.topiaid;

DO $$
BEGIN
    BEGIN
        alter table entrepot_plantation_perenne_phases_realise
        add constraint plantation_perenne_phases_realise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_plantation_perenne_phases_realise
ADD FOREIGN KEY (plantation_perenne_realise_id) REFERENCES entrepot_plantation_perenne_realise(id);

drop table if exists entrepot_plantation_perenne_especes_realise;
CREATE TABLE entrepot_plantation_perenne_especes_realise AS
select
ecs.topiaid id,
concat(refvar.denomination,refpg.variete) porte_greffe,
case when refc.topiaid is not null then concat(refc.codeclone,', ', refc.anneeagrement,' (',refc.origine,')') end clone_greffe,
ecs.plantscertified certification_plants,
ecs.overgraftdate date_sur_greffage,
ecc.id composant_culture_id,
eppr.id plantation_perenne_realise_id
from effectivecropcyclespecies ecs 
left join refcloneplantgrape refc on refc.topiaid = ecs.graftclone 
left join refvarietegeves refvar on refvar.topiaid = ecs.graftsupport 
left join refvarieteplantgrape refpg on refpg.topiaid = ecs.graftsupport
join entrepot_composant_culture ecc on ecc.id = ecs.croppingplanspecies 
join entrepot_plantation_perenne_realise eppr on eppr.id = ecs.effectiveperennialcropcycle ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_plantation_perenne_especes_realise
        add constraint plantation_perenne_especes_realise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_plantation_perenne_especes_realise
ADD FOREIGN KEY (composant_culture_id) REFERENCES entrepot_composant_culture(id);

alter table entrepot_plantation_perenne_especes_realise
ADD FOREIGN KEY (plantation_perenne_realise_id) REFERENCES entrepot_plantation_perenne_realise(id);
