
# Procédure de mise à jour des données de surface en GCPE

## Ressources
1. https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/
2. https://agreste.agriculture.gouv.fr/agreste-saiku/?plugin=true&query=query/open/SAANR_FOURRAGE_2#query/open/SAANR_FOURRAGE_2
3. https://agreste.agriculture.gouv.fr/agreste-saiku/?plugin=true&query=query/open/SAANR_DEVELOPPE_2#query/open/SAANR_DEVELOPPE_2

## Procédure de mise à jour des données

> Vérifier sur Agreste qu'il n'y a pas de version actualisée pour l'année en cours

### Données principales (ressource 1)
1. Télécharger le fichier principal du lien ci-dessus
2. le décompresser
3. ouvrir celui se terminant par "_provisoires_donnees_departementales"
4. se placer sur la feuille "COP" et l'exporter dan le répertoire courant en la nommant `surface_culture_departementales_agreste.csv`.


### Données secondaires (ressources 2 et 3)
Certaines données ne sont pas disponibles dans le jeu de données principal, on doit donc les obtenir via l'interface de manipulation fournie par Agreste (plus d'information dans le [README principal](../../README.md)).

> Si les liens dans les resources sont inaccessibles, taper "SAANR" dans [l'interface de recherche d'Agreste](https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAANR/searchUiid/search/). Chercher des noms du type : `Culture développées` (ressource 3) et `Fourrage et prairies` (ressource 2).

> Attention, les données supplémentaires ne sont disponibles que pour les campagnes antérieures à 2020.

Les données à obtenir via ce canal secondaires sont les surface développées pour les cultures suivantes :
- Betterave sucrière (ressource 3)
- Maïs fourrage (ressource 2)
- Pomme de terre (ressource 3)
- Canne à sucre (ressource 3)
- Soja (ressource 3)
- Lin Fibre (ressource 3)

#### Procédure détaillée pour obtenir les données de la resource 2 
- Ouvrir le [lien](https://agreste.agriculture.gouv.fr/agreste-saiku/?plugin=true&query=query/open/SAANR_FOURRAGE_2#query/open/SAANR_FOURRAGE_2) indiqué dans les ressouces.
- Cliquer-glisser **Année de référence** de l'item `Filtre` jusqu'à l'item `Colonne`.
- Cliquer sur **Année de référence** pour faire passer à droite toutes les donnée postérieures à 2010.
- Cliquer sur **Groupe d'indicateurs** dans l'item `Colonnes` et faire passer à droite uniquement la valeur *Superficie correspondante (hectare)*
- Cliquer-glisser "Département" dans l'item `Colonnes`
- Supprimer toute les lignes dans l'item `Lignes`
- Cliquer-glisser **Cultures développées 3** qui correspond à un niveau de détail suffisant pour les données qui nous intéressent

À l'issue de ces étapes, vous devriez avoir :
- dans l'item `Colonnes` : 
    - Groupe d'indicateur (*Superficie correspondante (hectare)*)
    - Année de référence (*toutes*)
    - Département (*tous*)

- dans l'item `Lignes` :
    - Cultures développées 3 (*tous*)

Rien dan les autres item.

Ensuite :
- Cliquer sur le bouton `Exporter sous Libre Office` dans le menu en haut. 
- Ouvrir le document et exporter à nouveau en csv l'onglet "Données" sous le nom `surface_fourrage_departementales_agreste.csv`

> **Pour aller plus vite** : vous pouvez annuler la requête à chaque fois tant que vous n'avez pas terminé votre configuration.

> **Note** : on n'exporter pas directement en csv depuis l'interface d'Agreste car le format de sortie est plus complexe à manipuler. 

#### Procédure détaillée pour obtenir les données de la resource 3
- Ouvrir le [lien](https://agreste.agriculture.gouv.fr/agreste-saiku/?plugin=true&query=query/open/SAANR_DEVELOPPE_2#query/open/SAANR_DEVELOPPE_2) indiqué dans les ressouces.
- Cliquer-glisser **Année de référence** de l'item `Filtre` jusqu'à l'item `Colonne`.
- Cliquer sur **Année de référence** pour ajouter toutes les années pour faire passer à droite toutes les donnée postérieures à 2010.
- Cliquer sur **Groupe d'indicateurs** dans l'item `Colonnes` et faire passer à droite uniquement la valeur *Superficie dévelopée* 
- Cliquer-glisser "Département" dans l'item `Colonnes`
- Supprimer toute les lignes dans l'item `Lignes`

À l'issue de ces étapes, vous devriez avoir :
- dans l'item `Colonnes` : 
    - Groupe d'indicateur (*Superficie dévelopée*)
    - Année de référence (*toutes*)
    - Département (*tous*)

- dans l'item `Lignes` :
    - Cultures développées 3 (*tous*)

Rien dan les autres item.

- Cliquer-glisser **Cultures développées 3** qui correspond à un niveau de détail suffisant pour les données qui nous intéressent
- Cliquer sur le bouton `Exporter sous Libre Office` dans le menu en haut. 
- Ouvrir le document et exporter à nouveau en csv l'onglet "Données" sous le nom  `surface_autre_culture_departementales_agreste.csv`




> **Pour aller plus vite**  : vous pouvez annuler la requête à chaque fois tant que vous n'avez pas terminé votre configuration.

> **Note** : on n'exporter pas directement en csv depuis l'interface d'Agreste car le format de sortie est plus complexe à manipuler. 



### Obtention du fichier final

Une fois les trois ressources précédentes obtenues :
- `surface_culture_departementales_agreste.csv`
- `surface_fourrage_departementales_agreste.csv`
- `surface_autre_culture_departementales_agreste.csv`

Veillez à : 

5. executer le jupyter notebook `./get_surface_espece_ancienne_region.ipynb`
6. le script se chargera d'enregistrer un fichier `surface_espece_ancienne_region.csv`

> Attention, il ne s'agit pas du fichier final mobilisé dans les outils Datagrosyst, on doit encore procéder à quelques modifications.