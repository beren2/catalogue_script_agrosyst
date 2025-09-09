CREATE TABLE entrepot_texture_sol_arvalis AS
SELECT
	r.topiaid AS id,
	r.id_type_sol AS id_type_sol,
	r.sol_nom AS nom,
	r.sol_region AS region
FROM refsolarvalis r
WHERE r.active IS true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_texture_sol_arvalis
        add constraint texture_sol_arvalis_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
