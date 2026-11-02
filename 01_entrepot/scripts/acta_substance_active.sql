DROP TABLE IF EXISTS entrepot_acta_substance_active CASCADE;

CREATE TABLE entrepot_acta_substance_active AS
SELECT 
	rasa.topiaid AS id,
	rasa.id_produit,
	rasa.code_amm,
	rasa.nom_commun_sa,
	rasa.nom_produit, 
	rasa.concentration_valeur,
	rasa.concentration_unite,
	rasa.source,
	rasa.remarques,
	rasa.active
FROM refactasubstanceactive rasa;

DO $$
BEGIN
    BEGIN
		alter table entrepot_acta_substance_active
		add constraint acta_substance_active_PK_
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;