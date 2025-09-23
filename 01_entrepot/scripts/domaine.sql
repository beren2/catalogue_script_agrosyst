CREATE TABLE entrepot_domaine AS
  WITH domainresponsibles as (
    SELECT domaincode, string_agg(au.lastname||' '||au.firstname, ', ') AS responsibles
    FROM userrole ur
    JOIN agrosystuser au ON ur.agrosystuser = au.topiaid
    WHERE domaincode IS NOT NULL
    GROUP BY domaincode
  )
  SELECT
    d.topiaid id,
    d.code code,
    d.name nom,
    d.siret,
    d.campaign campagne,
    d.type type_ferme,
    rl.departement departement,
    rl.codeinsee||' - '||rl.commune commune,
    rl.topiaid commune_id,
    rl.petiteRegionAgricoleCode|| ' - '||rl.petiteRegionAgricoleNom petite_region_agricole,
    d.zoning zonage,
    d.uaavulnarablepart pct_SAU_zone_vulnerable,
    d.uaastructuralsurplusareapart pct_SAU_zone_excedent_structurel,
    d.uaaactionpart pct_SAU_zone_actions_complementaires,
    d.uaanatura2000part pct_SAU_zone_natura_2000,
    d.uaaerosionregionpart pct_SAU_zone_erosion,
    d.uaawaterresourceprotectionpart pct_SAU_perimetre_protection_captage,
    d.description description,
    d.statuscomment statut_juridique_commentaire,
    d.chiefbirthyear annee_naissance_exploitant, 
    d.usedagriculturalarea SAU_totale,
    d.croppingplancomment cultures_commentaire,
    d.otheractivitiescomment autres_activites_commentaire,
    d.workforcecomment MO_commentaire,
    d.partnersnumber nombre_associes,
    d.otherworkforce MO_familiale_et_associes,
    d.permanentemployeesworkforce MO_permanente,
    d.temporaryemployeesworkforce MO_temporaire,
    d.familyworkforcewage MO_familiale_remuneration,
    d.wagecosts charges_salariales,
    d.cropsworkforce MO_conduite_cultures_dans_domaine_expe,
    d.msafee cotisation_MSA,
    d.averagetenantfarming fermage_moyen,
    d.decoupledassistance aides_decouplees,
    d.orientation otex_commentaire,
    dr.responsibles responsables_domaine, 
    d.nbplot as nombre_parcelles,
    d.furthestplotdistance as distance_siege_parcelle_max,
    d.areaaroundhq as surface_autour_siege_exploitation,
    d.groupedplots as parcelles_groupees,
    d.scatteredplots as parcelles_dispersees,
    d.ratherscatteredplots as parcelles_plutot_dispersees,
    d.joinedplots as parcelles_groupees_distinctes,
    d.rathergroupedplots as parcelles_plutot_groupees,
    d.maincontact as contact_principal,
    ro1.libelle_otex_18_postes as otex_18_nom,
    ro2.libelle_otex_70_postes as otex_70_nom,
    rls.libelle_insee as statut_juridique_nom,
    d.defaultweatherstation as station_meteo_defaut,
    d.objectives as objectifs,
    d.domainassets as atouts_domaine,
    d.domainconstraints as contraintes_domaine,
    d.domainlikelytrends as perspective_evolution_domaine,
    d.cooperativemember as membre_cooperative,
    d.developmentgroupmember as membre_groupe_developpement,
    d.cumamember as membre_cuma,
    d.stakestourist as domaine_touristique,
    d.operatorworkforce as main_oeuvre_exploitant,
    d.nonseasonalworkforce as main_oeuvre_non_saisoniere,
    d.seasonalworkforce as main_oeuvre_saisoniere,
    d.volunteerworkforce as main_oeuvre_volontaire,
    d.usedagriculturalareaforfarming as surface_agricole_utilisee_fermage,
    d.experimentalagriculturalarea as surface_agricole_experimentale,
    d.homogenizationexperimentalagriculturalarea as surface_agricole_experimentale_homogeneisation,
    d.irrigablearea as surface_irrigable,
    d.fallowarea as surface_jachere,
    d.annualcroparea as surface_culture_annuelle,
    d.vineyardandorchardarea as surface_vignoble_verger,
    d.meadowarea as surface_prairie,
    d.meadowalwayswithgrassarea as surface_toujours_prairie,
    d.meadowotherarea as surface_prairie_autre,
    d.meadowonlypasturedarea as surface_prairie_uniquement_paturee,
    d.meadowonlymowedarea as surface_prairie_uniquement_fauchee,
    d.meadowpasturedandmowedarea as surface_prairie_paturee_et_fauchee,
    d.heathlandandroutesarea as surface_landes_parcours,
    d.summerandmountainpasturearea as surface_paturage_ete_montagne,
    d.collectiveheathlandandroutesarea as surface_collective_landes_parcours,
    d.collectivesummerandmountainpasturearea as surface_collective_paturage_ete_montagne,
    d.totalotherareas as total_surface_autre
  FROM domain d
  LEFT JOIN domainresponsibles dr ON d.code = dr.domaincode
  LEFT JOIN reflocation rl ON d.location = rl.topiaid
  LEFT JOIN reflegalstatus rls ON d.legalstatus = rls.topiaid
  LEFT JOIN refotex ro1 ON d.otex18 = ro1.topiaid
  LEFT JOIN refotex ro2 ON d.otex70 = ro2.topiaid
 WHERE d.active = TRUE;

