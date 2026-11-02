drop table if exists entrepot_recolte_rendement_prix cascade;
CREATE TABLE entrepot_recolte_rendement_prix(
    id character varying(255),
	libelle_culture text,
    commercialisation_pct int4,
    autoconsommation_pct int4,
    nonvalorisation_pct int4,
    rendement_min float8,
    rendement_max float8, 
    rendement_moy float8,
    rendement_median float8,
    rendement_unite text,
    destination_id character varying(255),
    destination text,
    prixreel float8,
    prixreel_unite text,
    prixref float8,
    prixref_unite text,
    prixref_campagnes text,
    composant_culture_code text,
    action_id character varying(255)
);

INSERT INTO entrepot_recolte_rendement_prix(id,libelle_culture,commercialisation_pct,autoconsommation_pct,nonvalorisation_pct,
    rendement_min,rendement_max,rendement_moy,rendement_median,rendement_unite,destination_id, destination,
    prixreel,prixreel_unite,composant_culture_code,action_id)
SELECT 
hav.topiaid id ,
refesp.libelle_espece_botanique ||','|| COALESCE(refesp.libelle_qualifiant_aee) ||','|| COALESCE(refesp.libelle_type_saisonnier_aee,'') as libelle_culture,
hav.salespercent commercialisation_pct,
hav.selfconsumedpersent autoconsommation_pct,
hav.novalorisationpercent nonvalorisation_pct,
hav.yealdmin rendement_min,
hav.yealdmax rendement_max, 
hav.yealdaverage rendement_moy,
hav.yealdmedian rendement_median,
hav.yealdunit rendement_unite,
hav.destination as destination_id,
refdest.destination,
hp.price prixreel,
hp.priceunit prixreel_unite,
hav.speciescode composant_culture_code,
hav.harvestingaction action_id
from harvestingactionvalorisation hav
join refdestination refdest on refdest.topiaid = hav.destination
join harvestingprice hp on hp.harvestingactionvalorisation = hav.topiaid 
-- avoir le libelle de l'esp
join croppingplanspecies cps on cps.code = hav.speciescode 
join croppingplanentry cpe on cpe.topiaid = cps.croppingplanentry and cpe.domain = hp.domain -- selectionne la bonne annee du domaine parmi tous les especes codes
join refespece refesp on refesp.topiaid = cps.species 
-- filtrer les actions qui sont dans les tables entrepot_action_xx
left join entrepot_action_realise ear on ear.id = hav.harvestingaction
left join entrepot_action_synthetise eas on eas.id = hav.harvestingaction 
where ear.id is not null or eas.id is not null
;

CREATE INDEX entrepot_recolte_rendement_prix_idx on entrepot_recolte_rendement_prix(id);

-- Attribution des prix de reference 
/*
L'attribution des prix de reference est selon la clé : l'esp , le qualifiant aee , la destination , bio ou pas, période de récolte
Si aucun prix de reference n'existe dans le référentiel pour cette période de récolte, alors on regarde aux années précedantes sans modifier les mois et semaines de recolte.
Dans le referentiel, certains prix de reference sont attribués à tous mois et semaines confondu marketingPeriod=-1 et marketingperioddecade=NULL , 
Ce type prix est prioritaire avant de changer d'année quand il n'y a pas de prix pour la période mois/semaine . 

=> Creation table prixref_selection qui pour une cle de prix, selectione tous les prix dans le referentiel ayant la bonne période (mois et semaines) et toutes périodes pour chaque campagne
On ne selectionne que les prix de references différents de 0 (=NA), de campagne differentes de 0, les prix actifs

Un score_campagne est attribué aux prix de reference selon la campagne. 0, le min est le meilleur : correspond à la bonne campagne
Quand la période de recolte s'étale sur deux ans ou bien concerne un synthetise pluriannuel, un score_campagne est aussi attibué par rapport au l'année de debut de recolte
ex : une recolte de 2014 - 2016 , les prix selectionnés en 2014 auront un score de 0 et les prix en 2016 un score de -2
Lors de la selection finale des prix, on prendra le prix avec le score_campagne minimum + ceux qui ont un score_campagne de min + nb années entre debut et fin recolte

Meme raisonnement pour les unités : un score_unit est attribué afin de prioriser les prix de reference de meme unite que le prix reel.
score_unit = 0 : l'unité est la meme que le prix reel
 */

/*
Creation table periode_recolte pour isoler le contexte (la cle) du prix réel 
Il faut : 
- l'esp : refespece depuis croppingplantspecies
- le qualifiant aee de l'esp 
- la destination de la recolte : refdestination depuis hav
- bio ou pas : growingsystem
- epoque de recolte (campagne, mois, semaine (debut et fin)) : hav

Il y a des recoltes associes a des realises qui n'ont pas de sdc associes donc pas de connaissance si c'est un type bio ou pas. 
Pour ces prix de references, on va moyenner les prix bio et sans bio quand il y a les deux. 
Pour ces cas là, la colonne type_agri = NULL
 */


