## Magasins
Ce répertoire permet la génération des magasins de données basés sur les données Agrosyst.

Un magasin est un jeu de données adapté aux besoin d'un ou plusieurs utilisateurs. 

Un README expliquant les objectifs et les spécificités de chaque magasin ainsi que les scripts nécessaires à sa génération sont disponibles dans le dossier éponyme.

> Ces jeux de données, à forte redondance, ne sont pas stockés en bases de données mais générés à la volée lors de la demande de l'utilisateur sur Datagrosyst.

### Créer un nouveau magasin
La création d'un nouveau magasin implique de mener à bien les étapes suivantes :

1. Identification et réalisation des outils nécessaires au magasin

Pensez à vérifier si l'outil que vous cherchez à mobiliser n'est pas déjà disponible sur Datagrosyst ! L'interface web peut être un bon outil mais tous les outils stockés n'y sont pas forcément répertoriés.

2. Développement des scripts SQL

Un script SQL permettant la génération d'un magasin consiste en un "SELECT" s'alimentant dans les outils et dans l'entrepôt. Au besoin, il est possible de créer des tables temporaires dans des dépendances (cf [dépendances du magasin can](./can/scripts/dependances/)), il est alors nécessaires de les déclarer dans la table *entrepot_table_dependance* de la base de données opérationnelle de Datagrosyst.

3. Test de la génération en local

Afin de tester la génération de votre nouveau magasin, vous pouvez ajouter les tables nécessaires à sa génération dans le fichier [specs.json](./../00_config/specs.json) et lancer la génération grace au script [main.py](./main.py). 

> Pour simuler le comportement de Datagrosyst et exécuter une requête SQL sur votre machine, vous aurez besoin de la librairie duckdb. Il peut être utile de compléter ces tests grâce à une instance de test de Datagrosyst.

5. Documentation 

Vous n'avez plus qu'à documenter les catégories, tables et colonnes de votre magasin. Attention à bien cocher la colonne *generated* dans **entrepot_table**. 

Si votre magasin mobilise des colonnes déjà documentées par ailleurs (dans des outils ou dans l'entrepôt), vous pouvez utiliser la colonne *reference_column_id* pour y faire référence, Datagroyst affichera automatiquement l'explication présente pour cette colonne.