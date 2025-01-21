DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_generalites CASCADE;
CREATE TABLE entrepot_bilan_campagne_sdc_generalites AS
select 
rgs.topiaid id,
rgs.name nom,
rgs.code code,
d.campaign campagne,
rgs.author auteur,
gs.sector filiere_sdc,
gp.type type_dispositif,
rgs_sect.filiere_bcsdc,
-- faits marquants
rgs.highlightsevolutions principales_evolutions_depuis_pz0,
rgs.highlightsmeasures mesure_specifique_annee,
rgs.highlightsperformances faits_marquants_conduiteculture_performancetechnique,
rgs.highlightsteachings enseignements_amelioration_sdc,
rgs.iftestimationmethod methode_estimation_IFT_declares,
case 
	when rgs.arbochemicalfungicideift is not null then rgs.arbochemicalfungicideift
	when rgs.vitidiseasechemicalfungicideift  is not null then rgs.vitidiseasechemicalfungicideift 
end perenne_ift_fongicide_chimique_sdc,
case 
	when rgs.arbobiocontrolfungicideift  is not null then rgs.arbobiocontrolfungicideift
	when rgs.vitidiseasebiocontrolfungicideift is not null then rgs.vitidiseasebiocontrolfungicideift
end perenne_ift_fongicide_biocontrole_sdc,
case 
	when rgs.arbocopperquantity is not null then  rgs.arbocopperquantity 
	when rgs.vitidiseasecopperquantity is not null then rgs.vitidiseasecopperquantity
end perenne_quantite_cuivre_appliquee_kgha,
case 
	when rgs.arbochemicalpestift is not null then rgs.arbochemicalpestift
	when rgs.vitipestchemicalpestift  is not null then rgs.vitipestchemicalpestift
end perenne_ift_ravageur_chimique_sdc,
case 
	when rgs.arbobiocontrolpestift is not null then rgs.arbobiocontrolpestift
	when rgs.vitipestbiocontrolpestift  is not null then rgs.vitipestbiocontrolpestift
end perenne_ift_ravageur_biocontrole_sdc,
case 
	when rgs.arbodiseasequalifier is not null then rgs.arbodiseasequalifier
	when rgs.vitidiseasequalifier is not null then rgs.vitidiseasequalifier
end perenne_niveau_maitrise_maladie,
case 
	when rgs.arbopestqualifier is not null then rgs.arbopestqualifier
	when rgs.vitipestqualifier is not null then rgs.vitipestqualifier
end perenne_niveau_maitrise_ravageur,
gs.topiaid sdc_id,
rgs.reportregional bcregional_associe_id,
mm1.topiaid modele_descisionelassocie_prevu_id,
mm2.topiaid modele_descisionelassocie_obs_id
from reportgrowingsystem rgs
left JOIN reportregional rr on rgs.reportregional = rr.topiaid -- pas toujours de BC regional associe (pareil pour le reseau puisque on l'a depuis BC regional)
left join (select nrg.reportregional, string_agg(distinct n.name,'|') reseau from networks_reportregional nrg -- Quand il y a plusieurs IR pour un meme id de rr, on agrege les noms d'IR sur la meme ligne  
	join network n on nrg.networks = n.topiaid group by nrg.reportregional) nr on nr.reportregional = rr.topiaid
join growingsystem gs on rgs.growingsystem = gs.topiaid 
join growingplan gp on gs.growingplan = gp.topiaid 
join domain d on gp.domain = d.topiaid
left join (select * from managementmode where category = 'PLANNED') mm1 on gs.topiaid = mm1.growingsystem 
left join (select * from managementmode where category = 'OBSERVED') mm2 on gs.topiaid = mm2.growingsystem
join (select owner, string_agg(sectors,'|') filiere_bcsdc from reportgrowingsystem_sectors group by owner) rgs_sect on rgs_sect.owner = rgs.topiaid 
join entrepot_sdc es on es.id = gs.topiaid ;

alter table entrepot_bilan_campagne_sdc_generalites
add constraint bilan_campagne_sdc_generalites_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_generalites
ADD FOREIGN KEY (sdc_id) REFERENCES entrepot_sdc(id);

alter table entrepot_bilan_campagne_sdc_generalites
ADD FOREIGN KEY (bcregional_associe_id) REFERENCES entrepot_bilan_campagne_regional_generalites(id);

alter table entrepot_bilan_campagne_sdc_generalites
ADD FOREIGN KEY (modele_descisionelassocie_prevu_id) REFERENCES entrepot_modele_decisionnel(id);

alter table entrepot_bilan_campagne_sdc_generalites
ADD FOREIGN KEY (modele_descisionelassocie_obs_id) REFERENCES entrepot_modele_decisionnel(id);

--------------------------------------------------------------------
-- ASSOLEE : Maitrise agresseurs = ravageurs, maladies et adventices
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_assolee_agresseur;
CREATE TABLE entrepot_bilan_campagne_sdc_assolee_agresseur AS
select 
pm.topiaid id,
'adventice' type_bioagresseur,
null groupe_cible,
refadv.adventice bioagresseur,
trad1.traduction_interface echelle_pression,
pm.pressurescaleint EXPE_echelle_pression_marhorti,
pm.pressurefarmercomment pression_commentaire_agri,
trad2.traduction_interface echelle_maitrise,
pm.masterscaleint EXPE_echelle_maitrise_marhorti,
pm.qualifier maitrise_qualifiant,
pm.resultfarmercomment maitrise_commentaire_agri,
cm.iftmain IFT_principal,
null IFT_autre_ravageur,
null EXPE_IFT_hors_biocontrol,
cm.advisercomments commentaire_conseiller_experi,
ebcsg.id bilan_campagne_sdc_generalites_id
from pestmaster pm
join croppestmaster cm on cm.topiaid = pm.croppestmaster 
join refadventice refadv on pm.agressor = refadv.topiaid
-- traductions des libelles
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'echelle pression adventice assolee') trad1 on pm.pressurescale = trad1.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'echelle de maitrise adventice assolee') trad2 on pm.masterscale = trad2.nom_base
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id = cm.cropadventicemasterreportgrowingsystem
union
select 
pm.topiaid id,
case 
	when cm.cropdiseasemasterreportgrowingsystem is not null then 'maladie'
	when cm.croppestmasterreportgrowingsystem is not null then 'ravageur'
