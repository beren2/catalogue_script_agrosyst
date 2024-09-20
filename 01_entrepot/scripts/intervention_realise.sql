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
ei.spatialfrequency * ei.transitcount psci_intervention,
ei.workrate debit_de_chantier,
ei.workrateunit debit_de_chantier_unite,
ei.progressionspeed vitesse_avancement,
ei.involvedpeoplecount nb_personne_mobili,
ei.intermediatecrop concerne_ci,
ei.effectivecropcyclenode noeuds_realise_id,
'NA' plantation_perenne_phases_realise_id,
eitc.toolcouplings combinaison_outil_id
FROM effectiveintervention ei
left join effectiveintervention_toolcouplings eitc on eitc.effectiveintervention = ei.topiaid 
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
ei.spatialfrequency * ei.transitcount psci_intervention,
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
left join effectiveintervention_toolcouplings eitc on eitc.effectiveintervention = ei.topiaid
join entrepot_plantation_perenne_phases_realise epppr on epppr.id = eccp.topiaid;

alter table entrepot_intervention_realise
add constraint intervention_realise_PK
PRIMARY KEY (id);

alter table entrepot_intervention_realise
ADD FOREIGN KEY (combinaison_outil_id) REFERENCES entrepot_combinaison_outil(id);

-- Les clés etrangeres qui ne concerne que les assolees ou perennes ne peuvent pas être ajoutees comme contraintes = il y a des NA dans la colonne