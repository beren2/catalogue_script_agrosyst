DROP TABLE IF EXISTS exports_agronomes_context_input_usages;

-- Table usage_id + action_id
create temporary table exports_agronomes_context_input_usages as 
  	select a.topiaid usage_id, aa.topiaid action_id
	  	from abstractinputusage a
		left join mineralproductinputusage m ON m.topiaid = a.topiaid  
		left join biologicalproductinputusage b on b.topiaid = a.topiaid 
		left join pesticideproductinputusage p on p.topiaid = a.topiaid
		left join organicproductinputusage o ON o.topiaid = a.topiaid 
		left join potinputusage pot ON pot.topiaid = a.topiaid 
		left join substrateinputusage sub ON sub.topiaid = a.topiaid 
		left join otherproductinputusage other on other.topiaid = a.topiaid 
		join abstractaction aa on aa.topiaid in (m.mineralfertilizersspreadingaction, b.biologicalcontrolaction, p.pesticidesspreadingaction, o.organicfertilizersspreadingaction, pot.otheraction, sub.otheraction, other.otheraction, other.pesticidesspreadingaction, other.biologicalcontrolaction,
		other.harvestingaction, other.irrigationaction, other.maintenancepruningvinesaction, other.mineralfertilizersspreadingaction, other.organicfertilizersspreadingaction, other.pesticidesspreadingaction, other.seedingaction)
	union
	select a.topiaid usage_id, aa.topiaid action_id 
		from abstractinputusage a
	 	join irrigationinputusage i on i.topiaid = a.topiaid 
	 	join abstractaction aa on aa.irrigationinputusage = i.topiaid
	union
	-- espece de semence
	select a.topiaid usage_id, aa.topiaid action_id 
		from abstractinputusage a
		join seedspeciesinputusage su on su.topiaid = a.topiaid 
		join seedlotinputusage slu on su.seedlotinputusage = slu.topiaid 
		join abstractaction aa on slu.seedingactionusage = aa.topiaid
	union
	--lot de semence quand il n'y a pas d'esp associee
	select a.topiaid usage_id, aa.topiaid action_id 
		from abstractinputusage a
		join seedlotinputusage slu on slu.topiaid = a.topiaid 
		join abstractaction aa on slu.seedingactionusage = aa.topiaid
		join domainseedlotinput dl on dl.topiaid = slu.domainseedlotinput 
		left join domainseedspeciesinput dssi on dssi.domainseedlotinput = dl.topiaid 
  		where dssi.topiaid is null 
  	union
  	-- traitement de semence
	select a.topiaid usage_id, aa.topiaid action_id 
		from abstractinputusage a
		join seedproductinputusage spu on spu.topiaid = a.topiaid 
		join seedspeciesinputusage su on su.topiaid = spu.seedspeciesinputusage 
		join seedlotinputusage slu on su.seedlotinputusage = slu.topiaid 
		join abstractaction aa on slu.seedingactionusage = aa.topiaid;

CREATE INDEX if not exists exports_agronomes_context_input_usages_idx ON exports_agronomes_context_input_usages(usage_id);
CREATE INDEX if not exists exports_agronomes_context_input_usages_idx2 ON exports_agronomes_context_input_usages(action_id);

-------------------------------
-- Intrants_Synthetise
-------------------------------
CREATE TABLE entrepot_utilisation_intrant_synthetise(
  id character varying(255),
  campagne text,
  intrant_type text,
  dose double precision,
  volume_bouillie_hl double precision,
  unite text,
  profondeur_semis_cm double precision,
  intrant_phyto_type text,
  intrant_phyto_cible_nom text,
  intervention_synthetise_id character varying(255),
  action_synthetise_id character varying(255),
  intrant_id character varying(255),
  semence_id character varying(255)
);


