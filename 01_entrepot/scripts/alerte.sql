CREATE TABLE entrepot_alerte AS
SELECT 
	topiaid as id,
	nom_alerte,
	id_alerte as num_alerte,
	variable_agrosyst as variable_concernee,
	echelle_calcul,
	filiere,
	bio,
	rendement_unite,
	code_espece_botanique,
	libelle_espece_botanique,
	code_qualifiant_aee,
	libelle_qualifiant_aee,
	code_type_saisonnier_aee,
	libelle_type_saisonnier_aee,
	seuil_min,
	seuil_min_inclus,
	seuil_max,
	seuil_max_inclus,
	valeur_si_dans_seuil,
	valeur_si_inferieur_a_seuil,
	valeur_si_superieur_a_seuil
FROM refalerte
WHERE active=True;

DO $$
BEGIN
    BEGIN
		alter table entrepot_alerte
		add constraint alerte_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
