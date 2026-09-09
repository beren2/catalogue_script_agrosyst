# Données Agreste

## Contexte

[Agreste](https://agreste.agriculture.gouv.fr/agreste-web/) est un organisme public français d'études et de statistiques sur l'agriculture, la forêt et les industries agro-alimentaires. Son service de la statistique agricole est chargé de l'exécution, en France, d'enquêtes communautaires consistants en de grandes opérations statistiques.

Plusieurs jeux de données produit par l'organisme sont mobilisés dans le cadre de la livraison des données sur Datagrosyst :
- le niveau d'utilisation de traitements phytosanitaire moyen par région et par année 
- la surface dévelopée par région, par année et par culture
- les rendement moyens par région, par année et par culture (**TODO**)

## Objectifs

Ce document a pour objectifs de 
- décrire les spécificités de la source Agreste et de donner quelques clés de compréhension à l'utilisation des données
- recenser les dépendances de Datagrosyst à Agreste
- documenter les procédures de mise à jour des données

## Utiliser les données Agreste

Les données sont disponibles sur le site internet d'Agreste  https://agreste.agriculture.gouv.fr/

Dans l'onglet Chiffres et Analyse, trois items nous intéressent : 
- [Tableaux interractifs](https://agreste.agriculture.gouv.fr/agreste-web/disaron/!searchurl/4b54e171-2bf3-4c8b-93b9-06e41472066c!cda8b080-3e9e-4368-b41d-7a29c1da0be6/search/)
- [Séries longues](https://agreste.agriculture.gouv.fr/agreste-web/disaron/!searchurl/26127c00-fa22-4254-a2e3-8c7e24bcebae/search/)
- [Chiffres et données](https://agreste.agriculture.gouv.fr/agreste-web/disaron/!searchurl/745fcc0d-4e89-4a99-b151-835d2a9be2df/search/)

Tous trois consistent en un filtre prédéfini de l'outil de parcours des données Agreste. 

### Tableaux interractifs
Pour certaines données, Agreste met à disposition un outil de manipulation de données. Par exemple, pour le jeu de donnés d'identifiant **saanr_fourrage_2**, on peut accéder à une interface de manipulation [ici]( https://agreste.agriculture.gouv.fr/agreste-saiku/?plugin=true&query=query/open/SAANR_FOURRAGE_2#query/open/SAANR_FOURRAGE_2).

> Certaines données nécessaires à Datagrosyst seront obtenues via cette interface.

### Séries longues
Ce filtre permet d'accéder à toutes les données suivies sur le long terme par Agreste. Par exemple la [statistique agricole annuelle](https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/) qui donne le détail des surfaces développées par année depuis 2010 en France.

## Dépendances

### Niveau d'utilisation de traitement phytosanitaires

À intervalle régulier, Agreste publie les résultat de ses enquêtes sur le niveau de dépendance aux produits phytosanitaire des agriculteurs en France. Ces enquêtes sont spécifiques à une ou plusieurs filière.

#### Grandes cultures et polyculture élevage

2017 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd1903/detail/

2021 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2407/detail/

> [Voir la méthodologie de mise à jour](./ift/gcpe/README.md)

#### Maraîchage

2018 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2312/detail/

2022 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2504/detail/

> Voir la méthodologie de mise à jour  : TODO

#### Viticulture

2019 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2304/detail/

2016 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2004/detail/

2024 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2607/detail/

> Voir la méthodologie de mise à jour  : TODO

#### Arboriculture 

2018 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2108/detail/

2024 : https://agreste.agriculture.gouv.fr/agreste-web/disaron/Chd2607/detail/


### Surface développée par région, par année et par culture

#### GCPE
- https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/ :

> [Voir la méthodologie de mise à jour](./surface/gcpe/README.md)


### Génération des fichiers finaux

Une fois l'intégralité des fichiers récupérés, on doit procéder à une étape supplémentaire. En effet, certaines enquêtes Agreste n'exposent pas les mêmes colonnes en sortie, il faut donc retravailler les fichier pour. 

> Cette étape ne **peut pas** être réalisée directement au moment de l'import du fichier car, pour rendre homogène les fichiers, on a besoin des autres fichiers. Par exemple, pour fusionner les colonnes "Orge de printemps" et "Orge d'hiver" de l'enquête PK sur les produits phytosanitaires, on a besoin des résultats de l'enquête sur les surface développées dans chacune de ces cultures...

Les fichiers finaux sont stockés dans TODO. 
C'est ceux-ci qui seront mobilisés par les outils Datagrosyst.
