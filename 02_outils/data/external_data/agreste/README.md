## Agreste

Pour certains magasins (exemple : tableau de bord magasin can), il est nécessaire de disposer des données des pratiques culturale, publiées par Agreste tous les 5 ans environs.
Les données doivent être mises à jour manuellement car Agreste n'expose pas d'API permettant d'envisager une automatisation. 
De plus, les fichiers obtenus ont des structures complexes dont la stabilité dans le temps n'est pas assurée.
> Il est donc important de vérifier, lors de toute mise à jour, que la structure des nouveaux fichiers est bien conforme aux anciens fichiers.

Le présent document fait l'inventaire des ressources nécessaires et des procédures nécessaires à l'actualisation. 

> TODO : réfléchir à comment ancrer dans la routine de l'équipe la vérification de la disponibilité de ressources Agreste + à jour.

## IFT : 
Se rendre dans le dossier ift



### Viticulture
- Viticulture et arboriculture : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2607/detail/

> TODO :

### GCPE

Se rendre dans le dossier gcpe

fichier : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2407/detail/

**Procédure de mise à jour**
1. Télécharger les données diponible au lien ci-dessus. Le nom du fichier doit ressembler à `cd2024-7_DonneesPKGC-IFT_Tableaux_principauxxlsx`
2. Enregistrer sous la feuille "IFT_ancienne_regions" sous le nom : "ift_anciennes_regions_brut.csv"
3. Exécuter le script `./get_ift_anciennes_regions.ipynb`
4.  le script se chargera d'enregistrer un fichier `ift_anciennes_regions.csv` donnant, pour chaque région et chaque espèce étudiée, l'IFT moyen pour chaque région.

> TODO

### Maraîchage
- Maraîchage : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2504/detail/

> TODO


### Cultures tropicales
- Cultures tropicales ?
> TODO

### Horticulture
- Horticulture ?
> TODO

## Surfaces
Se rendre dans le dossier surface

- https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/ :

**Procédure de mise à jour**
1. Télécharger le fichier principal
2. le décompresser
3. ouvrir celui se terminant par "_provisoires_donnees_regionales"
4. se placer sur la feuille "COP" et l'exporter en la nommant "surface_culture_regionales_agreste.csv"
5. executer le jupyter notebook `./get_surface_espece_ancienne_region.ipynb`
6. le script se chargera d'enregistrer un fichier `surface_espece_ancienne_region.csv`