-- requête pour insérer l'assolé
INSERT INTO entrepot_utilisation_intrant_synthetise  (
	id,
	campagne, 
	intrant_type,
	dose, 
	profondeur_semis_cm,
	volume_bouillie_hl,
	unite, 
	intrant_phyto_type, 
	intrant_phyto_cible_nom, 
	intervention_synthetise_id, 
	action_synthetise_id,
	intrant_id, 
	semence_id
)
	SELECT
		cu.usage_id as id,
		esdc.campagne as campagne,
		null intrant_type,
		null dose,
		null profondeur_semis_cm,
		aa.boiledquantity volume_bouillie_hl,
		null unite,
		null intrant_phyto_type,
		null intrant_phyto_cible_nom,
		pi.topiaid intervention_synthetise_id,
		aa.topiaid as action_synthetise_id,
		null intrant_id,
		null semence_id
	FROM abstractaction aa
	JOIN practicedintervention pi ON pi.topiaid = aa.practicedintervention
	JOIN practicedcropcycleconnection pccc ON pi.practicedcropcycleconnection = pccc.topiaid
	JOIN practicedcropcyclenode pccnt ON pccc.target = pccnt.topiaid
	JOIN practicedcropcyclenode pccns ON pccc.source = pccns.topiaid
	JOIN practicedcropcycle pcc ON pccnt.practicedseasonalcropcycle = pcc.topiaid
	JOIN practicedsystem ps ON pcc.practicedsystem = ps.topiaid
	JOIN entrepot_sdc esdc on ps.growingsystem = esdc.id
	join exports_agronomes_context_input_usages cu on aa.topiaid = cu.action_id
	AND ps.active IS TRUE;


-- requête pour insérer le pérenne
INSERT INTO entrepot_utilisation_intrant_synthetise  (
	id,
	campagne, 
	intrant_type,
	dose, 
	profondeur_semis_cm,
	volume_bouillie_hl,
	unite, 
	intrant_phyto_type, 
	intrant_phyto_cible_nom, 
	intervention_synthetise_id, 
	action_synthetise_id,
	intrant_id, 
	semence_id
)
	SELECT
		cu.usage_id id,
		esdc.campagne,
		null intrant_type,
		null dose,
		null profondeur_semis_cm,
		aa.boiledquantity volume_bouillie_hl,
		null unite,
		null intrant_phyto_type,
		null intrant_phyto_cible_nom,
		pi.topiaid intervention_synthetise_id,
		aa.topiaid as action_synthetise_id,
		null intrant_id,
		null semence_id
	FROM abstractaction aa
	JOIN practicedintervention pi ON pi.topiaid = aa.practicedintervention
	JOIN practicedcropcyclephase pccp ON pi.practicedcropcyclephase = pccp.topiaid
	JOIN practicedperennialcropcycle ppcc ON pccp.practicedperennialcropcycle = ppcc.topiaid
	JOIN practicedcropcycle pcc ON ppcc.topiaid = pcc.topiaid
	JOIN practicedsystem ps ON pcc.practicedsystem = ps.topiaid
	JOIN entrepot_sdc esdc on ps.growingsystem = esdc.id
	join exports_agronomes_context_input_usages cu on aa.topiaid = cu.action_id
	AND ps.active IS TRUE;


CREATE INDEX if not exists entrepot_utilisation_intrant_synthetise_inputid_idx ON entrepot_utilisation_intrant_synthetise (id);


-- 9 sec : INTRANTS MINERAUX 
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = d.topiaid,
	unite = d.usageunit,
	intrant_type = u.inputtype,
	dose = u.qtavg
from mineralproductinputusage m 
join abstractinputusage u on m.topiaid = u.topiaid 
join domainmineralproductinput d on m.domainmineralproductinput = d.topiaid 
join abstractdomaininputstockunit su on d.topiaid = su.topiaid
where u.topiaid = e.id;


-- 35 sec : INTRANTS PRODUITS PHYTOS (contient les traitements de semence)
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = d.topiaid,
	unite = d.usageunit,
	dose = u.qtavg,
	intrant_type = u.inputtype,
	intrant_phyto_type = d.producttype
from abstractphytoproductinputusage p 
join abstractinputusage u on p.topiaid = u.topiaid 
join domainphytoproductinput d on p.domainphytoproductinput = d.topiaid 
join abstractdomaininputstockunit su on d.topiaid = su.topiaid 
where u.topiaid = e.id;


-- 1 secondes : INTRANTS IRRIGATIONS
update entrepot_utilisation_intrant_synthetise e set
	intrant_id = d.topiaid,
	unite = d.usageunit,
	dose = u.qtavg
from irrigationinputusage i 
join abstractinputusage u on i.topiaid = u.topiaid 
join domainirrigationinput d on i.domainirrigationinput = d.topiaid 
join abstractaction a on a.irrigationinputusage = i.topiaid 
where u.topiaid = e.id;


