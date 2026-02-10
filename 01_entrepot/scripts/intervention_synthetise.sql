-- cette table est un peu particulière : on doit préalablement récupérer des informations provenant des actions. 
-- en effet, le psci, traditionnelement défini au niveau de l'intervention fait appel à certaines informations à l'échelle de l'action.
-- on a donc 3 psci différentes : 
-- 	- le psci de l'intervention (n'intègre pas la pondération par la proportion de surface traitée)
--	- le psci_phyto_avec_amm (dans le cas des interventions contenant une action de type "APPLICATION_DE_PRODUITS_PHYTOSANITAIRES"), le psci pondéré par la proportion de surface traitée
-- 	- le psci_phyto_sans_amm (dans le cas des interventions contenant une action de type "LUTTE_BIOLOGIQUE"), le psci pondéré par la proportion de surface traitée
-- c'est une entorse au principe de l'entrepôt qui est censé uniquement sélectionner les informations présentes dans la base, au bénéfice du confort de l'utilisateur historique. 

DROP TABLE IF EXISTS action_synthetise_phyto_avec_amm CASCADE;
CREATE TEMPORARY table action_synthetise_phyto_avec_amm AS 
SELECT DISTINCT ON (aa.practicedintervention)
	aa.topiaid,
	aa.proportionoftreatedsurface,
	aa.practicedintervention
FROM abstractaction aa
JOIN refinterventionagrosysttravailedi refintrav ON aa.mainaction = refintrav.topiaid
where refintrav.intervention_agrosyst = 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES';

DROP TABLE IF EXISTS action_synthetise_phyto_sans_amm CASCADE;
CREATE TEMPORARY table action_synthetise_phyto_sans_amm AS 
SELECT DISTINCT ON (aa.practicedintervention)
	aa.topiaid,
	aa.proportionoftreatedsurface,
	aa.practicedintervention
FROM abstractaction aa
JOIN refinterventionagrosysttravailedi refintrav ON aa.mainaction = refintrav.topiaid
where refintrav.intervention_agrosyst = 'LUTTE_BIOLOGIQUE';


CREATE INDEX if not exists entrepot_domaine_idx0 on entrepot_domaine(id);
CREATE INDEX if not exists entrepot_dispositif_idx0 on entrepot_dispositif(id);
CREATE INDEX if not exists entrepot_abstraction_action_idx0 on abstractaction(topiaid, mainaction);
CREATE INDEX if not exists entrepot_abstraction_action_idx3 on refinterventionagrosysttravailedi(topiaid);
CREATE INDEX if not exists entrepot_abstraction_action_idx4 on practicedcropcyclenode(topiaid);
CREATE INDEX if not exists entrepot_abstraction_action_idx5 on practicedcropcycleconnection(target);
CREATE INDEX if not exists entrepot_abstraction_action_idx6 on practicedcropcycleconnection(source);
CREATE INDEX if not exists entrepot_abstraction_action_idx7 on practicedintervention(practicedcropcycleconnection);

drop table if exists entrepot_intervention_synthetise cascade;
CREATE TABLE entrepot_intervention_synthetise as 
---------------------------
-- Interventions Assolées
---------------------------
select
pi.topiaid id,
pi.name nom,
pi.type,
pi.comment commentaire,
pi.rank +1 rang, -- !! Rang de l intervention et pas de la culture
pi.startingperioddate date_debut,
pi.endingperioddate date_fin,
pi.spatialfrequency freq_spatiale,
pi.temporalfrequency freq_temporelle,
pi.spatialfrequency * pi.temporalfrequency as psci,
aa1.proportionoftreatedsurface * pi.spatialfrequency * pi.temporalfrequency / 100 as psci_phyto_avec_amm,
aa2.proportionoftreatedsurface * pi.spatialfrequency * pi.temporalfrequency / 100 as psci_phyto_sans_amm,
-- pi.spatialfrequency * pi.temporalfrequency psci_intervention,
pi.workrate debit_de_chantier,
pi.workrateunit debit_de_chantier_unite,
pi.progressionspeed vitesse_avancement,
pi.involvedpeoplenumber nb_personne_mobili,
pi.intermediatecrop concerne_ci,
ecs.id connection_synthetise_id,
'NA' plantation_perenne_phases_synthetise_id,
pitcc.toolscouplingcodes combinaison_outil_code
FROM practicedintervention pi
JOIN practicedcropcycleconnection pccc ON pi.practicedcropcycleconnection = pccc.topiaid
LEFT JOIN practicedintervention_toolscouplingcodes pitcc ON pi.topiaid = pitcc.owner
LEFT JOIN action_synthetise_phyto_avec_amm aa1 on aa1.practicedintervention = pi.topiaid 
LEFT JOIN action_synthetise_phyto_sans_amm aa2 on aa2.practicedintervention = pi.topiaid 
JOIN entrepot_connection_synthetise ecs ON pccc.topiaid = ecs.id

UNION
---------------------------
-- Interventions Perennes
---------------------------
select
pi.topiaid id,
pi.name nom,
pi.type,
pi.comment commentaire,
pi.rank +1 rang, -- !! Rang de l intervention et pas de la culture
pi.startingperioddate date_debut,
pi.endingperioddate date_fin,
pi.spatialfrequency freq_spatiale,
pi.temporalfrequency freq_temporelle,
pi.spatialfrequency * pi.temporalfrequency as psci,
aa1.proportionoftreatedsurface * pi.spatialfrequency * pi.temporalfrequency / 100 as psci_phyto_avec_amm,
aa2.proportionoftreatedsurface * pi.spatialfrequency * pi.temporalfrequency / 100 as psci_phyto_sans_amm,
-- pi.spatialfrequency * pi.temporalfrequency psci_intervention,
pi.workrate debit_de_chantier,
pi.workrateunit debit_de_chantier_unite,
pi.progressionspeed vitesse_avancement,
pi.involvedpeoplenumber nb_personne_mobili,
pi.intermediatecrop concerne_ci,
'NA' connection_synthetise_id,
pccp.topiaid plantation_perenne_phases_synthetise_id,
pitcc.toolscouplingcodes combinaison_outil_code
FROM practicedintervention pi
JOIN practicedcropcyclephase pccp ON pi.practicedcropcyclephase = pccp.topiaid
left JOIN practicedintervention_toolscouplingcodes pitcc ON pi.topiaid = pitcc.owner
LEFT JOIN action_synthetise_phyto_avec_amm aa1 on aa1.practicedintervention = pi.topiaid 
LEFT JOIN action_synthetise_phyto_sans_amm aa2 on aa2.practicedintervention = pi.topiaid 
join entrepot_plantation_perenne_phases_synthetise eppps on eppps.id = pccp.topiaid;
    
DO $$
BEGIN
    BEGIN
		alter table entrepot_intervention_synthetise 
		add constraint intervention_synthetise_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

-- Les clés etrangeres qui ne concerne que les assolees ou perennes ne peuvent pas être ajoutees comme contraintes = il y a des NA dans la colonne