DO $$
BEGIN
    BEGIN
        alter table entrepot_domaine
        add constraint domaine_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

-- Sols du domaine
drop table if exists entrepot_domaine_sol cascade;

CREATE TABLE entrepot_domaine_sol AS
select 
g.topiaid id,
g.name nom_local,
g."comment" commentaire,
g.importance SAU_concernee_pct,
g."domain" domaine_id,
g.refsolarvalis sol_arvalis_id
from ground g
join entrepot_domaine ed on ed.id = g."domain" ;
 
DO $$
BEGIN
    BEGIN
        alter table entrepot_domaine_sol
        ADD CONSTRAINT domaine_sol_PK
        primary key (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_domaine_sol
add FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);

alter table entrepot_domaine_sol
add FOREIGN KEY (sol_arvalis_id) REFERENCES entrepot_sol_arvalis(id);


-- Surfaces par especes
-- l'information est stockée dans la colonne speciestoarea sous format json {"1espece_qualif_saison" : surface, "2espece_qualif_saison" : surface)
-- pb : il n'y a pas de clé unique puisque c'est issus d'une colonne de la table domaine
-- On en crée une 

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

drop table if exists entrepot_speciestoarea;
CREATE TABLE entrepot_speciestoarea(
  id uuid DEFAULT uuid_generate_v4(), -- v4 pour que la génération se base juste sur des nombres aleatoires
  campagne integer,
  code_espece character varying(255),
  code_qualifiant character varying(255),
  code_type_saisonnier character varying(255),
  surface_cultivee double precision,
	domaine_id character varying(255)
);

-- grace a une boucle qui parcours la table + une 2e qui parcours le json d'une ligne , on peut isolé dans une ligne chaque esp de chaque domaine
do $$
declare
    d record;
begin
for d in select topiaid, campaign , speciestoarea 
    from domain
    where speciestoarea like '{"%'
    loop
        for i IN 1..(select (length(d.speciestoarea) - length(replace(d.speciestoarea,',',''))) + 1) LOOP
        	insert into entrepot_speciestoarea(domaine_id,campagne, code_espece) select d.topiaid, d.campaign, split_part(d.speciestoarea, ',', i);
        RAISE NOTICE 'counter: %', i;
        END LOOP;
    raise notice '% - % - %', d.topiaid, d.campaign, d.speciestoarea ;
    end loop;
end;
$$;

-- retirer les caractères speciaux et remplir la colonne de surface cultivée
update entrepot_speciestoarea set code_espece = replace(code_espece, '{', '');
update entrepot_speciestoarea set code_espece = replace(code_espece, '}', '');
update entrepot_speciestoarea set code_espece = replace(code_espece, '"', '');

update entrepot_speciestoarea set surface_cultivee = case when length(split_part(code_espece, ':',2)) = 0 then null 
                                                                              else cast(split_part(code_espece, ':',2) as double precision) end
;
update entrepot_speciestoarea set code_espece = split_part(code_espece, ':',1);
update entrepot_speciestoarea set code_espece = replace(code_espece, ':', '');

update entrepot_speciestoarea set code_qualifiant = coalesce(split_part(code_espece, '_',2),null);
update entrepot_speciestoarea set code_type_saisonnier = coalesce(split_part(code_espece, '_', 3),null);
update entrepot_speciestoarea set code_espece = coalesce(split_part(code_espece, '_', 1),null);

drop table if exists entrepot_domaine_surface_especes_cultivees;
CREATE TABLE entrepot_domaine_surface_especes_cultivees as 
select 
sp.id,
sp.campagne,
r1.topiaid as espece_id,
sp.surface_cultivee,
sp.domaine_id
from entrepot_speciestoarea sp
join entrepot_domaine e on e.id = sp.domaine_id
join (select distinct topiaid, code_espece_botanique, libelle_espece_botanique, code_qualifiant_aee, libelle_qualifiant_aee , code_type_saisonnier_aee, libelle_type_saisonnier_aee from refespece) r1 on r1.code_espece_botanique = UPPER(sp.code_espece) and r1.code_qualifiant_aee = UPPER(sp.code_qualifiant) and r1.code_type_saisonnier_aee = UPPER(sp.code_type_saisonnier);

DO $$
BEGIN
    BEGIN
        alter table entrepot_domaine_surface_especes_cultivees
        ADD CONSTRAINT domaine_surface_especes_cultivees_PK
        primary key (id,espece_id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_domaine_surface_especes_cultivees
add FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