-- 1) isoler les informations de la recolte
drop table if exists recolte_context cascade;

create temporary table recolte_context as
select 
hav.topiaid topiaid_hav,
refesp.libelle_espece_botanique esp_libelle,
refesp.code_espece_botanique,
refesp.code_qualifiant_aee qualifiant_aee,
refdest.code_destination_a ,
case 
	when refta.reference_label = 'Agriculture biologique' then TRUE
	when refta.reference_label <> 'Agriculture biologique' then false
	when refta.reference_label is null then NULL
end type_agri,
hav.beginmarketingperiod , hav.beginmarketingperioddecade , hav.endingmarketingperiod , hav.endingmarketingperioddecade , hav.beginmarketingperiodcampaign , hav.endingmarketingperiodcampaign ,
hp.priceunit prix_reel_unit -- a garder pour choisir un prix de reference = au prix reel saisi si il y a le choix dans les unités
from harvestingprice hp 
join harvestingactionvalorisation hav on hav.topiaid = hp.harvestingactionvalorisation 
join refdestination refdest on refdest.topiaid = hav.destination 
join croppingplanspecies cps on cps.code = hav.speciescode 
join croppingplanentry cpe on cpe.topiaid = cps.croppingplanentry and cpe.domain = hp.domain -- selectionne la bonne annee du domaine parmi tous les especes codes
join refespece refesp on refesp.topiaid = cps.species 
left join practicedsystem ps on ps.topiaid = hp.practicedsystem -- pour les synthetises
left join zone z on z.topiaid = hp.zone -- pour les realises
left join plot p on p.topiaid = z.plot
left join growingsystem gs on gs.topiaid = ps.growingsystem or p.growingsystem = gs.topiaid  -- left join pour garder les realises qui n'ont pas de parcelles rattachees
left join reftypeagriculture refta on refta.topiaid = gs.typeagriculture ;

CREATE INDEX recolte_context_idx on recolte_context(topiaid_hav);
CREATE INDEX recolte_context_idx2 on recolte_context(beginMarketingPeriodDecade);
CREATE INDEX recolte_context_idx3 on recolte_context(endingMarketingPeriodDecade);
CREATE INDEX recolte_context_idx4 on recolte_context(beginMarketingPeriod);

-- 2) recuperer tous les prix de références qui correspondent à la bonne période + année = ou antérieure à la récolte.
-- dans le cas où la récolte couvre plusieurs decades, la moyenne est faite pour attribuer 1 prix de référence


drop table if exists prixref_selection cascade;

create table prixref_selection(
topiaid_hav character varying(255),
esp_libelle text,
code_espece_botanique text,
qualifiant_aee text,
code_destination_a text,
type_agri bool,
beginmarketingperiodcampaign int,
endingmarketingperiodcampaign int,
beginmarketingperiod int,
endingmarketingperiod int,
beginmarketingperioddecade int,
endingmarketingperioddecade int,
prix_ref float8,
prix_ref_unit text,
campaign int,
marketingperiod int,
marketingperioddecade int,
organic bool,
score_unit int,
score_campagne int); 


insert into prixref_selection (topiaid_hav, esp_libelle, code_espece_botanique, qualifiant_aee, code_destination_a, type_agri,
beginmarketingperiodcampaign, endingmarketingperiodcampaign, beginmarketingperiod, endingmarketingperiod, beginmarketingperioddecade, endingmarketingperioddecade,
prix_ref, prix_ref_unit, campaign, marketingperiod, marketingperioddecade, organic, score_unit,score_campagne)
with jointure_referentiel as (
	select rc.topiaid_hav ,
	rc.esp_libelle,rc.code_espece_botanique,rc.qualifiant_aee,rc.code_destination_a,rc.type_agri,
	rc.beginmarketingperiodcampaign,rc.endingmarketingperiodcampaign,rc.beginmarketingperiod, rc.endingmarketingperiod , rc.beginmarketingperioddecade , rc.endingmarketingperioddecade ,
	r.price, r.priceunit,
	r.campaign ref_campagne, r.marketingperiod ref_period, r.marketingperioddecade ref_decade, r.organic ref_organic,
	case
		when r.priceunit = rc.prix_reel_unit then 0
		when r.priceunit <> rc.prix_reel_unit then 1
	end score_unit
	from (select * from recolte_context ) rc -- where beginmarketingperiod = endingmarketingperiod) rc
	join (select * from refharvestingprice where campaign <> 0 and price <> 0 and active = TRUE) r on 
									(rc.code_espece_botanique = r.code_espece_botanique 
									and rc.qualifiant_aee = r.code_qualifiant_aee 
									and case
										when type_agri is not null then rc.code_destination_a=r.code_destination_a and rc.type_agri = r.organic
										when type_agri is null then rc.code_destination_a=r.code_destination_a
										end)
)
-- cas 1 : periode de recolte sur un meme mois pour une même année ou pour synthetisé pluriannuel
select *, beginmarketingperiodcampaign - ref_campagne as score_campagne
from jointure_referentiel
where (beginmarketingperiod = endingmarketingperiod)
and (ref_campagne <= endingmarketingperiodcampaign) and 
((ref_period = beginMarketingPeriod and ref_decade >= beginMarketingPeriodDecade and ref_decade <= endingMarketingPeriodDecade)
or ref_period = -1)
union
-- cas 2 : periode de recolte sur 2 ou plus de mois d'une meme année ou pour synthetises pluriannuels
select *, beginmarketingperiodcampaign - ref_campagne as score_campagne
from jointure_referentiel
where (beginmarketingperiod < endingmarketingperiod and beginmarketingperiodcampaign <> endingmarketingperiodcampaign -1)
and (ref_campagne <= endingmarketingperiodcampaign) and
((ref_period = beginMarketingPeriod and ref_decade >= beginMarketingPeriodDecade) -- semaines du mois du debut
or (ref_period = endingMarketingPeriod and ref_decade <= endingMarketingPeriodDecade) -- semaines du mois de fin
or (ref_period > beginMarketingPeriod and ref_period < endingMarketingPeriod) -- mois du milieu si il y a 
or ref_period=-1)
union 
--- CAS 3 : une recolte qui s'étale sur deux ans (en hiver) : que quand annee de fin = annee debut +1 ET que le mois de debut > mois de fin 
select *,
case 
	when ref_period = -1 then beginmarketingperiodcampaign - ref_campagne
	when ref_period >= beginmarketingperiod then beginmarketingperiodcampaign - ref_campagne
	when ref_period <= endingmarketingperiod then endingmarketingperiodcampaign - ref_campagne
