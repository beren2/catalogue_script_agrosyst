
# Procédure de mise à jour des données de traitements en Maraîchage

## Ressources
2018 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2312/detail/

> Attention, pour celle-ci, on ne dispose pas d'IFT clairement calculés

2022 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2504/detail/


## Procédure de mise à jour des données

1. Pour chaque campagne `YYYY` étudiée :
    1. Télécharger les données diponibles aux liens ci-dessus (extention`xlsx` ou `ods`, dépendamment des annés)

    2. Enregistrer la feuille "IFT_ancienne_regions" sous le nom : `ift_culture_ancienne_region_maraichage_brut_YYYY.csv`

    3. Ajouter les informations relatives à l'étude de la campagne `YYYY`au paramètre STUDIES dans le notebook `./get_ift_anciennes_regions_maraichage.ipynb` 

    > Attention, il se peut que le formalisme d'Agreste évolue encore. On ne peut garantir que le script d'extraction des information fonctionne à chaque fois.

    > Attention, on ne prend que le mode de conduite "Ensemble", on ne tient pas compte donc de l'éventuel distinction d'ift entre Plein air, sous abri, sous serre...

3. Exécuter l'ensemble du notebook `./get_ift_anciennes_regions_maraichage.ipynb`

4.  le script se chargera d'enregistrer tous les fichiers `ift_culture_ancienne_region_maraichage_YYYY.csv` donnant, pour chaque région et chaque espèce étudiée, l'IFT moyen pour chaque région lors de la campagne `YYYY`. 

5. Vérifier la cohérence des fichiers obtenus (pas de valeurs aberrantes)


