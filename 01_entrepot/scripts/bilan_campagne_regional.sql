--entrepot_bilan_campagne_regional_generalite : generalites du bilan regional
DROP TABLE IF EXISTS entrepot_bilan_campagne_regional_generalites CASCADE;
CREATE TABLE entrepot_bilan_campagne_regional_generalites AS
WITH reseaux_bcr as (select 
    nrg.reportregional,
    string_agg(distinct n.name,'|') reseau -- Quand il y a plusieurs IR pour un meme id de rr, on agrege les noms d'IR sur la meme ligne  
    from networks_reportregional nrg 
	join network n on nrg.networks = n.topiaid group by nrg.reportregional
  ),
  secteurs_bcr as (select
  owner,
  string_agg(rrs.sectors,'|') as sectors
  from reportregional_sectors rrs group by owner
  ),
  species_bcr as (select
  owner,
  string_agg(rrss.sectorspecies,'|') as sectorspecies
  from reportregional_sectorspecies rrss group by owner
  ) 
select 
rr.topiaid as id,
rr.code ,
rr."name" as nom,
rr.campaign campagne,
rr.author auteur,
r.reseau reseau,
sect.sectors secteurs,
sp.sectorspecies arbo_esp,
rr.highlights faits_marquants,
rr.rainfallmarchjune pluvio_marsjuin,
rr.rainydaysmarchjune jourspluie_marsjuin,
rr.rainfalljulyoctober pluvio_juiloct,
rr.primarycontaminations INOKI_nb_contaminationprimaire,
rr.numberofdayswithprimarycontaminations INOKI_nbjours_contamitationprimaire,
rr.secondarycontaminations RIMpro_nb_contaminationsecondaire,
rr.rimsum RIMpro_sommeRIM
from reportregional rr
join reseaux_bcr r on r.reportregional = rr.topiaid
join secteurs_bcr sect on sect.owner = rr.topiaid
left join species_bcr sp on sp.owner = rr.topiaid;

DO $$
BEGIN
    BEGIN
    alter table entrepot_bilan_campagne_regional_generalites
    add constraint bilan_campagne_regional_generalites_PK
    PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

-- entrepot_bilan_campagne_regional_pressionbioagresseur : pressions des bioagresseurs. 
-- !!! Si plusieurs bioagresseurs sont saisis pour une meme observation, les noms des bioagresseurs sont concatenes
DROP TABLE IF EXISTS entrepot_bilan_campagne_regional_pressionbioagresseur CASCADE;
CREATE TABLE entrepot_bilan_campagne_regional_pressionbioagresseur AS
WITH groupe_cible as (select distinct 
	code_groupe_cible_maa,
	groupe_cible_maa 
	from refciblesagrosystgroupesciblesmaa 
	where active = true 
	and groupe_cible_maa not in ('Cicadelles, cercopides et psylles','Maladies des taches foliaires') -- on retire les doublons de code 38 'Cicadelles cercopides et psylles' puisque ce nom est utilisé par le 37 , et le 82 puisqu'il y a deux orthographes  
  ),
  maladies as (select 
  	ap.pestpressure ,
  	string_agg(refnui.reference_label, '|') nom_maladie_ravageur
  	from agressors_pestpressure ap
  	join refnuisibleedi refnui on ap.agressors = refnui.topiaid 
  	group by pestpressure)
select
pp.topiaid as id,
case 
	when pp.diseasepressurereportregional like '%ReportRegional%' then 'maladies'
	when pp.pestpressurereportregional like '%ReportRegional%' then 'ravageurs'
end type_pression,
refgrp.groupe_cible_maa,
m.nom_maladie_ravageur,
pp.crops as culture_concernee,
pp.pressurescale as pression_annee,
pp.pressureevolution as pression_evolution,
pp.comment as commentaires,
bcrg.id as bilan_campagne_regional_id
FROM pestpressure pp
JOIN entrepot_bilan_campagne_regional_generalites bcrg on bcrg.id = pp.diseasepressurereportregional or bcrg.id = pp.pestpressurereportregional 
LEFT JOIN groupe_cible refgrp on pp.codegroupeciblemaa = refgrp.code_groupe_cible_maa
left join maladies m on pp.topiaid = m.pestpressure;

DO $$
BEGIN
    BEGIN
    alter table entrepot_bilan_campagne_regional_pressionbioagresseur
    add constraint bilan_campagne_regional_pressionbioagresseur_PK
    PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_bilan_campagne_regional_pressionbioagresseur
ADD FOREIGN KEY (bilan_campagne_regional_id) REFERENCES entrepot_bilan_campagne_regional_generalites(id);