end score_campagne
from jointure_referentiel
where (beginmarketingperiod > endingmarketingperiod and beginmarketingperiodcampaign = endingmarketingperiodcampaign -1)
and 
(ref_campagne <= endingmarketingperiodcampaign) and 
((ref_period = beginMarketingPeriod and ref_decade >= beginMarketingPeriodDecade) -- semaines du mois du debut
or (ref_period = endingMarketingPeriod and ref_decade <= endingMarketingPeriodDecade) -- semaines du mois de fin
or ref_period > beginMarketingPeriod -- semaines des mois de milieu
or ref_period < endingMarketingPeriod
or ref_period = -1);


/* Choix final des prix de reférence : 
1) Pour les unités : Selection du minimum de score_unit pour chaque topiaid_hav dans prixref_selection, puis inner join à prixref_selection (=autojointure) selon topiaid_hav ET score_unit
inner join (select topiaid_hav topiaid_hav3, min(score_unit) min_score_unit from prixref_selection group by topiaid_hav3) selec3 
	on selec3.topiaid_hav3 = ps.topiaid_hav and selec3.min_score_unit = ps.score_unit
	
Pour le cas où aucun de prix de reference pour la même unité que celle du prix reel n'existe, mais que plusieurs autres unités sont disponibles (plusieurs score_unit =1),
on prend la premiere ligne de prix ref. => grace à rownumber() attribués selon les topiaid_hav puis where rownb = 1

2) Pour les prix : meme raisonnement autojointure mais avec le minimum de score_campagne
Pour les recoltes sur plusieurs années : on joint le minimum de score_campagne pour chaque topiaid_hav. 
Puis on selectionne (avec where) uniquement les campagnes où score_campagne <= min_score_campagne + nb années entre debut et fin recolte
*/

update entrepot_recolte_rendement_prix e SET
prixref = pf.prix_ref, 
prixref_unite = pf.prix_ref_unit, 
prixref_campagnes = pf.campaign 
from (select 
	topiaid_hav, AVG(ps.prix_ref) prix_ref, ps.prix_ref_unit, ps.campaign,
	row_number() OVER (PARTITION BY ps.topiaid_hav) as rownb -- attribution du numero de ligne selon le topiaid_hp : pour les cas où il y a plusieurs unités mais aucune n'est celle du prix reel
	from prixref_selection ps
	inner join (select topiaid_hav topiaid_hav2, min(score_campagne) min_score_campagne 
						from prixref_selection ps group by topiaid_hav) selec2 on selec2.topiaid_hav2 = ps.topiaid_hav and selec2.min_score_campagne = ps.score_campagne 
	inner join (select topiaid_hav topiaid_hav3, min(score_unit) min_score_unit
						from prixref_selection ps group by topiaid_hav) selec3 on selec3.topiaid_hav3 = ps.topiaid_hav and selec3.min_score_unit = ps.score_unit
	group by topiaid_hav,campaign,prix_ref_unit) pf
where (pf.rownb = 1 or pf.rownb is null)
and pf.topiaid_hav = e.id
;

-- Contraintes 
DO $$
BEGIN
    BEGIN
		alter table entrepot_recolte_rendement_prix
		add constraint rendement_prix_recolte_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
