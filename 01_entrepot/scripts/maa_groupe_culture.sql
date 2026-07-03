DROP TABLE IF EXISTS entrepot_maa_groupe_culture CASCADE;

CREATE TABLE entrepot_maa_groupe_culture AS 
SELECT 
	ragc.topiaid AS id,
	ragc.code_culture_maa, 
	ragc.id_groupe_culture,
	ragc.nom_cuture AS nom_culture, 
	ragc.nom_groupe_culture,
	ragc.commentaires,
	ragc.active
FROM refmaagroupecultures ragc;

DO $$
BEGIN
    BEGIN
		alter table entrepot_maa_groupe_culture
		add constraint maa_groupe_culture_PK_
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;