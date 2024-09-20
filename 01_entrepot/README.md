### Boîte à outil entrepôt de données 

Ce repertoire rassemble les outils permettant de mettre à jour les informations dans l'entrepôt de données Agrosyst. 


### Lancer le programme principal

Afin d'accéder à l'interface en ligne de commande, saisissez ceci :
```
	python main.py
```
Les fichiers de configuration sont disponibles dans le répertoire 'config_files'.
L'option 4 est l'option automatisée pour le dump et le restore.
Il suffit de saisir le nom de la BDD à dump, le nom de la nouvelle BDD (entrepot_yyyymmdd) et l'entrepôt sera généré. 

Une fois que l'option 4 est terminé, mettez à jour les fichiers de configuration et executez l'option 1.

### Génération des magasins de données

Une fois les données de l'entrepôt crée sur la nouvelle BDD : 
- se rendre dans le repertoire 'utils/entrepot_nettoyage'
- executer le main.py (comme précédemment)
- télécharger les nouvelles données (option 1)
- charger les nouvelles données (option 2)
- lancer la génération de chacun des magasins de données 

