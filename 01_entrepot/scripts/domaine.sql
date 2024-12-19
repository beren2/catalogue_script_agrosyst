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
    rls.libelle_insee statut_juridique_nom,
    d.statuscomment statut_juridique_commentaire,
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
    ro1.libelle_otex_18_postes otex_18_nom,
    ro2.libelle_otex_70_postes otex_70_nom,
    d.orientation otex_commentaire,
    dr.responsibles responsables_domaine
  FROM domain d
  LEFT JOIN domainresponsibles dr ON d.code = dr.domaincode
  LEFT JOIN reflocation rl ON d.location = rl.topiaid
  LEFT JOIN reflegalstatus rls ON d.legalstatus = rls.topiaid
  LEFT JOIN refotex ro1 ON d.otex18 = ro1.topiaid
  LEFT JOIN refotex ro2 ON d.otex70 = ro2.topiaid
 WHERE d.active = TRUE;

alter table entrepot_domaine
add constraint domaine_PK
PRIMARY KEY (id);

-- Sols du domaine
drop table if exists entrepot_domaine_sol cascade;

CREATE TABLE entrepot_domaine_sol AS
select 
g.topiaid id,
g.name nom_local,
g."comment" commentaire,
g.importance SAU_concernee_pct,
g."domain" domaine_id,
g.refsolarvalis refsolarvalis_id
from ground g
join entrepot_domaine ed on ed.id = g."domain" ;
 
alter table entrepot_domaine_sol
ADD CONSTRAINT domaine_sol_PK
primary key (id);

alter table entrepot_domaine_sol
add FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);

alter table entrepot_domaine_sol
add FOREIGN KEY (refsolarvalis_id) REFERENCES refsolarvalis(topiaid);


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

--alter table entrepot_domaine_surface_especes_cultivees
--ADD CONSTRAINT domaine_surface_especes_cultivees_PK
--primary key (id);

alter table entrepot_domaine_surface_especes_cultivees
add FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
