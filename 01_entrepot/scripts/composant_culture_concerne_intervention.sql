
---------------------------
 -- Réalisé
 ---------------------------

DROP TABLE IF EXISTS entrepot_composant_culture_concerne_intervention_realise CASCADE;

CREATE TABLE entrepot_composant_culture_concerne_intervention_realise (
	id text NULL, 
	stade_minimal text null, 
	stade_maximal text null,
	-- clé étrangère
	intervention_realise_id text null,
	composant_culture_id text null
);



INSERT INTO entrepot_composant_culture_concerne_intervention_realise
    (id, stade_minimal, stade_maximal, intervention_realise_id, composant_culture_id)
SELECT DISTINCT ON (ess.effectiveintervention, ess.croppingplanspecies, ess.minstade, ess.maxstade)
	ess.topiaid               AS id,
	ess.minstade              AS stade_minimal,
	ess.maxstade              AS stade_maximal,
	ess.effectiveintervention AS intervention_realise_id,
	ess.croppingplanspecies   AS composant_culture_id
	from effectivespeciesstade ess
	left join entrepot_composant_culture ecc on ecc.id = ess.croppingplanspecies 
	join entrepot_intervention_realise eir  on eir.id = ess.effectiveintervention
	order by 
	  ess.effectiveintervention,
  	  ess.croppingplanspecies,
  	  ess.minstade,
  	  ess.maxstade,
  	  ess.topiaid;
;

DO $$
BEGIN
    BEGIN
		alter table entrepot_composant_culture_concerne_intervention_realise
		add constraint composant_culture_concerne_intervention_realise_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;


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
 
DROP TABLE IF EXISTS entrepot_composant_culture_concerne_intervention_synthetise CASCADE;
 
 
CREATE TABLE entrepot_composant_culture_concerne_intervention_synthetise (
	id text NULL, 
	stade_minimal text null, 
	stade_maximal text null,
	-- clé étrangère
	intervention_synthetise_id text null,
	composant_culture_code text null
);

-- Table temporaire avec unicité sur la colonne code pour join sur ceux présents, pareil pour les interventions
DROP TABLE IF EXISTS tmp_composant_culture_code_unique CASCADE;

CREATE TEMP TABLE tmp_composant_culture_code_unique AS
SELECT DISTINCT ON (code)
    id,
    code
FROM entrepot_composant_culture
ORDER BY code, id;

ALTER TABLE tmp_composant_culture_code_unique
ADD CONSTRAINT tmp_composant_culture_code_unique_pk
PRIMARY KEY (code);

-- Remplissage avec join des 2 tables concernées
insert into entrepot_composant_culture_concerne_intervention_synthetise (
	select 
	pss.topiaid id,
	pss.stademin stade_minimal, 
	pss.stademax stade_maximal,
	pss.practicedintervention intervention_synthetise_id, 
	pss.speciescode composant_culture_code
	from practicedspeciesstade pss
	LEFT JOIN tmp_composant_culture_code_unique ecc ON ecc.code = pss.speciescode
	JOIN entrepot_intervention_synthetise eis ON eis.id = pss.practicedintervention
);

DO $$
BEGIN
    BEGIN
		alter table entrepot_composant_culture_concerne_intervention_synthetise
		add constraint composant_culture_concerne_intervention_synthetise_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;


alter table entrepot_composant_culture_concerne_intervention_synthetise
ADD FOREIGN KEY (stade_minimal) REFERENCES refstadeedi(topiaid);

alter table entrepot_composant_culture_concerne_intervention_synthetise
ADD FOREIGN KEY (stade_maximal) REFERENCES refstadeedi(topiaid);
