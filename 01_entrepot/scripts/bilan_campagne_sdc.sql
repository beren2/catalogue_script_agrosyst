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
rgs.iftestimationmethod methode_estimation_IFT_declares,
rgs.highlightsevolutions principales_evolutions_depuis_pz0,
rgs.highlightsmeasures mesure_specifique_annee,
rgs.highlightsperformances faits_marquants_conduiteculture_performancetechnique,
rgs.highlightsteachings enseignements_amelioration_sdc,
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

-- Creation d'une table de traduction entre l'information en base et l'interface
DROP TABLE IF EXISTS traductions_bilan_campagne_sdc;
CREATE TABLE traductions_bilan_campagne_sdc(
	nom_rubrique text, 
	nom_base text,
	traduction_interface text);
	
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur','NONE','Nulle (absence)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur','LOW','Faible (un peu mais pas d''impact)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur','MODERATE','Moyenne (impact sur le rendement possible)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur','HIGH','Forte (impact certain sur le rendement et la marge)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','NONE','Aucun symptôme');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','LOW','Symptômes sans effet sur le rendement ou la qualité');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','MODERATE','Symptômes avec effet très limité sur le rendement et la qualité');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','HIGH','Pertes économiques dues à la maladie');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','NONE','Aucun symptome ou presence');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','LOW','Symptomes sans effet sur le rendement');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','MODERATE','Rendement un peu affecté sans effet sur la marge de la culture');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','HIGH','Pertes économiques sur la culture');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','NONE','Aucun symptôme');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','LOW','Symptômes sans effet sur le rendement ou la qualité');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','MODERATE','Symptômes avec effet très limité sur le rendement et la qualité');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','HIGH','Pertes économiques dues à des dégâts sur fruits, feuilles, ou arbres');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','ZERO','0% de ceps touchés, 0% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_0_TO_10_2_INTENSITY','0 à 10 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_10_TO_35_2_INTENSITY','10 à 35 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_35_TO_70_2_INTENSITY','35 à 70 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_2_INTENSITY','70 à 100 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_35_TO_70_2_TO_5_INTENSITY','35 à 70 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_2_TO_5_INTENSITY','70 à 100 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_5_TO_15_INTENSITY','70 à 100 % de ceps touchés, 5 à 15% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_15_TO_25_INTENSITY','70 à 100 % de ceps touchés, 15 à 25% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_25_INTENSITY','70 à 100 % de ceps touchés, > 25% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','ZERO','0% de ceps touchés, 0% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_0_TO_10_2_INTENSITY','0 à 10 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_10_TO_35_2_INTENSITY','10 à 35 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_35_TO_70_2_INTENSITY','35 à 70 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_2_INTENSITY','70 à 100 % de ceps touchés, moins de 2% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_35_TO_70_2_TO_5_INTENSITY','35 à 70 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_2_TO_5_INTENSITY','70 à 100 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_5_TO_15_INTENSITY','70 à 100 % de ceps touchés, 5 à 15% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_15_TO_25_INTENSITY','70 à 100 % de ceps touchés, 15 à 25% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_25_INTENSITY','70 à 100 % de ceps touchés, > 25% d intensité d attaque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','NONE','pas de dégâts');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','LOW','attaque faible');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','MODERATE','attaque moyenne');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','HIGH','attaque forte');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','NONE','pas de dégâts');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','LOW','attaque faible');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','MODERATE','attaque moyenne');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','HIGH','attaque forte');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','NONE','sol nu');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','LOW','sol globalement nu avec toutefois quelques taches, sans gravité ni concurrence hydrique');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','MODERATE','enherbement sans concurrence hydrique');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','HIGH','enherbement generalise (voulu ou accidentel) avec baisse de vigeur et rendement');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','NON_IRRIGABLE','Non irrigable');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','NOT_IRRIGATED_CROP','Irrigable, culture non irriguée');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','IRRIGATED_CROP_LIMITED_QUANTITY','Culture irriguée, quantité limitée');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','IRRIGATED_CROP','Culture irriguée');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','NO_STRESS','Pas de stress');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','STRESS_NO_IMPACT_YIELD','Stress limité sans impact sur le rendement');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','STRESS_NO_IMPACT_PROFIT','Stress limité sans impact sur la marge');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','STRESS_IMPACT_YIELD_PROFIT','Stress impactant le rendement et la marge');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','NONE','Nulle (absence)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','LOW','Faible (presence sporadique)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','MODERATE','Moyenne (premiers ronds)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','HIGH','Forte (concurrence en voie de generalisation)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','NONE','Pas de presence');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','LOW','Presence sans concurrence ni multiplication significative (sous couvert ou sur couvert)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','MODERATE','Presence de premiers ronds de concurrence directe sur ou sous couvert (avec risque de multiplication futur)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','HIGH','Concurrence en voie de generalisation (multication des zones ou "ronds") sous ou sur couvert cultive');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','NONE','Pas de risque');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','LOW','Risque faible (un peu mais pas d''impact)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','MODERATE','Risque moyenne (impact sur le rendement possible)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','HIGH','Risque fort (impact certain sur le rendement et la marge)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','NONE','Pas de verse');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','LOW','Un peu de verse sans effet sur le rendement');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','MODERATE','Verse sans effet sur la marge de la culture');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','HIGH','Verse impactant la performance economique');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise visee adv arboexpe','NONE','Rang nu toute la saison');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise visee adv arboexpe','LOW','Rang nu à certaines periodes');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise visee adv arboexpe','HIGH','Enherbement permanent');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo ferme','NONE','Sol propre toute la saison');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo ferme','LOW','Sol propre à certaines periodes (recolte)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo ferme','MODERATE','Enherbement permanent sans concurrence hydrique');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo ferme','HIGH','Enherbement permanent avec concurrence (eau,vigueur,coloration …)');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','4','LESS_50');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','3','FROM_50_TO_75');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','2','FROM_75_TO_95');
insert into traductions_bilan_campagne_sdc(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','1','MORE_95');

-- Maitrise des ravageurs maladies et adventices
DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_agresseur;
CREATE TABLE entrepot_bilan_campagne_sdc_agresseur AS
select 
pm.topiaid id,
'adventice' type_bioagresseur,
null groupe_cible,
refadv.adventice agresseur,
trad1.traduction_interface echelle_pression,
pm.pressurescaleint EXPE_echelle_pression_marhorti,
pm.pressurefarmercomment pression_commentaire_agri,
pm.masterscale echelle_maitrise,
trad2.traduction_interface echelle_maitrise_libelle_filiere,
pm.masterscaleint EXPE_echelle_maitrise_marhorti,
pm.qualifier maitrise_qualifiant,
pm.resultfarmercomment maitrise_commentaire_agri,
cm.iftmain IFT_principal,
null IFT_autre,
null EXPE_IFT_hors_biocontrol,
cm.advisercomments commentaire_conseiller_experi,
ebcsg.id bilan_campagne_sdc_generalites_id
from pestmaster pm
join croppestmaster cm on cm.topiaid = pm.croppestmaster 
join refadventice refadv on pm.agressor = refadv.topiaid
-- traductions des libelles
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'echelle de pression maladie ravageur') trad1 on pm.pressurescale = trad1.nom_base 
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'echelle de maitrise maladie ravageur assolee') trad2 on pm.masterscale = trad2.nom_base
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
pm.masterscale echelle_maitrise,
trad2.traduction_interface echelle_maitrise_libelle_filiere,
pm.masterscaleint EXPE_echelle_maitrise_marhorti,
pm.qualifier maitrise_qualifiant,
pm.resultfarmercomment maitrise_commentaire_agri,
cm.iftmain IFT_principal,
cm.iftother IFT_autre,
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
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'echelle pression adventice assolee') trad1 on pm.pressurescale = trad1.nom_base 
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'echelle de maitrise adventice assolee') trad2 on pm.masterscale = trad2.nom_base
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id in (cm.croppestmasterreportgrowingsystem, cm.cropdiseasemasterreportgrowingsystem)
;


