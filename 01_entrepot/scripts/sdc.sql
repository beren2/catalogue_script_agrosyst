DROP TABLE IF EXISTS entrepot_sdc CASCADE;

CREATE TABLE entrepot_sdc AS
WITH sdc AS (
  SELECT
    gs.topiaid AS id,
    gs.code AS code,
    gs.name AS nom,
    edo.campagne,
    gs.modality AS modalite_suivi_dephy,
    gs.dephynumber AS code_dephy,
    gs.description AS commentaire,
    CASE gs.validated
      WHEN true then 'oui'
      WHEN false then 'non'
    END validite,
    gs.startingdate date_debut_pratique,
    gs.endingdate date_fin_pratique,
    gs.sector AS filiere,
    gs.production AS type_production,
    rt.reference_label AS type_agriculture,
    gs.categorystrategy AS strategie_categorie,
    gs.affectedarearate AS part_SAU_domaine,
    gs.affectedworkforcerate AS part_MO_domaine,
    gs.domainstoolsusagerate AS part_materiel_domaine,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Couverts associés,  plantes de service'),
             'non') couverts_associes,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Cultures intermédiaires a effet allélopathique ou biocide'),
             'non') ci_effet_allelo_ou_biocide,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Cultures intermédiaires attractives pour les auxiliaires'),
             'non') ci_attractives_pour_auxiliaires,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Cultures intermédiaires piège a nitrate'),
             'non') cipan,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Evitement par la date de semis - semis précoce'),
             'non') semis_precoce,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Evitement par la date de semis - semis tardif'),
             'non') semis_tardif,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Exportation des menu-pailles'),
             'non') exportation_menu_pailles,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Destruction de la litière des feuilles'),
             'non') destruction_litiere,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Efficience - Dose adaptée à la surface foliaire'),
             'non') dose_adaptee_surf_foliaire,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Filets anti-insectes'),
             'non') filet_anti_insectes,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Taille des organes contaminés'),
      'non') taille_organes_contamines,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Taille limitant les risques sanitaires'),
      'non') taille_limitant_risques_sanitaires,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Adaptation de la densité - faible densité'),
      'non') faible_densite,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Adaptation de la densité - forte densité'),
      'non') forte_densite,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND id_trait = '34'),
      'non') faible_ecartement,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND id_trait = '33'),
      'non') fort_ecartement,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND id_trait = '36'),
      'non') ajustement_fertilisation,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND id_trait = '35'),
      'non') ajustement_irrigation,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Autre forme de désherbage'),
      'non') desherbage_autre_forme,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Cultures pièges'),
      'non') cultures_pieges,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Désherbage mécanique fréquent'),
      'non') desherbage_meca_frequent,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Désherbage mécanique occasionel'),
      'non') desherbage_meca_occasionnel,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Désherbage thermique'),
      'non') desherbage_thermique,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Adaptation de la lutte à la parcelle'),
      'non') adaptation_lutte_a_la_parcelle,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND id_trait = '20'),
      'non') optim_conditions_application,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Réduction de dose autres produits phytosanitaires'),
      'non') reduction_dose_autres_phyto,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Réduction de dose fongicides'),
      'non') reduction_dose_fongi,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Réduction de dose herbicides'),
      'non') reduction_dose_herbi,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Réduction de dose insecticides'),
      'non') reduction_dose_insec,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Traitements localisés en intra-parcellaire'),
      'non') traitement_localise,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Utilisation d''adjuvants'),
      'non') utilisation_adjuvants,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Utilisation de seuils pour les décisions de traitement'),
      'non') utilisation_seuils,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Utilisation de stimulateur de défense'),
      'non') utilisation_stim_defense,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Efficience - Utilisation d''outil d''aide à la décision pour les traitements'),
      'non') utilisation_oad,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Levier génétique - Variétés compétitives sur adventices'),
      'non') var_competitives_adventice,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Levier génétique - Variétés peu sensibles à la verse'),
      'non') var_peu_sensibles_verse,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Levier génétique - Variétés peu sensibles aux maladies'),
      'non') var_peu_sensibles_maladies,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Levier génétique - Variétés peu sensibles aux ravageurs'),
      'non') var_peu_sensibles_ravageurs,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Lutte biologique par confusion sexuelle'),
      'non') lutte_bio_confu_sexuelle,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Lutte biologique autre'),
      'non') lutte_bio_autre,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Toutes cultures - Mélange d''espèces ou de variétés'),
      'non') melange,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Gestion spécifique des résidus supports d''inoculum (broyage, enfouissement)'),
      'non') gestion_residus,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Monoculture ou rotation courte'),
      'non') monoculture_rotation_courte,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Rotation avec cultures rustiques ou étouffantes (adventices)'),
      'non') rotation_cultures_rustiques,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Rotation diversifiée équilibrée avec prairie temporaire'),
      'non') rotation_diversifiee_avec_pt,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Rotation diversifiée équilibrée avec prairie temporaire'),
      'non') rotation_diversifiee_sans_pt,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Rotation diversifiée par l''introduction d''une culture dans une rotation courte'),
      'non') rotation_diversifiee_intro_une_culture,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Enherbement (espèces semées)'),
      'non') enherbement_seme,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures pérennes - Enherbement naturel maîtrisé'),
      'non') enherbement_naturel,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Agroforesterie'),
      'non') agroforesterie,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Arbres isolés ou alignements en bordure de parcelle'),
      'non') arbres_bordure_parcelle,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Broyage des bordures'),
      'non') broyage_bordure,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Gestion des bordures de bois pour favoriser la biodiversité'),
      'non') gestion_bordure_de_bois,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Présence de haies anciennes'),
      'non') haies_anciennes,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Présence de jeunes haies'),
      'non') haies_jeunes,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Proximité de bandes enherbées favorisant les auxiliaires'),
      'non') bandes_enherbees,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Proximité de bandes fleuries favorisant les auxiliaires'),
      'non') bandes_fleuries,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Proximité de bois et bosquets'),
      'non') bois_bosquet,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Décompactage  occasionnel'),
      'non') decompactage_occasionnel,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Décompactage  profond fréquent (fréquence > 50%)'),
      'non') decompactage_frequent,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Faux semis ponctuels'),
      'non') faux_semis_ponctuels,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Faux semis intensifs (travaux superficiels répétés spécifiques)'),
      'non') faux_semis_intensifs,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Labour occasionnel'),
      'non') labour_occasionnel,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Labour fréquent (fréquence > 50%)'),
      'non') labour_frequent,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Labour systématique (fréquence > 80%)'),
      'non') labour_systematique,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Semis direct sans travail du sol occasionnel'),
      'non') semis_direct_occasionnel,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Semis direct sans travail du sol systématique'),
      'non') semis_direct_systematique,

    COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Strip till occasionnel'),
      'non') strip_till_occasionnel,

	COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Strip till fréquent ou systématique'),
      'non') strip_till_frequent,

	COALESCE ((SELECT CASE WHEN nom_trait IS NOT NULL THEN 'oui' END
        FROM reftraitsdc rts2
        JOIN characteristics_growingsystem cgs2 ON rts2.topiaid = cgs2.characteristics
        WHERE cgs2.growingsystem = gs.topiaid
        AND nom_trait = 'Cultures assolées - Techniques culturales superficielles uniquement'),
      'non') tcs,
      ed.id as dispositif_id
  FROM growingsystem gs
  JOIN entrepot_dispositif ed on gs.growingplan = ed.id --fusion pour n'obtenir que des dispositifs actifs
  LEFT JOIN entrepot_domaine edo on ed.domaine_id = edo.id
  LEFT JOIN reftypeagriculture rt ON gs.typeagriculture = rt.topiaid
  where gs.active = true

  GROUP BY edo.id, edo.campagne, ed.id,
  gs.topiaid, gs.code, gs.name, gs.dephynumber, gs.description,
  gs.validated, gs.sector,
  rt.reference_label,
  gs.categorystrategy,
  gs.affectedarearate

),
  reseaux_parents AS
    (SELECT n.topiaid, n.name reseau_ir, n.codeconventiondephy, string_agg(distinct n2.name,'|') reseau_it
      FROM network_parents np
      JOIN network n ON n.topiaid = np.network
      JOIN network n2 ON np.parents = n2.topiaid
      GROUP BY n.topiaid, n.name
    ),
  modes_commercialisation AS
    (SELECT dest.growingsystem,
      json_object_agg(
        dest.marketingdestination,
        CASE WHEN (dest.selectedforgs IS TRUE OR (dest.part IS NOT NULL AND dest.part>0)) THEN coalesce(dest.part::varchar(5),'OUI') ELSE 'NON' END
        ORDER BY dest.marketingdestination) modes_comm
    from (
      select mdo.growingsystem,  rfd.sector, rfd.marketingdestination, mdo.selectedforgs,	mdo.part
      from MarketingDestinationObjective mdo
      JOIN RefMarketingDestination rfd ON mdo.refmarketingdestination = rfd.topiaid
      ) dest
     GROUP BY dest.growingsystem)

    SELECT
      sdc.*,
      (select string_agg(distinct rp.reseau_ir, '|')
        FROM reseaux_parents rp
        JOIN growingsystem_networks gn ON rp.topiaid = gn.networks
        where gn.growingsystem = sdc.id
      ) reseaux_IR,

      (select string_agg(distinct rp.reseau_it, '|')
        FROM reseaux_parents rp
        JOIN growingsystem_networks gn ON rp.topiaid = gn.networks
        where gn.growingsystem = sdc.id
      ) reseaux_IT,

      (select string_agg(distinct rp.codeconventiondephy, '|')
        FROM reseaux_parents rp
        JOIN growingsystem_networks gn ON rp.topiaid = gn.networks
        where gn.growingsystem = sdc.id
      ) codes_convention_dephy,

      (select modes_comm
        FROM modes_commercialisation mc
        where mc.growingsystem = sdc.id
      ) modes_commercialisation
    FROM sdc;

DO $$
BEGIN
    BEGIN
        alter table entrepot_sdc
        ADD CONSTRAINT sdc_PK
        primary key (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_sdc
add FOREIGN KEY (dispositif_id) REFERENCES entrepot_dispositif(id);
