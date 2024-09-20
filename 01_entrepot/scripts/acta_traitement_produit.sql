CREATE TABLE entrepot_acta_traitement_produit AS
SELECT 
	ratp.topiaid AS id,
	ratp.id_produit,
	ratp.id_traitement,
	ratp.nom_produit,
	ratp.code_traitement,
	ratp.nom_traitement,
	ratp.nodu,
	ratp.source,
	ratp.code_amm, 
	ratp.code_traitement_maa, 
	ratp.nom_traitement_maa,
	ratp.etat_usage,
	ratp.refcountry as country_id,
	ratp.active
FROM refactatraitementsproduit ratp;

alter table entrepot_acta_traitement_produit
add constraint acta_traitement_produit_PK_
PRIMARY KEY (id);