end type_bioagresseur,
refgrpcible.groupe_cible_maa groupe_cible,
refnui.reference_label bioagresseur,
trad1.traduction_interface echelle_pression,
pm.pressurescaleint EXPE_echelle_pression_marhorti,
pm.pressurefarmercomment pression_commentaire_agri,
trad2.traduction_interface echelle_maitrise,
pm.masterscaleint EXPE_echelle_maitrise_marhorti,
pm.qualifier maitrise_qualifiant,
pm.resultfarmercomment maitrise_commentaire_agri,
cm.iftmain IFT_principal,
cm.iftother IFT_autre_ravageur,
cm.ifthorsbiocontrole EXPE_IFT_hors_biocontrol,
cm.advisercomments commentaire_conseiller_experi,
ebcsg.id bilan_campagne_sdc_generalites_id
from pestmaster pm
join croppestmaster cm on cm.topiaid = pm.croppestmaster 
join refnuisibleedi refnui on pm.agressor = refnui.topiaid
left join (select distinct code_groupe_cible_maa,groupe_cible_maa 
			from refciblesagrosystgroupesciblesmaa where active = true 
			and groupe_cible_maa not in ('Cicadelles cercopides et psylles','Maladies des taches foliaires')) refgrpcible -- on retire les doublons de code 38 'Cicadelles cercopides et psylles' puisque ce nom est utilisé par le 37 , et le 82 puisqu'il y a deux orthographes 
		on refgrpcible.code_groupe_cible_maa = pm.codegroupeciblemaa 
-- traductions des libelles
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'echelle de pression maladie ravageur assolee') trad1 on pm.pressurescale = trad1.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'echelle de maitrise maladie ravageur assolee') trad2 on pm.masterscale = trad2.nom_base
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id in (cm.croppestmasterreportgrowingsystem, cm.cropdiseasemasterreportgrowingsystem)
;


alter table entrepot_bilan_campagne_sdc_assolee_agresseur
add constraint bilan_campagne_sdc_agresseur_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_assolee_agresseur
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);


