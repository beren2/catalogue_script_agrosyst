drop table if exists entrepot_variete;
CREATE TABLE entrepot_variete AS
(SELECT 
	rvg.topiaid AS id,
	rvg.nom_francais AS nom,
	rvg.code_gnis_variete AS code_gnis,
	rvg.nom_groupe, 
	rvg.nom_botanique, 
	rvg.denomination,
	rvg.reference_provisoire,
	rvg.liste,
	rvg.rubrique,
	rvg.libelle_rubrique,
	rvg.type_varietal,
	rvg.libelle_type_varietal,
	rvg.ploidie,
	rvg.libelle_ploidie
FROM refvarietegeves rvg)
UNION
(
	SELECT 
	rvp.topiaid as id, 
	NULL AS nom,
	NULL AS code_gnis,
	NULL AS nom_groupe, 
	NULL AS nom_botanique, 
	rvp.variete AS denomination,
	NULL AS reference_provisoire,
	NULL AS liste,
	NULL AS rubrique,
	NULL AS libelle_rubrique,
	NULL AS type_varietal,
	NULL AS libelle_type_varietal,
	NULL AS ploidie,
	NULL AS libelle_ploidie
	from refvarieteplantgrape rvp
);


alter table entrepot_variete
ADD CONSTRAINT entrepot_variete_PK
primary key (id);
