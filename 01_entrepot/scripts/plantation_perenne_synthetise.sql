CREATE TABLE entrepot_plantation_perenne_synthetise AS
select
ppc.topiaid id,
ppc.plantingyear plantation_annee,
ppc.soloccupationpercent pct_occupation_sol,
ppc.plantinginterfurrow plantation_espacement_interrang_cm, -- Inter-rang de plantation
ppc.plantingspacing plantation_espacement_intrarang_cm, -- Espacement de plantation sur le rang 
refo.reference_label orientation_rang,
ppc.plantingdensity plantation_densite_p_ha,
ppc.orchardfrutalform verger_forme_fruitiere,
ppc.vinefrutalform vigne_forme_fruitiere,
ppc.foliageheight feuillage_hauteur_cm,
ppc.foliagethickness feuillage_epaisseur_cm,
ppc.plantingdeathrate taux_mortalite_pct,
ppc.plantingdeathratemeasureyear taux_mortalite_annee_mesure,
ppc.pollinator pollinisateurs,
ppc.pollinatorpercent pollinisateurs_pct,
ppc.pollinatorspreadmode mode_repartition_pollinisateurs,
ppc.weedtype type_enherbement,
ppc.othercharacteristics autre_caracteristiques_couvert_vegetal,
ppc.croppingplanentrycode culture_code,
esynth.id synthetise_id
from practicedperennialcropcycle ppc 
join practicedcropcycle pc on pc.topiaid = ppc.topiaid 
join entrepot_synthetise esynth on esynth.id = pc.practicedsystem
left join reforientationedi refo on refo.topiaid = ppc.orientation ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_plantation_perenne_synthetise
        add constraint plantation_perenne_synthetise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_plantation_perenne_synthetise
ADD FOREIGN KEY (synthetise_id) REFERENCES entrepot_synthetise(id);

drop table if exists entrepot_plantation_perenne_phases_synthetise;
CREATE TABLE entrepot_plantation_perenne_phases_synthetise AS
select
pcp.topiaid id,
pcp.duration duree,
pcp."type" ,
epps.id plantation_perenne_synthetise_id
from practicedcropcyclephase pcp
join entrepot_plantation_perenne_synthetise epps on epps.id = pcp.practicedperennialcropcycle;

DO $$
BEGIN
    BEGIN
        alter table entrepot_plantation_perenne_phases_synthetise
        add constraint plantation_perenne_phases_synthetise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_plantation_perenne_phases_synthetise
ADD FOREIGN KEY (plantation_perenne_synthetise_id) REFERENCES entrepot_plantation_perenne_synthetise(id);

drop table if exists entrepot_plantation_perenne_especes_synthetise;
CREATE TABLE entrepot_plantation_perenne_especes_synthetise AS
select 
pcs.topiaid id,
concat(refvar.denomination,refpg.variete) porte_greffe,
case when refc.topiaid is not null then concat(refc.codeclone,', ', refc.anneeagrement,' (',refc.origine,')') end clone_greffe,
pcs.plantscertified certification_plants,
pcs.overgraftdate date_sur_greffage,
epps.id plantation_perenne_synthetise_id
from practicedcropcyclespecies pcs 
left join refcloneplantgrape refc on refc.topiaid = pcs.graftclone 
left join refvarietegeves refvar on refvar.topiaid = pcs.graftsupport 
left join refvarieteplantgrape refpg on refpg.topiaid = pcs.graftsupport
join entrepot_plantation_perenne_synthetise epps on epps.id = pcs."cycle" ;