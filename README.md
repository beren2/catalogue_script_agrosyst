## Catalogue_script_agrosyst

Catalogue des pré-traitements des données issues du système d'information Agrosyst (https://agrosyst.fr). Les données sont disponibles au téléchargement sur (https://agrosyst.fr/datagrosyst/) sous réserve d'avoir déposé une demande d'accès et que celle-ci ait été approuvée par l'intégralité du comité des partenaires.

## Organisation du répertoire

### Scripts
L'ensemble des scripts générant les magasins de données disponibles sur datagrosyst ou bien les outils d'aide à la valorisation sont disponibles dans le répetoire [scripts](scripts/).

Afin de comprendre comment sont réalisés les prétraitements, ou bien les réaliser nous même (ex : avec d'autres seuils), plus d'informations sont disponibles dans le README.md du répertoire.

### Data
Les données et méta-données concernant les scripts sont disponibles dans le répertoire [data](data/).

### Tests
Chaque fonction de prétraitement possède un test controlant la sortie de la fonction de prétraitement. Les jeux de tests avec les valeurs attendues sont disponibles dans le repetoire [tests](tests/). Plus d'informations sont disponibles dans le README.md du répertoire.

## Contribuer
Le catalogue des pré-traitements agrosyst est libre et collaboratif. Si vous souhaitez participer en ajoutant des scripts de prétraitements, il vous suffit d'effectuer les étapes suivantes. 
Les scripts ajoutés seront étudiés et modifiés par l'équipe Agrosyst afin d'entrer dans les scripts de pré-traitements officiels.

> [!NOTE]  
> **L'ensemble des scripts sont en python.** Nous avons conscience que beaucoup de valorisateurs utilisent le langage R. **Un répertoire de dépôt des script R** est disponible. D'autres utilisateurs pourrons être aidés par votre proposition de pré traitement le temps que nous fassions le travail de traduction de R vers python. 
Cependant pour que votre pré traiment soit traduit en python et intégré à datagrosyst, une condition est necessaire : **fournir un jeu de test complet (cf [Mettre en place des tests unitaires](#mettre-en-place-des-tests-unitaires))** 

### Créer une branche

1. `git checkout main` depuis n'importe quel dossier de votre dépôt local `catalogue_script_agrosyst`.
1. `git pull origin main` pour vous assurer que vous avez le dernier code principal.
1. `git checkout -b nom-de-ma-branche` (en remplaçant nom-de-ma-branche par un nom approprié) pour créer une branche

### Faire les changements
Vous pouvez soit ajouter un prétraitement dans outils ou bien creer un nouveau magasin.
Pour créer un magasin, il faut créer un nouveau repertoire dans [scripts/magasins/](scripts/magasins/) et y deposer tous vos scripts. 

> [!NOTE]  
> Si vous pensez que des fonctions peuvent être utiles à plusieurs magasins, alors les ajouter en tant qu'outils au dossier [scripts/outils](scripts/outils/)
> Si vous avez besoin de fonctions intermédiaires ne donnant pas lieu à une sortie de test, alors les ajout au dossier [scripts/utils](scripts/utils/)

Si vous souhaitez ajouter un outil:
1. Vous pouvez utiliser les fonctions existantes : par exemple ajouter une fonction test dans [scripts/outils/fonctions_tests](scripts/outils/fonctions_tests) et l'utiliser dans [scripts/outils/nettoyage.py](scripts/outils/nettoyage.py)
1. Créer une ou plusieurs fonction qui créent de nouveaux dataframes (prendre pour exemple : indicateur_utilisation_intrant dans [scripts/outils/indicateur.py](scripts/outils/indicateur.py)

> [!WARNING]  
> Le nouveau script doit respecter les contraintes imposées par pylint (https://pylint.pycqa.org/en/latest/tutorial.html)
> Il sera inspecté lors de la publication des changements. Pour analyser vos script en local, vous pouvez par exemple travailer sur vs-code et télécharger l'extension pylint

### Mettre en place des tests unitaires
Les tests unitaires sont des exemples permettant d'assurer que les fonctions crées ont le comportement attendu. 

Les tests unitaires nécessitent :
1) la valeur attendue de chaque sortie de fonction de prétraitement sous forme de tableau .csv 
2) l'ensemble des tables nécessaire sous format .csv afin d'executer les fonctions pour retrouver les valeurs attendues

> [!CAUTION]  
> Si votre fonction integre des données de référentiels (catégorie reférentiel sur datagrosyst) veuillez contacter l'équipe datagrosyst puisque les référentiels ne peuvent être rendus publiques sur ce git

### Push les changement

1. `git add -A && git commit -m "Mon message"` (en remplaçant Mon message par un message de commit, tel que "Ajout du script de filtration des mélanges d'espèce réel.") pour ajouter et valider vos modifications.
1. `git push nom-de-ma-branche`
1. Allez sur le [dépôt catalogue_script_agrosyst](https://github.com/beren2/catalogue_script_agrosyst) et vous devriez voir les branches récemment poussées.

1. Une fois votre travail fini, créer une pull request vers le main. Celle-ci sera analysée par l'équipe Agrosyst.


