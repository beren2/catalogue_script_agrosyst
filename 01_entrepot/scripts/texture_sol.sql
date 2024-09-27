CREATE TABLE entrepot_texture_sol AS
SELECT
	r.topiaid AS id,
	r.classes_texturales_gepaa AS classe_texturale_geppa,
	r.classe_indigo AS classe_indigo
FROM refsoltexturegeppa r
WHERE r.active IS true;
