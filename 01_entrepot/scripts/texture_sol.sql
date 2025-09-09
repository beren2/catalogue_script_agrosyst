CREATE TABLE entrepot_texture_sol AS
SELECT
	r.topiaid AS id,
	r.classes_texturales_gepaa AS classe_texturale_geppa,
	r.classe_indigo AS classe_indigo
FROM refsoltexturegeppa r
WHERE r.active IS true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_texture_sol
        add constraint texture_sol_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;