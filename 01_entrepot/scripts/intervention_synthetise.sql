CREATE INDEX if not exists entrepot_domaine_idx0 on entrepot_domaine(id);
CREATE INDEX if not exists entrepot_dispositif_idx0 on entrepot_dispositif(id);
CREATE INDEX if not exists entrepot_abstraction_action_idx0 on abstractaction(topiaid, mainaction);
CREATE INDEX if not exists entrepot_abstraction_action_idx3 on refinterventionagrosysttravailedi(topiaid);
CREATE INDEX if not exists entrepot_abstraction_action_idx4 on practicedcropcyclenode(topiaid);
CREATE INDEX if not exists entrepot_abstraction_action_idx5 on practicedcropcycleconnection(target);
CREATE INDEX if not exists entrepot_abstraction_action_idx6 on practicedcropcycleconnection(source);
CREATE INDEX if not exists entrepot_abstraction_action_idx7 on practicedintervention(practicedcropcycleconnection);

drop table if exists entrepot_intervention_synthetise;

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
pi.spatialfrequency * pi.temporalfrequency psci_intervention,
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
pi.spatialfrequency * pi.temporalfrequency psci_intervention,
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
join entrepot_plantation_perenne_phases_synthetise eppps on eppps.id = pccp.topiaid
;
    
alter table entrepot_intervention_synthetise 
add constraint intervention_synthetise_PK
PRIMARY KEY (id);

-- Les clés etrangeres qui ne concerne que les assolees ou perennes ne peuvent pas être ajoutees comme contraintes = il y a des NA dans la colonne