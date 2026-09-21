
# Procédure de mise à jour des données de traitements en Viticulture

## Ressources
2019 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2304/detail/

2016 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2004/detail/

2024 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2607/detail/

> Prendre le jeu de données nommé `cd2026-07_DonneesAssociees-principales_IFT-VITI_V2`

## Procédure de mise à jour des données

1. Pour chaque campagne `YYYY` étudiée :
    1. Télécharger les données diponibles aux liens ci-dessus (extention`xlsx` ou `ods`, dépendamment des annés)


    2. 
        **2019** :  Enregistrer la feuille "Tableau 2" sous le nom : `ift_culture_ancienne_region_viticulture_brut_2019.csv`

        **2016** : Enregistrer la feuille "Traitements phytosanitaires" sous le nom : `ift_culture_ancienne_region_viticulture_brut_2016.csv`

        **2024** : Enregistrer la feuille "IFT" sous le nom : `ift_culture_ancienne_region_viticulture_brut_2024.csv`

    3. Ajouter les informations relatives à l'étude de la campagne `YYYY`au paramètre STUDIES dans le notebook `./get_ift_anciennes_regions_maraichage.ipynb` 

    > Attention, il se peut que le formalisme d'Agreste évolue encore. On ne peut garantir que le script d'extraction des information fonctionne à chaque fois.

    > Attention, on ne prend que le mode de conduite "Ensemble", on ne tient pas compte donc de l'éventuel distinction d'ift entre Plein air, sous abri, sous serre...

3. Exécuter l'ensemble du notebook `./get_ift_anciennes_regions_maraichage.ipynb`

4.  le script se chargera d'enregistrer tous les fichiers `ift_culture_ancienne_region_maraichage_YYYY.csv` donnant, pour chaque région et chaque espèce étudiée, l'IFT moyen pour chaque région lors de la campagne `YYYY`. 

5. Vérifier la cohérence des fichiers obtenus (pas de valeurs aberrantes)