--------------------------------------------------------------------
-- ASSOLEE : Maitrise de la verse
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_assolee_verse;
CREATE TABLE entrepot_bilan_campagne_sdc_assolee_verse AS
select 
vm.topiaid id ,
trad1.traduction_interface echelle_risque,
vm.riskfarmercomment risque_commentaire_agri ,
trad2.traduction_interface echelle_maitrise,
vm.qualifier maitrise_qualifiant, 
vm.resultfarmercomment resultats_commentaire_agri , 
vm.iftmain IFT_regulateur , 
vm.advisercomments commentaire_conseiller,
vm.reportgrowingsystem bilan_campagne_sdc_generalites_id
from versemaster vm
-- traductions des libelles
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'echelle de risque verse') trad1 on vm.riskscale = trad1.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'echelle de maitrise verse') trad2 on vm.masterscale = trad2.nom_base 
join entrepot_bilan_campagne_sdc_generalites e on e.id = vm.reportgrowingsystem;

alter table entrepot_bilan_campagne_sdc_assolee_verse
add constraint bilan_campagne_sdc_verse_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_assolee_verse
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);


--------------------------------------------------------------------
-- TOUTES fillieres : Rendement
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_rendement;
CREATE TABLE entrepot_bilan_campagne_sdc_rendement AS
select 
coalesce(yl.topiaid,'') ||''|| coalesce(yi.topiaid,'') id,
case 
	when yl.yieldobjective is not null then trad1.traduction_interface
	when yl.yieldobjectiveint is not null then trad2.traduction_interface
end objectif_rendement_atteint,
yl.cause1 as rendement_cause1,
yl.cause2 as rendement_cause2,
yl.cause3 as rendement_cause3,
yl.comment as qualite_commentaire,
yi.comment as rendementqualite_commentaire_global,
rgs.topiaid as bilan_campagne_sdc_generalites_id
from reportgrowingsystem rgs
join growingsystem gs on gs.topiaid = rgs.growingsystem
left join yieldinfo yi on rgs.topiaid = yi.reportgrowingsystem
left join yieldloss yl on rgs.topiaid = yl.reportgrowingsystem
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id = rgs.topiaid
-- traductions des libelles
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'rendement echelle objectif') trad1 on yl.yieldobjective = trad1.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'rendement echelle objectif expe') trad2 on yl.yieldobjectiveint::text = trad1.nom_base 
where gs.sector <> 'VITICULTURE' and (yi.topiaid is not null or yl.topiaid is not null)
union 
select 
'fr.inra.agrosyst.api.entities.report.YieldLoss_' || SUBSTR(rgs.topiaid,58), -- les infos de la viti sont dans rgs mais sont les memes donc on attribut un id
trad1.traduction_interface as objectif_rendement_atteint,
rgs.vitilosscause1 as rendement_cause1,
rgs.vitilosscause2 as  rendement_cause2,
rgs.vitilosscause3 as  rendement_cause3,
rgs.vitiyieldquality as qualite_commentaire,
yi.comment rendementqualite_commentaire_global,
rgs.topiaid bilan_campagne_sdc_generalites_id
from reportgrowingsystem rgs
join growingsystem gs on gs.topiaid = rgs.growingsystem
left join yieldinfo yi on rgs.topiaid = yi.reportgrowingsystem and yi.sector = 'VITICULTURE'
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id = rgs.topiaid
-- traductions des libelles
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'rendement echelle objectif') trad1 on rgs.vitiyieldobjective = trad1.nom_base 
where gs.sector = 'VITICULTURE'
;

alter table entrepot_bilan_campagne_sdc_rendement
add constraint bilan_campagne_sdc_rendement_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_rendement
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);

--------------------------------------------------------------------
-- TOUTES fillieres : Alimentation hydrique et minerale
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_alimentation;
CREATE TABLE entrepot_bilan_campagne_sdc_alimentation AS
select 
fm.topiaid id,
trad1.traduction_interface irrigation ,
trad2.traduction_interface stress_hydrique ,
trad3.traduction_interface stress_azote ,
fm.mineralfood alimentation_minerale_hors_azote ,
trad4.traduction_interface stress_temperature_rayonnement ,
fm.comment commentaire,
ebcsg.id bilan_campagne_sdc_generalites_id
from foodmaster fm 
-- traductions des libelles
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'irrigation') trad1 on fm.foodirrigation = trad1.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'stress hydrique mineral temperature') trad2 on fm.hydriquestress = trad2.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'stress hydrique mineral temperature') trad3 on fm.azotestress = trad3.nom_base 
left join (select * from bilan_campagne_sdc_traduction where nom_rubrique = 'stress hydrique mineral temperature') trad4 on fm.tempstress = trad4.nom_base
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id = fm.foodmasterreportgrowingsystem ;

alter table entrepot_bilan_campagne_sdc_alimentation
add constraint bilan_campagne_sdc_alimentation_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_alimentation
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);
