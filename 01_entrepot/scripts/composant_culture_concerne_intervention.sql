
---------------------------
 -- Réalisé
 ---------------------------

DROP TABLE IF EXISTS entrepot_composant_culture_concerne_intervention_realise;

CREATE TABLE entrepot_composant_culture_concerne_intervention_realise (
	id text NULL, 
	stade_minimal text null, 
	stade_maximal text null,
	-- clé étrangère
	intervention_realise_id text null,
	composant_culture_id text null
);


insert into entrepot_composant_culture_concerne_intervention_realise (
	select 
	ess.topiaid id,
	ess.minstade stade_minimal, 
	ess.maxstade stade_maximal,
	ess.effectiveintervention intervention_realise_id, 
	ess.croppingplanspecies composant_culture_id
	from effectivespeciesstade ess
	left join entrepot_composant_culture ecc on ecc.id = ess.croppingplanspecies 
	join entrepot_intervention_realise eir  on eir.id = ess.effectiveintervention
);

alter table entrepot_composant_culture_concerne_intervention_realise
add constraint composant_culture_concerne_intervention_realise_PK
PRIMARY KEY (id);

alter table entrepot_composant_culture_concerne_intervention_realise
ADD FOREIGN KEY (stade_minimal) REFERENCES refstadeedi(topiaid);

alter table entrepot_composant_culture_concerne_intervention_realise
ADD FOREIGN KEY (stade_maximal) REFERENCES refstadeedi(topiaid);

alter table entrepot_composant_culture_concerne_intervention_realise
ADD FOREIGN KEY (composant_culture_id) REFERENCES entrepot_composant_culture(id);

alter table entrepot_composant_culture_concerne_intervention_realise
ADD FOREIGN KEY (intervention_realise_id) REFERENCES entrepot_intervention_realise(id);


 ---------------------------
 -- Synthétisé
 ---------------------------
 
DROP TABLE IF EXISTS entrepot_composant_culture_concerne_intervention_synthetise;
 
 
CREATE TABLE entrepot_composant_culture_concerne_intervention_synthetise (
	id text NULL, 
	stade_minimal text null, 
	stade_maximal text null,
	-- clé étrangère
	intervention_synthetise_id text null,
	composant_culture_code text null
);


insert into entrepot_composant_culture_concerne_intervention_synthetise (
	select 
	pss.topiaid id,
	pss.stademin stade_minimal, 
	pss.stademax stade_maximal,
	pss.practicedintervention intervention_synthetise_id, 
	pss.speciescode composant_culture_code
	from practicedspeciesstade pss
);


alter table entrepot_composant_culture_concerne_intervention_synthetise
add constraint composant_culture_concerne_intervention_synthetise_PK
PRIMARY KEY (id);

alter table entrepot_composant_culture_concerne_intervention_synthetise
ADD FOREIGN KEY (stade_minimal) REFERENCES refstadeedi(topiaid);

alter table entrepot_composant_culture_concerne_intervention_synthetise
ADD FOREIGN KEY (stade_maximal) REFERENCES refstadeedi(topiaid);
