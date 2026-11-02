DROP TABLE IF EXISTS entrepot_acta_groupe_culture CASCADE;

CREATE TABLE entrepot_acta_groupe_culture AS 
SELECT 
	ragc.topiaid AS id,
	ragc.id_culture, 
	ragc.id_groupe_culture,
	ragc.nom_cuture AS nom_culture, 
	ragc.nom_groupe_culture,
	ragc.commentaires,
	ragc.active
FROM refactagroupecultures ragc;

DO $$
BEGIN
    BEGIN
		alter table entrepot_acta_groupe_culture
		add constraint acta_groupe_culture_PK_
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;