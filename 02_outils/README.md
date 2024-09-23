## Outils
Ce répertoire permet la génération des tables d'outils d'utilisation des données agrosyst.

L'ensemble des tables outils sont crées par les scripts dans le repertoire [scripts](scripts/).

### Générer les outils : lancer le programme principal

Les fichiers de configuration sont disponibles dans le répertoire [00_config/config.ini](00_config/config.ini). <br>
Il suffit de saisir le nom de la BDD de l'entrepôt sur laquelle les outils seront ajoutés en base de données. 

```
	python main.py
```
Il suffit ensuite de choisir l'option à executer.

### Répertoire Tests
Chaque fonction outils générant une table outils est testée au sein de ce repertoire grâce à des **tests unitaires**.

Un test unitaire viens confronter une valeur théorique, celle à laquelle on s'attend avec celle qui est calculée par la fonction avec un jeu de données test.