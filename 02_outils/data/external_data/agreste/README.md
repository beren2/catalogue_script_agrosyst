# Données Agreste

## Contexte

[Agreste](https://agreste.agriculture.gouv.fr/agreste-web/) est un organisme public français d'études et de statistiques sur l'agriculture, la forêt et les industries agro-alimentaires. Son service de la statistique agricole est chargé de l'exécution, en France, d'enquêtes communautaires consistants en de grandes opérations statistiques.

Plusieurs jeux de données produit par l'organisme sont mobilisés dans le cadre de la livraison des données sur Datagrosyst :
- le niveau d'utilisation de traitements phytosanitaire moyen par région et par année 
- la surface dévelopée par région, par année et par culture
- les rendement moyens par région, par année et par culture (**TODO**)

La constitution des données est inspirée de la méthodologie mise au point par la cellule d'animation nationale du réseau DEPHY. Quelques différences sont néanmoins à prendre en compte.


## Objectifs

Ce document a pour objectifs  
- de décrire les spécificités de la source Agreste et de donner quelques clés de compréhension à l'utilisation des données
- de recenser les dépendances de Datagrosyst à Agreste
- de documenter les procédures de mise à jour des données

## Utiliser les données Agreste

Les données sont disponibles sur le site internet d'Agreste : https://agreste.agriculture.gouv.fr/

Dans l'onglet Chiffres et Analyse, trois items nous intéressent : 
- [Tableaux interractifs](https://agreste.agriculture.gouv.fr/agreste-web/disaron/!searchurl/4b54e171-2bf3-4c8b-93b9-06e41472066c!cda8b080-3e9e-4368-b41d-7a29c1da0be6/search/)
- [Séries longues](https://agreste.agriculture.gouv.fr/agreste-web/disaron/!searchurl/26127c00-fa22-4254-a2e3-8c7e24bcebae/search/)
- [Chiffres et données](https://agreste.agriculture.gouv.fr/agreste-web/disaron/!searchurl/745fcc0d-4e89-4a99-b151-835d2a9be2df/search/)

Tous trois consistent en un filtre prédéfini de l'outil de parcours des données Agreste. 

### Tableaux interractifs
Pour certaines données, Agreste met à disposition un outil de manipulation de données. Par exemple, pour le jeu de donnés d'identifiant **saanr_fourrage_2**, on peut accéder à une interface de manipulation [ici]( https://agreste.agriculture.gouv.fr/agreste-saiku/?plugin=true&query=query/open/SAANR_FOURRAGE_2#query/open/SAANR_FOURRAGE_2).

> Cette modalité d'accès aux données est obsolète. On peut aujourd'hui trouver toutes les informations qui nous intéressent dans les séries longues.

### Séries longues
Ce filtre permet d'accéder à toutes les données suivies sur le long terme par Agreste. Par exemple la [statistique agricole annuelle](https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/) qui donne le détail des surfaces développées par année depuis 2010 en France.

## Traitement par filières

À intervalle régulier, Agreste publie les résultat de ses enquêtes sur le niveau de dépendance aux produits phytosanitaire des agriculteurs en France. Ces enquêtes sont spécifiques à une ou plusieurs filière. Dans la suite, on distinguera donc les méthodologies en fonction des filières.

L'indicateur retenu pour l'étude via Agrosyst est l'IFT chimique total sans traitement de semence. En effet, les traitements de semences sont historiquement mal déclarés sur Agrosyst et leur prise en compte peut introduire des biais importants. On préfère donc comparer les versions sans traitements de semences. Cette information est, on le verra, parfois plus complexe à obtenir.

#### Grandes cultures et polyculture élevage
> [Voir la méthodologie de mise à jour](./gcpe/README.md)

#### Viticulture
> [Voir la méthodologie de mise à jour](./viticulture/README.md)

#### Maraîchage
> [Voir la méthodologie de mise à jour](./maraichage/README.md)
#### Arboriculture 
> [Voir la méthodologie de mise à jour](./arboriculture/README.md)

## Constitution du dossier final
Une fois toutes les données récupérées, veuillez placer tous ces fichiers dans le répertoire final : 
- Arboricutlure
    - `ift_culture_ancienne_region_arboriculture_2018.csv`
    - `ift_culture_ancienne_region_arboriculture_2024.csv`
- Viticulture
    - `agreste_ift_viticulture_departement.csv`
- GCPE
    - `agreste_ift_gcpe_reference_region_2017.csv`
    - `agreste_ift_gcpe_reference_region_2021.csv`