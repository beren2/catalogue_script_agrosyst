
# Procédure de mise à jour des données de surface en GCPE

## Ressources
- https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/ :

## Procédure de mise à jour des données

> Vérifier sur Agreste qu'il n'y a pas de version actualisée pour l'année en cours

### Données principales
1. Télécharger le fichier principal du lien ci-dessus
2. le décompresser
3. ouvrir celui se terminant par "_provisoires_donnees_regionales"
4. se placer sur la feuille "COP" et l'exporter en la nommant "surface_culture_regionales_agreste.csv"
5. executer le jupyter notebook `./get_surface_espece_ancienne_region.ipynb`
6. le script se chargera d'enregistrer un fichier `surface_espece_ancienne_region.csv`

### Données secondaires
Le jeu de donné principal est lacunaire : 
- il ne permet pas de disposer des surfaces 