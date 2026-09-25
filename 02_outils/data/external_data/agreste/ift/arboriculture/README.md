
# Procédure de mise à jour des données de traitements en Arboriculture

## Ressources
2018 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2108/detail/

> Prendre le jeu de données nommé `Evolution traitement - Résultats principaux V2`

2024 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2607/detail/
> Prendre le jeu de données nommé `cd2026-07_DonneesAssociees-principales_IFT-ARBO_V2`

## Procédure de mise à jour des données

1. Pour chaque campagne `YYYY` étudiée :
    1. Télécharger les données diponibles aux liens ci-dessus (extention`xlsx` ou `ods` ou `zip`, dépendamment des annés)

    2. 
        **Spécifique 2018** : 
        - Ouvrir le fichier `Traitements_IFT_region.ods`
        - dégroupper les colonnes Pomme et Prune et les duppliquer dans les colonnes manquantes de façon à avoir toujours l'information dans les sous-colonnes.
        - enregistrer la feuille "IFT par région" dans le répertoire `./brut` sous le nom : `ift_culture_ancienne_region_arboriculture_brut_2018.csv`

    3. 
        **Spécifique 2024** : Ouvrir le fichier `cd2026-07_DonneesAssociees-principales_IFT-ARBO_V2.xlsx`. IL y a une feuille par culture (Cerise, Pomme à cidre, Olive, Clémentine, Pomme de table, Abricot, Raisin de table, Agrumes, Prune, Pêche, Banane). 
        Il faut exporter chacune des ces feuilles dans le répertoire `./brut` sous le nom `ift_`*nom_de_la_culture*`_ancienne_region_arboriculture_brut_2024.csv`. 

    3. Ajouter les informations relatives à l'étude de la campagne `YYYY`au paramètre STUDIES dans le notebook `./get_ift_anciennes_regions_maraichage.ipynb` 

    > Attention, il se peut que le formalisme d'Agreste évolue encore. On ne peut garantir que le script d'extraction des information fonctionne à chaque fois.

    > Attention, on ne prend que le mode de conduite "Ensemble", on ne tient pas compte donc de l'éventuel distinction d'ift entre Plein air, sous abri, sous serre...

3. Exécuter l'ensemble du notebook `./get_ift_anciennes_regions_maraichage.ipynb`

4.  le script se chargera d'enregistrer tous les fichiers `ift_culture_ancienne_region_maraichage_YYYY.csv` donnant, pour chaque région et chaque espèce étudiée, l'IFT moyen pour chaque région lors de la campagne `YYYY`. 

5. Vérifier la cohérence des fichiers obtenus (pas de valeurs aberrantes)


