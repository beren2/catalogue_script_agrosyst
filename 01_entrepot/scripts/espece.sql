CREATE TABLE entrepot_espece AS
SELECT 
	re.topiaid AS id,
	re.code_espece_botanique, 
	re.code_qualifiant_aee,
	re.code_type_saisonnier_aee, 
	re.code_destination_aee,
	re.code_categorie_de_cultures AS code_categorie_culture,
	re.libelle_categorie_de_cultures AS libelle_categorie_culture, 
	re.commentaire,
	re.libelle_espece_botanique, 
	re.libelle_qualifiant_aee,
	re.libelle_type_saisonnier_aee, 
	re.libelle_destination_aee,
	re.code_cipan_aee, 
	re.libelle_cipan_aee,
	re.libelle_destination_bbch, 
	re.commentaires,
	re.genre, 
	re.espece,
	re.code_gnis, 
	re.num_groupe_gnis,
	re.nom_gnis, 
	re.nom_latin_gnis,
	re.nom_culture_acta, 
	re.remarque_culture_acta,
	re.typocan_espece,
	re.typocan_espece_maraich
FROM refespece re;

alter table entrepot_espece
add constraint espece_PK
PRIMARY KEY (id);