-- ESPECES DE SEMENCES.
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = dl.topiaid,
	unite = dl.usageunit,
	intrant_type = u.inputtype,
	dose = u.qtavg,
	profondeur_semis_cm = s.deepness,
	semence_id = dssi.topiaid
from seedspeciesinputusage s 
join abstractinputusage u on s.topiaid = u.topiaid 
join domainseedspeciesinput dssi on s.domainseedspeciesinput = dssi.topiaid
join domainseedlotinput dl on dl.topiaid = dssi.domainseedlotinput 
where u.topiaid = e.id;

-- Lots de semence, uniquement lorsque au sein de ce lot il n'y a aucune especes déclarées (aucunes esp dans la culture)
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = dl.topiaid,
	unite = dl.usageunit,
	intrant_type = u.inputtype
from seedlotinputusage slu 
join abstractinputusage u on slu.topiaid = u.topiaid 
join domainseedlotinput dl on dl.topiaid = slu.domainseedlotinput 
left join domainseedspeciesinput dssi on dssi.domainseedlotinput = dl.topiaid 
where dssi.topiaid is null and u.topiaid = e.id;


-- 3 sec : INTRANTS ORGANIQUES
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = d.topiaid,
	intrant_type = u.inputtype,
	unite = d.usageunit,
	dose = u.qtavg
from organicproductinputusage o 
join abstractinputusage u on o.topiaid = u.topiaid 
join domainorganicproductinput d on o.domainorganicproductinput = d.topiaid 
join abstractdomaininputstockunit su on d.topiaid = su.topiaid 
where u.topiaid = e.id;




-- 1 sec : INTRANTS AUTRES
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = d.topiaid,
	intrant_type = u.inputtype,
	unite = d.usageunit,
	dose = u.qtavg
from otherproductinputusage o 
join abstractinputusage u on o.topiaid = u.topiaid 
join domainotherinput d on o.domainotherinput  = d.topiaid 
join abstractdomaininputstockunit su on d.topiaid = su.topiaid 
where u.topiaid = e.id;


-- 1 sec : POTS
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = d.topiaid,
	intrant_type = u.inputtype,
	unite = d.usageunit,
	dose = u.qtavg
from potinputusage p
join abstractinputusage u on p.topiaid = u.topiaid 
join domainmineralproductinput d on p.domainpotinput  = d.topiaid 
join abstractdomaininputstockunit su on d.topiaid = su.topiaid 
where u.topiaid = e.id;


-- 1 sec : SUBTRATS
update entrepot_utilisation_intrant_synthetise e SET
	intrant_id = d.topiaid,
	intrant_type = u.inputtype,
	unite = d.usageunit,
	dose = u.qtavg
from substrateinputusage s
join abstractinputusage u on s.topiaid = u.topiaid 
join domainsubstrateinput d on s.domainsubstrateinput  = d.topiaid 
join abstractdomaininputstockunit su on d.topiaid = su.topiaid 
where u.topiaid = e.id;


 -- 20 secondes : Récupération et aggréations des espèces cibles. 
UPDATE entrepot_utilisation_intrant_synthetise eir SET intrant_phyto_cible_nom = (
    SELECT string_agg(
      (SELECT rnedi.reference_label FROM RefNuisibleEDI rnedi WHERE rnedi.topiaid = ppt.target AND ppt.abstractphytoproductinputusage = eir.id  UNION
       SELECT ra.adventice FROM RefAdventice ra WHERE ra.topiaid = ppt.target AND ppt.abstractphytoproductinputusage = eir.id ),'|')
       FROM phytoproducttarget ppt
       WHERE ppt.abstractphytoproductinputusage = eir.id
	   AND ppt0.topiaid = ppt.topiaid
  )
  FROM phytoproducttarget ppt0
  WHERE ppt0.abstractphytoproductinputusage = eir.id
  AND eir.intrant_type IN ('APPLICATION_DE_PRODUITS_PHYTOSANITAIRES', 'LUTTE_BIOLOGIQUE', 'TRAITEMENT_SEMENCE');
 
  
alter table entrepot_utilisation_intrant_synthetise
add constraint utilisation_intrant_synthetise_PK
PRIMARY KEY (id);

alter table entrepot_utilisation_intrant_synthetise
ADD FOREIGN KEY (intervention_synthetise_id) REFERENCES entrepot_intervention_synthetise(id);

alter table entrepot_utilisation_intrant_synthetise
ADD FOREIGN KEY (intrant_id) REFERENCES entrepot_intrant(id);
 
