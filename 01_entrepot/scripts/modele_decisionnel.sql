DROP TABLE if exists MD_traduction;
CREATE TABLE MD_traduction(
	nom_rubrique text, 
	nom_base text,
	traduction_interface text);

insert into MD_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('categorie_objectif','AUCUNE','Z - Zéro tolérance');
insert into MD_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('categorie_objectif','MINIMISER_LES_SYMPTOMES','De - Quelques symptômes acceptés, aucun impact sur le rendement ou la qualité');
insert into MD_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('categorie_objectif','MINIMISER_LES_DOMMAGES','Do - Quelques dommages (impact sur le rendement ou la qualité) acceptés, aucunes pertes économiques');
insert into MD_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('categorie_objectif','MINIMISER_LES_PERTES','Pe - Des pertes économiques limitées peuvent être acceptées');
insert into MD_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('categorie_objectif','AUTRE','Autre');


-- entrepot_modele_decisionnel : les generalites du modele decisionnel
DROP TABLE IF EXISTS entrepot_modele_decisionnel CASCADE;
CREATE TABLE entrepot_modele_decisionnel AS
select 
mm.topiaid id,
mm.category categorie,
mm.mainchanges changements_principaux,
mm.changereason changements_raisons,
mm.mainchangesfromplanned changements_principaux_depuisprevu,
mm.changereasonfromplanned changements_raisons_depuisprevu,
sdc.id sdc_id
from managementmode mm
join entrepot_sdc sdc on sdc.id = mm.growingsystem ;

DO $$
BEGIN
    BEGIN
		alter table entrepot_modele_decisionnel
		add constraint modele_decisionnel_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_modele_decisionnel
ADD FOREIGN KEY (sdc_id) REFERENCES entrepot_sdc(id);

-- entrepot_modele_decisionnel_maitrise : les sections de maitrises de rubrique (maladies, ravageurs ...)
DROP TABLE IF EXISTS entrepot_modele_decisionnel_maitrise CASCADE;
CREATE TABLE entrepot_modele_decisionnel_maitrise AS
WITH groupe_cible as (select distinct 
	code_groupe_cible_maa,
	groupe_cible_maa ,
	cible_edi_ref_code
	from refciblesagrosystgroupesciblesmaa 
	where active = true 
	and groupe_cible_maa not in ('Cicadelles cercopides et psylles','Maladies des taches foliaires') -- on retire les doublons de code 38 'Cicadelles cercopides et psylles' puisque ce nom est utilisé par le 37 , et le 82 puisqu'il y a deux orthographes  
  )
select 
sec.topiaid id,
sec.sectiontype type_rubrique,
case 
	when refcible.groupe_cible_maa is not null then refcible.groupe_cible_maa
	when refcible2.groupe_cible_maa is not null then refcible2.groupe_cible_maa
end libelle_groupe_cible_maa,
sec.codegroupeciblemaa as code_groupe_cible_maa,
case 
	when sec.bioagressor like '%RefNuisibleEDI%' then refnui.reference_label
	when sec.bioagressor like '%RefAdventice%' then refadv.adventice
end bioagresseur_considere,
trad.traduction_interface categorie_objectif,
sec.agronomicobjective objectif_agronomique,
sec.expectedresult resultat_attendu,
sec.categorystrategy categorie_strategie, 
sec.damagetype maitrise_dommage_physique_type_dommage,
md.id modele_decisionnel_id
from section sec
join entrepot_modele_decisionnel md on md.id = sec.managementmode 
left JOIN refadventice refadv on sec.bioagressor = refadv.topiaid 
left JOIN refnuisibleedi refnui on sec.bioagressor = refnui.topiaid
left join groupe_cible refcible on case 
	when sec.bioagressor like '%RefAdventice%' then (refadv.identifiant = refcible.cible_edi_ref_code) -- quand c'est une adventice, la colonne codegroupeciblemaa de section n'est pas remplie. on joint donc refgrpcible seulement avec l'ID d'adventice
	when sec.bioagressor like '%RefNuisibleEDI%' then (refnui.reference_code = refcible.cible_edi_ref_code and sec.codegroupeciblemaa = refcible.code_groupe_cible_maa)
end
left join (select distinct code_groupe_cible_maa,groupe_cible_maa from groupe_cible) refcible2 on case 
	when sec.bioagressor is null then sec.codegroupeciblemaa = refcible2.code_groupe_cible_maa -- quand le bioagresseur n'est pas précisé, la jointure se fait avec seulement avec le code groupe cible.
end
left join MD_traduction trad on trad.nom_base = sec.categoryobjective;

DO $$
BEGIN
    BEGIN
		alter table entrepot_modele_decisionnel_maitrise
		add constraint modele_decisionnel_maitrise_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_modele_decisionnel_maitrise
ADD FOREIGN KEY (modele_decisionnel_id) REFERENCES entrepot_modele_decisionnel(id);

-- entrepot_modeles_decisionnels_strategies : au sein d'une meme rubrique, il peut y avoir differentes strategies = leviers
DROP TABLE IF EXISTS entrepot_modele_decisionnel_strategie CASCADE;
CREATE TABLE entrepot_modele_decisionnel_strategie AS
select 
s.topiaid id,
reflevier.topiaid levier_id,
-- reflevier.lever levier,
-- reflevier.strategytype type_strategie,
s.explanation explication,
-- s.croppingplanmanagmentname, -- ne sait pas a quoi correspond
mdm.id modele_decisionnel_maitrise_id
from strategy s
join entrepot_modele_decisionnel_maitrise mdm on mdm.id = s."section"
join refstrategylever reflevier on s.refstrategylever = reflevier.topiaid ;

DO $$
BEGIN
    BEGIN
		alter table entrepot_modele_decisionnel_strategie
		add constraint modele_decisionnel_strategie_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_modele_decisionnel_strategie
ADD FOREIGN KEY (modele_decisionnel_maitrise_id) REFERENCES entrepot_modele_decisionnel_maitrise(id);

-- entrepot_modeles_decisionnels_strategies_cultures : pour un meme levier, plusieurs cultures peuvent etre associees
DROP TABLE IF EXISTS entrepot_modele_decisionnel_strategie_culture;
CREATE TABLE entrepot_modele_decisionnel_strategie_culture AS
select 
cs.strategy modele_decisionnel_strategie_id,
cs.crops culture_id
from crops_strategy cs  
join entrepot_modele_decisionnel_strategie mds on mds.id = cs.strategy;

alter table entrepot_modele_decisionnel_strategie_culture
ADD FOREIGN KEY (modele_decisionnel_strategie_id) REFERENCES entrepot_modele_decisionnel_strategie(id);

alter table entrepot_modele_decisionnel_strategie_culture
ADD FOREIGN KEY (culture_id) REFERENCES entrepot_culture(id);

DO $$
BEGIN
    BEGIN
		alter table entrepot_modele_decisionnel_strategie_culture
		add constraint modele_decisionnel_strategie_culture_PK
		PRIMARY KEY (modele_decisionnel_strategie_id,culture_id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
