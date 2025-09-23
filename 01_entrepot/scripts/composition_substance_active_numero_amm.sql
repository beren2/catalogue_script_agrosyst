CREATE TABLE entrepot_composition_substance_active_numero_amm AS
SELECT 
	rcsapna.topiaid AS id,
	rcsapna.numero_amm,
	rcsapna.id_sa,
	rcsapna.nom_sa,
	rcsapna.variant_sa,
	rcsapna.dose_sa,
	rcsapna.unite_sa,
	rcsapna.source,
	rcsapna.active
FROM refcompositionsubstancesactivesparnumeroamm rcsapna;

DO $$
BEGIN
    BEGIN
		alter table entrepot_composition_substance_active_numero_amm
		add constraint composition_substance_active_numero_amm_PK_
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
