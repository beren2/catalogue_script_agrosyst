DROP TABLE IF EXISTS entrepot_BC_sdc_generalites CASCADE;
CREATE TABLE entrepot_BC_sdc_generalites AS
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
replace(replace(rgs.highlightsevolutions,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS principales_evolutions_depuis_pz0,
replace(replace(rgs.highlightsmeasures,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS mesure_specifique_annee,
replace(replace(rgs.highlightsperformances,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS faits_marquants_conduiteculture_performancetechnique,
replace(replace(rgs.highlightsteachings,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS enseignements_amelioration_sdc,
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

alter table entrepot_BC_sdc_generalites
add constraint BC_sdc_generalites_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_generalites
ADD FOREIGN KEY (sdc_id) REFERENCES entrepot_sdc(id);

alter table entrepot_BC_sdc_generalites
ADD FOREIGN KEY (bcregional_associe_id) REFERENCES entrepot_bilan_campagne_regional_generalites(id);

alter table entrepot_BC_sdc_generalites
ADD FOREIGN KEY (modele_descisionelassocie_prevu_id) REFERENCES entrepot_modele_decisionnel(id);

alter table entrepot_BC_sdc_generalites
ADD FOREIGN KEY (modele_descisionelassocie_obs_id) REFERENCES entrepot_modele_decisionnel(id);

--------------------------------------------------------------------
-- ASSOLEE : Maitrise agresseurs = ravageurs, maladies et adventices
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_assolee_maitrise_agresseur CASCADE;
CREATE TABLE entrepot_BC_sdc_assolee_maitrise_agresseur AS
select
topiaid as id, 
case 
	when c.cropdiseasemasterreportgrowingsystem is not null then 'maladie'
	when c.croppestmasterreportgrowingsystem is not null then 'ravageur'
	when c.cropadventicemasterreportgrowingsystem is not null then 'adventice'
end type_bioagresseur,
case 
	when c.cropadventicemasterreportgrowingsystem is not null then iftmain
end IFT_herbicide,
case 
	when c.cropdiseasemasterreportgrowingsystem is not null then iftmain
end IFT_fongicide_chimique,
case 
	when c.croppestmasterreportgrowingsystem is not null then iftmain
end IFT_insecticide_chimique,
case 
	when c.croppestmasterreportgrowingsystem is not null then iftother
end IFT_autre_ravageur,
ifthorsbiocontrole as IFT_hors_biocontrol_EXPE,
replace(replace(c.advisercomments,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaires_conseiller_experi,
ebcsg.id as BC_sdc_generalites_id
from croppestmaster c  
join entrepot_BC_sdc_generalites ebcsg on ebcsg.id in (c.croppestmasterreportgrowingsystem, c.cropdiseasemasterreportgrowingsystem,c.cropadventicemasterreportgrowingsystem)
;

alter table entrepot_BC_sdc_assolee_maitrise_agresseur
add constraint BC_sdc_assolee_maitrise_agresseur_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_assolee_maitrise_agresseur
ADD FOREIGN KEY (BC_sdc_generalites_id) REFERENCES entrepot_BC_sdc_generalites(id);


DROP TABLE IF EXISTS entrepot_BC_sdc_assolee_agresseur;
CREATE TABLE entrepot_BC_sdc_assolee_agresseur AS
select 
pm.topiaid id,
'adventice' type_bioagresseur,
null groupe_cible,
refadv.adventice bioagresseur,
trad1.traduction_interface echelle_pression,
pm.pressurescaleint EXPE_echelle_pression_marhorti,
replace(replace(pm.pressurefarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS pression_commentaire_agri,
trad2.traduction_interface echelle_maitrise,
pm.masterscaleint EXPE_echelle_maitrise_marhorti,
pm.qualifier maitrise_qualifiant,
replace(replace(pm.resultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS maitrise_commentaire_agri,
bcsama.id as BC_sdc_assolee_maitrise_agresseur_id
from pestmaster pm
join entrepot_BC_sdc_assolee_maitrise_agresseur bcsama on bcsama.id = pm.croppestmaster 
join refadventice refadv on pm.agressor = refadv.topiaid
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle pression adventice assolee') trad1 on pm.pressurescale = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de maitrise adventice assolee') trad2 on pm.masterscale = trad2.nom_base
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
replace(replace(pm.pressurefarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS pression_commentaire_agri,
trad2.traduction_interface echelle_maitrise,
pm.masterscaleint EXPE_echelle_maitrise_marhorti,
pm.qualifier maitrise_qualifiant,
replace(replace(pm.resultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS maitrise_commentaire_agri,
bcsama.id as BC_sdc_assolee_maitrise_agresseur_id
from pestmaster pm
join croppestmaster cm on pm.croppestmaster = cm.topiaid
join entrepot_BC_sdc_assolee_maitrise_agresseur bcsama on bcsama.id = pm.croppestmaster 
join refnuisibleedi refnui on pm.agressor = refnui.topiaid
left join (select distinct code_groupe_cible_maa,groupe_cible_maa 
			from refciblesagrosystgroupesciblesmaa where active = true 
			and groupe_cible_maa not in ('Cicadelles cercopides et psylles','Maladies des taches foliaires')) refgrpcible -- on retire les doublons de code 38 'Cicadelles cercopides et psylles' puisque ce nom est utilisé par le 37 , et le 82 puisqu'il y a deux orthographes 
		on refgrpcible.code_groupe_cible_maa = pm.codegroupeciblemaa 
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de pression maladie ravageur assolee') trad1 on pm.pressurescale = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de maitrise maladie ravageur assolee') trad2 on pm.masterscale = trad2.nom_base
;


alter table entrepot_BC_sdc_assolee_agresseur
add constraint BC_sdc_assolee_agresseur_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_assolee_agresseur
ADD FOREIGN KEY (BC_sdc_assolee_maitrise_agresseur_id) REFERENCES entrepot_BC_sdc_assolee_maitrise_agresseur(id);


--------------------------------------------------------------------
-- ASSOLEE : Maitrise de la verse
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_assolee_verse;
CREATE TABLE entrepot_BC_sdc_assolee_verse AS
select 
vm.topiaid id ,
trad1.traduction_interface echelle_risque,
replace(replace(vm.riskfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS risque_commentaire_agri,
trad2.traduction_interface echelle_maitrise,
vm.qualifier maitrise_qualifiant, 
replace(replace(vm.resultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS resultats_commentaire_agri,
vm.iftmain IFT_regulateur , 
replace(replace(vm.advisercomments,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaire_conseiller,
vm.reportgrowingsystem BC_sdc_generalites_id
from versemaster vm
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de risque verse') trad1 on vm.riskscale = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de maitrise verse') trad2 on vm.masterscale = trad2.nom_base 
join entrepot_BC_sdc_generalites e on e.id = vm.reportgrowingsystem;

alter table entrepot_BC_sdc_assolee_verse
add constraint BC_sdc_assolee_verse_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_assolee_verse
ADD FOREIGN KEY (BC_sdc_generalites_id) REFERENCES entrepot_BC_sdc_generalites(id);


--------------------------------------------------------------------
-- ARBO : Adventice, maladies et ravageurs
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_arbo_maitrise_agresseur CASCADE;
CREATE TABLE entrepot_BC_sdc_arbo_maitrise_agresseur AS
select
a.topiaid as id,
'adventice' as type_bioagresseur,
a.treatmentcount as nombre_traitement,
a.chemicalpestift as ift_herbicide_chimique,
a.biocontrolpestift as ift_herbicide_biocontrole,
null as ift_fongicide_chimique,
null as ift_fongicide_biocontrole,
null as ift_ravageur_chimique,
null as ift_ravageur_biocontrole,
a.reportgrowingsystem as BC_sdc_generalites_id
from arbocropadventicemaster a 
join entrepot_BC_sdc_generalites ebcsg on ebcsg.id = a.reportgrowingsystem
union 
select 
a.topiaid as id,
case 
	when a.arbodiseasemasterreportgrowingsystem is not null then 'maladie'
	when a.arbopestmastergrowingsystem  is not null then 'ravageur'
end type_bioagresseur,
a.treatmentcount as nombre_traitement,
null as ift_chimique_herbicide,
null as ift_biocontrole_herbicide,
case 
	when a.arbodiseasemasterreportgrowingsystem is not null then a.chemicalpestift
end ift_fongicide_chimique,
case 
	when a.arbodiseasemasterreportgrowingsystem is not null then a.biocontrolpestift
end ift_fongicide_biocontrole,
case 
	when a.arbodiseasemasterreportgrowingsystem is not null then a.chemicalpestift
end ift_ravageur_chimique,
case 
	when a.arbodiseasemasterreportgrowingsystem is not null then a.biocontrolpestift
end ift_ravageur_biocontrole,
ebcsg.id as BC_sdc_generalites_id
from arbocroppestmaster a 
join entrepot_BC_sdc_generalites ebcsg on ebcsg.id in (a.arbodiseasemasterreportgrowingsystem, a.arbopestmastergrowingsystem)
;

alter table entrepot_BC_sdc_arbo_maitrise_agresseur
add constraint BC_sdc_arbo_maitrise_agresseur_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_arbo_maitrise_agresseur
ADD FOREIGN KEY (BC_sdc_generalites_id) REFERENCES entrepot_BC_sdc_generalites(id);

--------------------------------------------------------------------
-- ARBO : Adventice
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_arbo_adventice CASCADE;
CREATE TABLE entrepot_BC_sdc_arbo_adventice AS
select
a.topiaid as id,
r.adventice as adventice,
a.grassinglevel as niveau_enherbement,
trad2.traduction_interface as evolution_enherbement,
trad1.traduction_interface as echelle_maitrise ,
a.qualifier as qualification_maitrise,
replace(replace(a.resultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaire_agriculteur,
replace(replace(a.advisercomments,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaire_conseiller,
ebama.id as BC_sdc_arbo_maitrise_adventice_id
from arboadventicemaster a 
join refadventice r on r.topiaid = a.agressor
join entrepot_BC_sdc_arbo_maitrise_agresseur ebama on a.arbocropadventicemaster = ebama.id
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de maitrise arbo adv') trad1 on a.masterscale = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'evolution enherbement arbo adv') trad2 on a.grassingevolution = trad2.nom_base 
;

alter table entrepot_BC_sdc_arbo_adventice
add constraint BC_sdc_arbo_adventice_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_arbo_adventice
ADD FOREIGN KEY (BC_sdc_arbo_maitrise_adventice_id) REFERENCES entrepot_BC_sdc_arbo_maitrise_agresseur(id);

--------------------------------------------------------------------
-- ARBO : Maladies et ravageurs
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_arbo_ravageur_maladie CASCADE;
CREATE TABLE entrepot_BC_sdc_arbo_ravageur_maladie AS
select 
a.topiaid as id,
a.agressor as nuisible_edi_id,
a.codegroupeciblemaa as code_groupe_cible,
a.previousyearinoculum as inoculum_annee_precedente,
trad1.traduction_interface as echelle_pression,
trad2.traduction_interface as evolution_pression_annee_precedente,
trad3.traduction_interface as echelle_maitrise,
trad4.traduction_interface as parcelles_impactees_pct,
trad5.traduction_interface as arbres_impactes_pct,
trad6.traduction_interface as fruits_impactes_pct,
trad7.traduction_interface as feuilles_impactees_pct,
a.nextyearinoculum as inoculum_annees_suivantes,
a.qualifier as maitrise_qualifiant,
replace(replace(a.resultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaire_agri,
replace(replace(a.advisercomments,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaire_conseiller,
a.arbocroppestmaster as BC_sdc_arbo_maitrise_agresseur_id
from arbopestmaster a
join entrepot_BC_sdc_arbo_maitrise_agresseur ebsama on a.arbocroppestmaster = ebsama.id
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de pression maladie ravageur arbo') trad1 on a.pressurescale = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'evolution pression arbo maladie ravageur') trad2 on a.pressureevolution = trad2.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de maitrise maladie ravageur arbo') trad3 on a.masterscale = trad3.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'pct touchee arbo') trad4 on a.percentaffectedplots = trad4.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'pct touchee arbo') trad5 on a.percentaffectedtrees = trad5.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'pct touchee arbo') trad6 on a.percentdamagefruits = trad6.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'pct touchee arbo') trad7 on a.percentdamageleafs = trad7.nom_base 
;

alter table entrepot_BC_sdc_arbo_ravageur_maladie
add constraint BC_sdc_arbo_maitrise_ravageur_maladie_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_arbo_ravageur_maladie
ADD FOREIGN KEY (nuisible_edi_id) REFERENCES entrepot_nuisible_edi(id);

alter table entrepot_BC_sdc_arbo_ravageur_maladie
ADD FOREIGN KEY (BC_sdc_arbo_maitrise_agresseur_id) REFERENCES entrepot_BC_sdc_arbo_maitrise_agresseur(id);

--------------------------------------------------------------------
-- Viti : Adventice, maladies et ravageurs
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_viti_adventice CASCADE;
CREATE TABLE entrepot_BC_sdc_viti_adventice AS
select
-- les infos de la viti sont dans rgs mais pour une cohérence avec les autres tables, 
-- on cree un id à partir de celui rgs pour qu'il ne change pas à chaque generation de entrepot
'fr.inra.agrosyst.api.entities.report.VitiAdventiceMaster_' || SUBSTR(rgs.topiaid,58),
trad1.traduction_interface as echelle_pression,
replace(replace(rgs.vitiadventicepressurefarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS pression_commentaire_agri,
rgs.vitiadventicequalifier as niveau_maitrise,
replace(replace(rgs.vitiadventiceresultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS niveau_maitrise_commentaire_agri,
rgs.vitiherbotreatmentchemical as nb_traitement_herbicide_chimique,
rgs.vitiherbotreatmentbiocontrol as nb_traitement_herbicide_biocontrol,
rgs.vitisuckeringchemical as nb_traitement_epamprage_chimique,
rgs.vitisuckeringbiocontrol as nb_traitement_epamprage_biocontrol,
rgs.vitiherbotreatmentchemicalift as ift_herbicide_chimique,
rgs.vitiherbotreatmentbiocontrolift as ift_herbicide_biocontrol,
rgs.vitisuckeringchemicalift as ift_epamprage_chimique,
rgs.vitisuckeringbiocontrolift as ift_epamprage_biocontrol,
rgs.topiaid as BC_sdc_generalites_id
from reportgrowingsystem rgs
join entrepot_sdc es on es.id = rgs.growingsystem
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle pression adventice viti') trad1 on rgs.vitiadventicepressurescale = trad1.nom_base 
where es.filiere = 'VITICULTURE';


DROP TABLE IF EXISTS entrepot_BC_sdc_viti_maladie_ravageur CASCADE;
CREATE TABLE entrepot_BC_sdc_viti_maladie_ravageur AS
select
v.topiaid ,
case 
	when v.reportgrowingsystemvitidiseasemaster is not null then 'maladie'
	when v.reportgrowingsystemvitipestmaster is not null then 'ravageur'
end type_bioagresseur,
v.agressor as nuisible_edi_id,
v.codegroupeciblemaa as groupe_cible_code,
trad5.traduction_interface as echelle_pression,
trad6.traduction_interface as evolution_pression_annee_precedente,
replace(replace(v.pressurefarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS pression_commentaire_agri,
trad7.traduction_interface as echelle_maitrise,
trad1.traduction_interface as note_attaque_feuille_maladie,
trad2.traduction_interface as note_attaque_feuille_ravageur,
trad3.traduction_interface as note_attaque_grappe_maladie,
trad4.traduction_interface as note_attaque_grappe_ravageur,
v.qualifier as maitrise_qualifiant,
replace(replace(v.resultfarmercomment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS maitrise_commentaire_agri,
replace(replace(v.advisercomments,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS maitrise_commentaire_conseiller,
v.treatmentcount as nombre_traitement,
v.nbpesttraitementrequired as nombre_traitement_obligatoire,
v.chemicalfungicideift as ift_chimique,
v.biocontrolfungicideift as ift_biocontrole,
case 
	when v.reportgrowingsystemvitidiseasemaster is not null then v.reportgrowingsystemvitidiseasemaster
	when v.reportgrowingsystemvitipestmaster is not null then v.reportgrowingsystemvitipestmaster
end BC_sdc_generalites_id,
v.leafdiseaseattackrateprecisevalue as notre_fq_attaque_feuille_EXPE,
v.leafdiseaseattackintensityprecisevalue as notre_intensite_attaque_feuille_EXPE,
v.grapediseaseattackintensityprecisevalue as notre_fq_attaque_grappe_EXPE,
v.grapediseaseattackrateprecisevalue as notre_intensite_attaque_grappe_EXPE
from vitipestmaster v 
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'Note globale attaque maladie feuille') trad1 on v.leafdiseaseattackrate = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'Note globale attaque ravageurs feuille') trad2 on v.leafpestattackrate = trad2.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'Note globale attaque maladie grappe') trad3 on v.grapediseaseattackrate = trad3.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'Note globale attaque ravageurs grappe') trad4 on v.grapepestattackrate = trad4.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de pression maladie ravageur viti') trad5 on v.pressurescale = trad5.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'evolution pression viti maladie ravageur') trad6 on v.pressureevolution = trad6.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'echelle de maitrise maladie ravageur viti') trad7 on v.masterscale = trad7.nom_base 
;


--------------------------------------------------------------------
-- TOUTES fillieres : Rendement
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_rendement;
CREATE TABLE entrepot_BC_sdc_rendement AS
select 
coalesce(yl.topiaid,'') ||''|| coalesce(yi.topiaid,'') id,
case 
	when yl.yieldobjective is not null then trad1.traduction_interface
	when yl.yieldobjectiveint is not null then trad2.traduction_interface
end objectif_rendement_atteint,
yl.cause1 as rendement_cause1,
yl.cause2 as rendement_cause2,
yl.cause3 as rendement_cause3,
replace(replace(yl.comment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS qualite_commentaire,
replace(replace(yi.comment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS rendementqualite_commentaire_global,
rgs.topiaid as BC_sdc_generalites_id
from reportgrowingsystem rgs
join growingsystem gs on gs.topiaid = rgs.growingsystem
left join yieldinfo yi on rgs.topiaid = yi.reportgrowingsystem
left join yieldloss yl on rgs.topiaid = yl.reportgrowingsystem
join entrepot_BC_sdc_generalites ebcsg on ebcsg.id = rgs.topiaid
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'rendement echelle objectif') trad1 on yl.yieldobjective = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'rendement echelle objectif expe') trad2 on yl.yieldobjectiveint::text = trad1.nom_base 
where gs.sector <> 'VITICULTURE' and (yi.topiaid is not null or yl.topiaid is not null)
union 
select 
'fr.inra.agrosyst.api.entities.report.YieldLoss_' || SUBSTR(rgs.topiaid,58), -- les infos de la viti sont dans rgs mais sont les memes donc on attribut un id
trad1.traduction_interface as objectif_rendement_atteint,
rgs.vitilosscause1 as rendement_cause1,
rgs.vitilosscause2 as  rendement_cause2,
rgs.vitilosscause3 as  rendement_cause3,
replace(replace(rgs.vitiyieldquality,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS qualite_commentaire,
replace(replace(yi.comment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS rendementqualite_commentaire_global,
rgs.topiaid BC_sdc_generalites_id
from reportgrowingsystem rgs
join growingsystem gs on gs.topiaid = rgs.growingsystem
left join yieldinfo yi on rgs.topiaid = yi.reportgrowingsystem and yi.sector = 'VITICULTURE'
join entrepot_BC_sdc_generalites ebcsg on ebcsg.id = rgs.topiaid
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'rendement echelle objectif') trad1 on rgs.vitiyieldobjective = trad1.nom_base 
where gs.sector = 'VITICULTURE'
;

alter table entrepot_BC_sdc_rendement
add constraint BC_sdc_rendement_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_rendement
ADD FOREIGN KEY (BC_sdc_generalites_id) REFERENCES entrepot_BC_sdc_generalites(id);


--------------------------------------------------------------------
-- TOUTES fillieres : Alimentation hydrique et minerale
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_alimentation;
CREATE TABLE entrepot_BC_sdc_alimentation AS
select 
fm.topiaid id,
trad1.traduction_interface irrigation ,
trad2.traduction_interface stress_hydrique ,
trad3.traduction_interface stress_azote ,
replace(replace(fm.mineralfood ,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS alimentation_minerale_hors_azote,
trad4.traduction_interface stress_temperature_rayonnement ,
replace(replace(fm.comment,CHR(13)||CHR(10),'<br>'),CHR(10),'<br>') AS commentaire,
ebcsg.id BC_sdc_generalites_id
from foodmaster fm 
-- traductions des libelles
left join (select * from BC_sdc_traduction where nom_rubrique = 'irrigation') trad1 on fm.foodirrigation = trad1.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'stress hydrique mineral temperature') trad2 on fm.hydriquestress = trad2.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'stress hydrique mineral temperature') trad3 on fm.azotestress = trad3.nom_base 
left join (select * from BC_sdc_traduction where nom_rubrique = 'stress hydrique mineral temperature') trad4 on fm.tempstress = trad4.nom_base
join entrepot_BC_sdc_generalites ebcsg on ebcsg.id = fm.foodmasterreportgrowingsystem ;

alter table entrepot_BC_sdc_alimentation
add constraint BC_sdc_alimentation_PK
PRIMARY KEY (id);

alter table entrepot_BC_sdc_alimentation
ADD FOREIGN KEY (BC_sdc_generalites_id) REFERENCES entrepot_BC_sdc_generalites(id);

--------------------------------------------------------------------
-- TOUTES entites et fillieres : cultures liee pour reduire le nombre de tables creees
--------------------------------------------------------------------

DROP TABLE IF EXISTS entrepot_BC_sdc_culture_liee;
CREATE TABLE entrepot_BC_sdc_culture_liee as
select 
cc.croppestmaster as entite_id,
cc.crops as culture_id
from croppestmaster_crops cc 
join entrepot_composant_culture ec on ec.id = cc.crops 
union
select 
ac.arbocropadventicemaster as entite_id,
ac.crops as culture_id
from arbocropadventicemaster_crops ac 
join entrepot_composant_culture ec on ec.id = ac.crops  
union
select 
ac2.arbocroppestmaster as entite_id,
ac2.crops as culture_id
from arbocroppestmaster_crops ac2  
join entrepot_composant_culture ec on ec.id = ac2.crops 
union
select 
cf.foodmaster as entite_id,
cf.crops as culture_id
from crops_foodmaster cf
join entrepot_composant_culture ec on ec.id = cf.crops 
union
select 
cv.versemaster as entite_id,
cv.crops as culture_id
from crops_versemaster cv    
join entrepot_composant_culture ec on ec.id = cv.crops 
union
select 
cy.yieldloss as entite_id,
cy.crops as culture_id
from crops_yieldloss cy  
join entrepot_composant_culture ec on ec.id = cy.crops 
;

alter table entrepot_BC_sdc_culture_liee
ADD FOREIGN KEY (culture_id) REFERENCES entrepot_culture(id);


DROP TABLE IF EXISTS entrepot_BC_sdc_especes_liee;
CREATE TABLE entrepot_BC_sdc_especes_liee as
select 
cs.croppestmaster as entite_id,
cs.species as composant_culture_id
from croppestmaster_species cs 
join entrepot_composant_culture ec on ec.id = cs.species
union
select 
s.arbocropadventicemaster as entite_id,
s.species as composant_culture_id
from arbocropadventicemaster_species s
join entrepot_composant_culture ec on ec.id = s.species
union
select 
as2.arbocroppestmaster as entite_id,
as2.species as composant_culture_id
from arbocroppestmaster_species as2  
join entrepot_composant_culture ec on ec.id = as2.species
union
select 
fs.foodmaster as entite_id,
fs.species as composant_culture_id
from foodmaster_species fs
join entrepot_composant_culture ec on ec.id = fs.species
union
select 
sv.versemaster as entite_id,
sv.species as composant_culture_id
from species_versemaster sv    
join entrepot_composant_culture ec on ec.id = sv.species
union
select 
sy.yieldloss as entite_id,
sy.species as composant_culture_id
from species_yieldloss sy
join entrepot_composant_culture ec on ec.id = sy.species
;

alter table entrepot_BC_sdc_especes_liee
ADD FOREIGN KEY (composant_culture_id) REFERENCES entrepot_composant_culture(id);
