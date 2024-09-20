create table entrepot_sole_synthetise(
	id character varying(255), 
	rang integer, 
	synthetise_id character varying(255),
	--suivant_id character varying(255),
	--precedent_id character varying(500),
	culture_id character varying(500),
	culture_code character varying(500)
);

insert into entrepot_sole_synthetise
	SELECT 
		pccn.topiaid AS id, 
		pccn.rank AS rang, 
		es.id AS synthetise_id,
		--pccc_source.target AS suivant_id,
		--pccc_target.target AS precedent_id,
		cpe.topiaid AS culture_id,
		cpe.code as culture_code
	FROM practicedcropcyclenode pccn
	left join practicedcropcycle pcc on pccn.practicedseasonalcropcycle = pcc.topiaid 
	--left join practicedcropcycleconnection pccc_source on pccn.topiaid = pccc_source.source
	--left join practicedcropcycleconnection pccc_target on pccn.topiaid = pccc_target.target
	join entrepot_synthetise es on pcc.practicedsystem = es.id
	join entrepot_sdc esdc on esdc.id = es.sdc_id
	join entrepot_domaine ed on esdc.domaine_id = ed.id
	join croppingplanentry cpe on (cpe.code = pccn.croppingplanentrycode and ed.id = cpe.domain);

alter table entrepot_sole_synthetise
add constraint sole_synthetise_PK
PRIMARY KEY (id);
