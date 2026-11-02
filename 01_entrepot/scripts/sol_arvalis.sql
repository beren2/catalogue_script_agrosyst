DROP TABLE IF EXISTS entrepot_sol_arvalis CASCADE;

CREATE TABLE entrepot_sol_arvalis AS
	select 
		r.topiaid as id, 
		r.id_type_sol as type_sol, 
		r.sol_nom as nom,
		r.sol_calcaire as calcaire,
		r.sol_hydromorphie as hydromorphie, 
		r.sol_pierrosite as pierrosite, 
		r.sol_profondeur as profondeur, 
		r.sol_texture as texture, 
		r.sol_region as region, 
		r.sol_region_code as region_code,
		r.source as source,
		r.sol_calcaire_typecode as calcaire_type_code, 
		r.sol_hydromorphie_typecode as hydromorphie_type_code, 
		r.sol_profondeur_typecode as profondeur_type_code, 
		r.sol_texture_typecode as texture_type_code
	from refsolarvalis r
	where r.active is true;

DO $$
BEGIN
    BEGIN
		alter table entrepot_sol_arvalis
		add constraint sol_arvalis_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
