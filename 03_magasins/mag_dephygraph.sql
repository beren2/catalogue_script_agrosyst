ALTER TABLE magasin_dephygraph
ALTER COLUMN c105_administrativeRegion TYPE text;

UPDATE magasin_dephygraph
SET c105_administrativeRegion =
    CASE c105_administrativeRegion
        WHEN 84 THEN 'Auvergne-Rhône-Alpes'
        WHEN 32 THEN 'Hauts-de-France'
        WHEN 93 THEN 'Provence-Alpes-Côte d''Azur'
        WHEN 44 THEN 'Grand Est'
        WHEN 76 THEN 'Occitanie'
        WHEN 28 THEN 'Normandie'
        WHEN 75 THEN 'Nouvelle-Aquitaine'
        WHEN 24 THEN 'Centre-Val de Loire'
        WHEN 27 THEN 'Bourgogne-Franche-Comté'
        WHEN 53 THEN 'Bretagne'
        WHEN 94 THEN 'Corse'
        WHEN 52 THEN 'Pays de la Loire'
        WHEN 11 THEN 'Île-de-France'
        WHEN 1 THEN 'Guadeloupe'
        WHEN 2 THEN 'Martinique'
        WHEN 3 THEN 'Guyane'
        WHEN 4 THEN 'La Réunion'
        WHEN 6 THEN 'Mayotte'
        ELSE NULL
    END;

    