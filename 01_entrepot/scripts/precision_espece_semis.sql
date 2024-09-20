DROP TABLE IF EXISTS entrepot_precision_espece_semis;
CREATE TABLE entrepot_precision_espece_semis (
	id character varying(255),
	quantite double precision,
	profondeur double precision,
	semence_id character varying(255), -- clé étrangère vers la semence considérée
	utilisation_intrant_id character varying(255), --clé étrangère vers l'utilisation d'intrant considérées
	unite_application character varying(255) -- unité d'application déclaré au local à intrants 
);

insert into entrepot_precision_espece_semis(id, quantite, profondeur, semence_id, utilisation_intrant_id, unite_application)
	select 
		ssiu.topiaid as id,
		aiu.qtavg as quantite,
		ssiu.deepness as profondeur, 
		ssiu.domainseedspeciesinput as semence_id,
		ssiu.seedlotinputusage as utilisation_intrant_id, 
		dsli.usageunit as unite_application
	from seedspeciesinputusage ssiu
	join abstractinputusage aiu on ssiu.seedlotinputusage = aiu.topiaid
	join seedlotinputusage sliu on ssiu.seedlotinputusage = sliu.topiaid
	join domainseedlotinput dsli on sliu.domainseedlotinput = dsli.topiaid;


alter table entrepot_precision_espece_semis
add constraint entrepot_precision_espece_semis_pk
PRIMARY KEY (id);

 


