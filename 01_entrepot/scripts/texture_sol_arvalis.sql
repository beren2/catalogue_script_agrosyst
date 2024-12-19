CREATE TABLE entrepot_texture_sol_arvalis AS
SELECT
	r.topiaid AS id,
	r.id_type_sol AS id_type_sol,
	r.sol_nom AS nom,
	r.sol_region AS region
FROM refsolarvalis r
WHERE r.active IS true;
