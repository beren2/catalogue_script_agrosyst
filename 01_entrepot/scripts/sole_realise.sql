DROP TABLE IF EXISTS entrepot_sole_realise CASCADE;

create table entrepot_sole_realise(
	id character varying(255), 
	rang integer, 
	zone_id character varying(255),
	suivant_id character varying(255),
	precedent_id character varying(500),
	culture_id character varying(500)
);

insert into entrepot_sole_realise
	SELECT 
		eccn.topiaid AS id, 
		eccn.rank AS rang, 
		escc.zone AS zone_id,
		eccc_source.target AS suivant_id,
		eccc_target.source AS precedent_id,
		eccn.croppingplanentry AS culture_id 
	FROM effectivecropcyclenode eccn 
	LEFT JOIN effectiveseasonalcropcycle escc ON eccn.effectiveseasonalcropcycle  = escc.topiaid 
	LEFT JOIN croppingplanentry cpe ON cpe.topiaid = eccn.croppingplanentry 
	LEFT JOIN effectivecropcycleconnection eccc_source ON eccn.topiaid = eccc_source.source -- toutes les connections dont on est la source
	LEFT JOIN effectivecropcycleconnection eccc_target ON eccn.topiaid = eccc_target.target -- toutes les connections dont on est la destination
	JOIN entrepot_zone ez on escc.zone =  ez.id;

DO $$
BEGIN
    BEGIN
		alter table entrepot_sole_realise
		add constraint sole_realise_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
