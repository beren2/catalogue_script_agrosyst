-- cette table est un peu particulière : on doit préalablement récupérer des informations provenant des actions. 
-- en effet, le psci, traditionnelement défini au niveau de l'intervention fait appel à certaines informations à l'échelle de l'action.
-- on a donc 3 psci différentes : 
-- 	- le psci de l'intervention (n'intègre pas la pondération par la proportion de surface traitée)
--	- le psci_phyto_avec_amm (dans le cas des interventions contenant une action de type "APPLICATION_DE_PRODUITS_PHYTOSANITAIRES"), le psci pondéré par la proportion de surface traitée
-- 	- le psci_phyto_sans_amm (dans le cas des interventions contenant une action de type "LUTTE_BIOLOGIQUE"), le psci pondéré par la proportion de surface traitée
-- c'est une entorse au principe de l'entrepôt qui est censé uniquement sélectionner les informations présentes dans la base, au bénéfice du confort de l'utilisateur historique. 

CREATE TEMPORARY table action_realise_phyto_avec_amm AS 
SELECT DISTINCT ON (aa.effectiveintervention)
	aa.topiaid,
	aa.proportionoftreatedsurface,
	aa.effectiveintervention --avant on pouvait en saisir plusieurs sur l'interface
FROM abstractaction aa
JOIN refinterventionagrosysttravailedi refintrav ON aa.mainaction = refintrav.topiaid
where refintrav.intervention_agrosyst = 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES';

CREATE TEMPORARY table action_realise_phyto_sans_amm AS 
SELECT DISTINCT ON (aa.effectiveintervention)
	aa.topiaid,
	aa.proportionoftreatedsurface,
	aa.effectiveintervention
FROM abstractaction aa
JOIN refinterventionagrosysttravailedi refintrav ON aa.mainaction = refintrav.topiaid
where refintrav.intervention_agrosyst = 'LUTTE_BIOLOGIQUE';


CREATE TABLE entrepot_intervention_realise AS
---------------------------
-- Interventions Assolees
---------------------------
select
ei.topiaid id,
ei.name nom,
ei.type "type",
ei.comment commentaire,
ei.startinterventiondate date_debut,
ei.endinterventiondate date_fin,
ei.spatialfrequency freq_spatiale,
ei.transitcount nombre_de_passage,
ei.spatialfrequency * ei.transitcount as psci,
aa1.proportionoftreatedsurface * ei.spatialfrequency * ei.transitcount / 100 as psci_phyto_avec_amm,
aa2.proportionoftreatedsurface * ei.spatialfrequency * ei.transitcount / 100 as psci_phyto_sans_amm,
--ei.spatialfrequency * ei.transitcount psci_intervention,
ei.workrate debit_de_chantier,
ei.workrateunit debit_de_chantier_unite,
ei.progressionspeed vitesse_avancement,
ei.involvedpeoplecount nb_personne_mobili,
ei.intermediatecrop concerne_ci,
ei.effectivecropcyclenode noeuds_realise_id,
'NA' plantation_perenne_phases_realise_id,
eitc.toolcouplings combinaison_outil_id
FROM effectiveintervention ei
LEFT JOIN effectiveintervention_toolcouplings eitc on eitc.effectiveintervention = ei.topiaid 
LEFT JOIN action_realise_phyto_avec_amm aa1 on aa1.effectiveintervention = ei.topiaid 
LEFT JOIN action_realise_phyto_sans_amm aa2 on aa2.effectiveintervention = ei.topiaid 
JOIN entrepot_noeuds_realise enr on enr.id = ei.effectivecropcyclenode 

UNION all

------------------------------
-- Interventions Perennes
------------------------------
select 
ei.topiaid id,
ei.name nom,
ei.type "type",
ei.comment commentaire,
ei.startinterventiondate date_debut,
ei.endinterventiondate date_fin,
ei.spatialfrequency freq_spatiale,
ei.transitcount nombre_de_passage,
ei.spatialfrequency * ei.transitcount as psci,
aa1.proportionoftreatedsurface * ei.spatialfrequency * ei.transitcount / 100 as psci_phyto_avec_amm,
aa2.proportionoftreatedsurface * ei.spatialfrequency * ei.transitcount / 100 as psci_phyto_sans_amm,
ei.workrate debit_de_chantier,
ei.workrateunit debit_de_chantier_unite,
ei.progressionspeed vitesse_avancement,
ei.involvedpeoplecount nb_personne_mobili,
ei.intermediatecrop concerne_ci,
'NA' noeuds_realise_id,
epppr.id plantation_perenne_phases_realise_id,
eitc.toolcouplings combinaison_outil_id
FROM effectiveintervention ei
JOIN effectivecropcyclephase eccp ON ei.effectivecropcyclephase = eccp.topiaid
LEFT JOIN effectiveintervention_toolcouplings eitc on eitc.effectiveintervention = ei.topiaid
LEFT JOIN action_realise_phyto_avec_amm aa1 on aa1.effectiveintervention = ei.topiaid 
LEFT JOIN action_realise_phyto_sans_amm aa2 on aa2.effectiveintervention = ei.topiaid 
JOIN entrepot_plantation_perenne_phases_realise epppr on epppr.id = eccp.topiaid;

alter table entrepot_intervention_realise
add constraint intervention_realise_PK
PRIMARY KEY (id);

alter table entrepot_intervention_realise
ADD FOREIGN KEY (combinaison_outil_id) REFERENCES entrepot_combinaison_outil(id);

-- Les clés etrangeres qui ne concerne que les assolees ou perennes ne peuvent pas être ajoutees comme contraintes = il y a des NA dans la colonne
