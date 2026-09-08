## Agreste

Pour certains magasins (exemple : tableau de bord magasin can), il est nécessaire de disposer des données des pratiques culturale, publiées par Agreste tous les 5 ans environs.
Les données doivent être mises à jour manuellement car Agreste n'expose pas d'API permettant d'envisager une automatisation. 
De plus, les fichiers obtenus ont des structures complexes dont la stabilité dans le temps n'est pas assurée.
> Il est donc important de vérifier, lors de toute mise à jour, que la structure des nouveaux fichiers est bien conforme aux anciens fichiers.

## IFT : 

- Viticulture et arboriculture : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2607/detail/
- Grandes cultures et polyculutre élevage : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2407/detail/
- Maraîchage : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2504/detail/
- Culture tropicales ?
- Horticulture ?

## Surfaces

- https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/ :

> - Télécharger le fichier principal
> - le décompresser
> - ouvrir celui se terminant par "_provisoires_donnees_regionales"
> - se placer sur la feuille "COP" et l'exporter en la nommant "surface_culture_regionales_agreste.csv"
> - executer le jupyter notebook "./get_surface_espece_ancienne_region.ipynb"
> - le script se chargera d'enregistrer un fichier surface_espece_ancienne_region.csv 