alter table entrepot_bilan_campagne_sdc_agresseur
add constraint bilan_campagne_sdc_agresseur_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_agresseur
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);


-- Maitrise de la verse
DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_verse;
CREATE TABLE entrepot_bilan_campagne_sdc_verse AS
select 
vm.topiaid id ,
trad1.traduction_interface risque_echelle,
vm.riskfarmercomment risque_commentaire_agri ,
trad2.traduction_interface resultats_echelle_maitrise,
vm.qualifier resultats_qualifiant, 
vm.resultfarmercomment resultats_commentaire_agri , 
vm.iftmain IFT_regulateur , 
vm.advisercomments IFT_commentaire_conseiller,
vm.reportgrowingsystem bilan_campagne_sdc_generalites_id
from versemaster vm
-- traductions des libelles
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'echelle de risque verse') trad1 on vm.riskscale = trad1.nom_base 
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'echelle de maitrise verse') trad2 on vm.masterscale = trad2.nom_base 
join entrepot_bilan_campagne_sdc_generalites e on e.id = vm.reportgrowingsystem;

alter table entrepot_bilan_campagne_sdc_verse
add constraint bilan_campagne_sdc_verse_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_verse
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);

-- Rendement et qualité
DROP TABLE IF EXISTS entrepot_bilan_campagne_sdc_rendement;
CREATE TABLE entrepot_bilan_campagne_sdc_rendement AS
select 
yl.topiaid ||''|| coalesce(yi.topiaid,'') id,
yl.yieldobjective objectif_rendement,
yl.yieldobjectiveint objectif_rendement_echelleint,
yl.cause1 rendement_cause1,
yl.cause2 rendement_cause2,
yl.cause3 rendement_cause3,
yl.comment qualite_commentaire ,
yi.comment rendementqualite_commentaires_global,
rgs.vitiyieldobjective objectif_rendement_viti,
rgs.vitilosscause1 rendement_cause1_viti,
rgs.vitilosscause2 rendement_cause2_viti,
rgs.vitilosscause3 rendement_cause3_viti,
rgs.vitiyieldquality qualite_commentaire_viti,
rgs.topiaid bilan_campagne_sdc_generalites_id
from reportgrowingsystem rgs
join yieldloss yl on rgs.topiaid = yl.reportgrowingsystem
left join yieldinfo yi on rgs.topiaid = yi.reportgrowingsystem
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id = rgs.topiaid;

alter table entrepot_bilan_campagne_sdc_rendement
add constraint bilan_campagne_sdc_rendement_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_rendement
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);

-- Alimentation hydrique et minerale
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
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'irrigation') trad1 on fm.foodirrigation = trad1.nom_base 
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'stress hydrique mineral temperature') trad2 on fm.hydriquestress = trad2.nom_base 
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'stress hydrique mineral temperature') trad3 on fm.azotestress = trad3.nom_base 
left join (select * from traductions_bilan_campagne_sdc where nom_rubrique = 'stress hydrique mineral temperature') trad4 on fm.tempstress = trad4.nom_base
join entrepot_bilan_campagne_sdc_generalites ebcsg on ebcsg.id = fm.foodmasterreportgrowingsystem ;

alter table entrepot_bilan_campagne_sdc_alimentation
add constraint bilan_campagne_sdc_alimentation_PK
PRIMARY KEY (id);

alter table entrepot_bilan_campagne_sdc_alimentation
ADD FOREIGN KEY (bilan_campagne_sdc_generalites_id) REFERENCES entrepot_bilan_campagne_sdc_generalites(id);


-- DROP TABLE IF EXISTS traductions_bilan_campagne_sdc;
