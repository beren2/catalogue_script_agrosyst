CREATE TABLE entrepot_combinaison_outil AS
select 
tc.topiaid id,
tc.toolscouplingname nom,
tc.code code,
tc.manualintervention intervention_manuelle,
tc.tractor tracteur_composant_parc_materiel_id,
tc.workforce nb_personnes,
tc.workrate debit,
tc.workrateunit debit_unite,
tc.boiledquantity bouillie_volume_moy_parha_hl,
tc.antidriftnozzle buse_anti_derive_pulverisateur,
tc.transitvolume volume_voyage,
tc.serviceprovider prestation_service,
tc."domain" domaine_id
from toolscoupling tc 
join entrepot_domaine ed on ed.id = tc."domain" 
left join entrepot_composant_parc_materiel em on em.id = tc.tractor ;

alter table entrepot_combinaison_outil
add constraint combinaison_outil_PK
PRIMARY KEY (id);

alter table entrepot_combinaison_outil
ADD FOREIGN KEY (tracteur_composant_parc_materiel_id) REFERENCES entrepot_composant_parc_materiel(id);

alter table entrepot_combinaison_outil
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);

-- une combinaison d'outils peut avoir plusieurs outils associé à un outils motorise
DROP TABLE IF EXISTS entrepot_combinaison_outil_composant_parc_materiel;
CREATE TABLE entrepot_combinaison_outil_composant_parc_materiel AS
select 
et.toolscoupling combinaison_outil_id,
et.equipments composant_parc_materiel_id
from equipments_toolscoupling et  
join entrepot_composant_parc_materiel em on em.id = et.equipments 
join entrepot_combinaison_outil eco on eco.id = et.toolscoupling;

alter table entrepot_combinaison_outil_composant_parc_materiel
ADD FOREIGN KEY (combinaison_outil_id) REFERENCES entrepot_combinaison_outil(id);

alter table entrepot_combinaison_outil_composant_parc_materiel
ADD FOREIGN KEY (composant_parc_materiel_id) REFERENCES entrepot_composant_parc_materiel(id);

alter table entrepot_combinaison_outil_composant_parc_materiel
add constraint combinaison_outil_composant_parc_materiel_PK
PRIMARY KEY (combinaison_outil_id,composant_parc_materiel_id);

-- une combinaison d'outils peut avoir plusieurs actions principales renseignées
DROP TABLE IF EXISTS entrepot_combinaison_outil_action;
CREATE TABLE entrepot_combinaison_outil_action AS
select distinct 
mtc.toolscoupling combinaison_outil_id,
mtc.mainsactions intervention_travail_edi_id
from mainsactions_toolscoupling mtc 
join entrepot_intervention_travail_edi refint on mtc.mainsactions = refint.id ;

alter table entrepot_combinaison_outil_action
add constraint combinaison_outil_action_PK
PRIMARY KEY (combinaison_outil_id,intervention_travail_edi_id);