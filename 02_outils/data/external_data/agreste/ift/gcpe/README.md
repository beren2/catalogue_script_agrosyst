
# Procédure de mise à jour des données de traitements en GCPE

## Ressources
2017 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd1903/detail/

2021 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2407/detail/


## Procédure de mise à jour des données


1. Pour chaque campagne `YYYY` étudiée :
    1. Télécharger les données diponibles aux liens ci-dessus (extention`xlsx` ou `ods`, dépendamment des annés)

    2. Enregistrer la feuille "IFT_ancienne_regions" sous le nom : `ift_culture_ancienne_region_gcpe_brut_YYYY.csv`

    3. Ajouter les informations relatives à l'étude de la campagne `YYYY`au paramètre STUDIES dans le notebook `./get_ift_anciennes_regions_gcpe.ipynb` 

    > Attention, il se peut que le formalisme d'Agreste évolue encore. On ne peut garantir que le script d'extraction des information fonctionne à chaque fois.

3. Exécuter l'ensemble du notebook `./get_ift_anciennes_regions_gcpe.ipynb`

4.  le script se chargera d'enregistrer tous les fichiers `ift_culture_ancienne_region_gcpe_YYYY.csv` donnant, pour chaque région et chaque espèce étudiée, l'IFT moyen pour chaque région lors de la campagne `YYYY`. 

5. Vérifier la cohérence des fichiers obtenus (pas de valeurs aberrantes)


> TODO : comment gérer le cas où on a pas exactement les mêmes espèces en sorties ?