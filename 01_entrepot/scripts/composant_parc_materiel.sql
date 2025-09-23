CREATE TABLE entrepot_composant_parc_materiel AS
SELECT 
e.topiaid as id,
e.code,
e."name" as nom,
d.campagne,
CASE e.materieleta
      WHEN true THEN 'oui'
      WHEN false THEN 'non'
END appartient_eta_cuma,
case 
	when e.refmateriel like '%Traction%' then 'Tracteur'
	when e.refmateriel like '%Automoteur%' then 'Automoteur'
	when e.refmateriel like '%Outil%' then 'Outil'
	when e.refmateriel like '%Irrigation%' then 'Irrigation'
end categorie,
rm.topiaid as materiel_id,
d.id as domaine_id
FROM equipment e
JOIN entrepot_domaine d on e."domain" = d.id -- obtention uniquement des domaines actifs
JOIN refmateriel rm ON e.refmateriel = rm.topiaid;

DO $$
BEGIN
    BEGIN
		alter table entrepot_composant_parc_materiel
		add constraint composant_parc_materiel_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_composant_parc_materiel
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);

alter table entrepot_composant_parc_materiel
ADD FOREIGN KEY (materiel_id) REFERENCES entrepot_materiel(id);
