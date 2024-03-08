## catalogue_script_agrosyst

Catalogue des pré-traitements des données issues du système d'information Agrosyst (https://agrosyst.fr). Les données sont disponibles au téléchargement sur (https://agrosyst.fr/datagrosyst/) sous réserve d'avoir déposé une demande d'accès et que celle-ci ait été approuvée par l'intégralité du comité des partenaires.

## Contribuer
Le catalogue des pré-traitements agrosyst est libre et collaboratif. Si vous souhaitez participer en ajoutant des scripts de prétraitements, il vous suffit d'effectuer les étapes suivantes. 
Les scripts ajoutés seront étudiés et modifiés par l'équipe Agrosyst afin d'entrer dans les scripts de pré-traitements officiels.

#### Créer une branche

1. `git checkout main` depuis n'importe quel dossier de votre dépôt local `catalogue_script_agrosyst`.
1. `git pull origin main` pour vous assurer que vous avez le dernier code principal.
1. `git checkout -b nom-de-ma-branche` (en remplaçant nom-de-ma-branche par un nom approprié) pour créer une branche

#### Faire les changements

1. Créer un nouveau script dans le repertoire scripts/ avec un nom approprié.
2. Le nouveau script doit respecter les contraintes imposées par pylint (https://pylint.pycqa.org/en/latest/tutorial.html)

#### Push les changement

1. `git add -A && git commit -m "Mon message"` (en remplaçant Mon message par un message de commit, tel que "Ajout du script de filtration des mélanges d'espèce réel.") pour ajouter et valider vos modifications.
1. `git push my-fork-name nom-de-ma-branche`
1. Allez sur le [dépôt catalogue_script_agrosyst](https://github.com/beren2/catalogue_script_agrosyst) et vous devriez voir les branches récemment poussées.
1. Suivez les instructions de GitHub.


## Organisation du répertoire

### Scripts
Les scripts sont disponibles dans le répetoire [scripts](scripts/). 

#### Nettoyage global
Les scripts disponibles dans le repertoire [scripts/nettoyage_global](scripts/nettoyage_global/) proposent des fonctions permettant d'obtenir des scores de conformité pour chaque entité d'Agrosyst. Plus d'information dans le README.md du répertoire. 

#### Utils

##### Général
Les scripts disponibles dans le repertoire [scripts/utils](scripts/utils/) proposent des fonctions utiles permettant par exemple d'obtenir des informatiosn supplémentaires sur les données ou de mettre à jour les données via l'appel à l'api. 

##### Mise à jour ou téléchargement des données via l'API
1) Modifier le fichier de configuration avec vos informations [config/datagrosyst.ini](config/database.ini) 
> Le chemin last_update_date_file sert de stockage pour l'historique de vos mise à jours des données, il est conseillé de le stocker au même endroit que ces dernières
2) Servez-vous de la fonction principale dans [api_call.py](scripts/utils/api_call.py) :

> `refresh_last_data(data_path)`



### Tests
Les tests sont disponibles dans le repetoire [tests](tests/). Plus d'information dans le README.md du répertoire. 

### Data
Les données et méta-données disponibles sont disponibles dans le répertoire [data](data/).
