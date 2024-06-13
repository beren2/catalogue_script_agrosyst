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

1. Créer un nouveau script dans le repertoire scripts/mon_magasin. Si vous pensez que des fonctions peuvent être utiles à plusieurs magasins, alors les ajouters dans le dossier [scripts/utils](scripts/utils/)
1. Créer une ou plusieurs fonction qui créent vos nouveaux dataframes (prendre pour exemple : indicateur_utilisation_intrant dans [scripts/nettoyage_global/indicateur.py](scripts/nettoyage_global/indicateur.py)) 
1. Le nouveau script doit respecter les contraintes imposées par pylint (https://pylint.pycqa.org/en/latest/tutorial.html)

#### Push les changement

1. `git add -A && git commit -m "Mon message"` (en remplaçant Mon message par un message de commit, tel que "Ajout du script de filtration des mélanges d'espèce réel.") pour ajouter et valider vos modifications.
1. `git push my-fork-name nom-de-ma-branche`
1. Allez sur le [dépôt catalogue_script_agrosyst](https://github.com/beren2/catalogue_script_agrosyst) et vous devriez voir les branches récemment poussées.
1. Si vous considérez que votre travail peut intéresser la communauté des utilisateurs des données Agrosyst, créer une pull request vers le main. Celle-ci sera analysée par l'équipe Agrosyst.

### Mettre en place des tests unitaires
Les tests unitaires sont des exemples permettant d'assurer que les fonctions crées ont le comportement attendu. Une fois votre pull request réalisée, l'équipe Agrosyst vous contactera pour obtenir des tests unitaires propres à votre fonction.

## Organisation du répertoire

### Scripts
Les scripts sont disponibles dans le répetoire [scripts](scripts/).
Chacun des dossiers contenu dans ce répertoire sert à la constitution d'un magasin de données. Par exemple, le dossier [nettoyage_global](scripts/nettoyage_global) contient l'ensemble des fichiers permettant de constituer le magasin de donnée "nettoyage", disponible sur Datagrosyst. Chaque magasin de donnée doit disposer d'un README.md qui explique son objectif et sa méthodologie.

#### Nettoyage global
Les scripts disponibles dans le repertoire [scripts/nettoyage_global](scripts/nettoyage_global/) proposent des fonctions permettant d'obtenir des scores de conformité pour chaque entité d'Agrosyst. Plus d'information dans le README.md du répertoire. 

#### Utils
Les scripts jugés d'interêt général pour les magasins de données peuvent être stockés dans le répertoire [scripts/utils](scripts/utils/). 

#### Prise en main
Les scripts disponibles dans le répertoire [scripts/prise_en_main](scripts/prise_en_main/) proposent des exemples basiques de traitement sur les données.

### Tests
Les tests sont disponibles dans le repetoire [tests](tests/). Plus d'information dans le README.md du répertoire. 

### Data
Les données et méta-données disponibles sont disponibles dans le répertoire [data](data/).
