

# catalogue_script_agrosyst [<img src="./images/datagrosyst.png" align="right" width=200 height=30 alt=""/>](https://datagrosyst.agrosyst.fr)

<!-- badges: start -->
[![Lifecycle: stable](https://img.shields.io/badge/lifecycle-stable-green)](https://lifecycle.r-lib.org/articles/stages.html)
![](https://img.shields.io/github/last-commit/beren2/catalogue_script_agrosyst)
<!-- badges: end -->


Inventaire des scripts mobilisés pour le traitement des données issues du système d'information [Agrosyst](https://agrosyst.fr). 

Les données sont disponibles au téléchargement sur [Datagrosyst](https://datagrosyst.agrosyst.fr). 


## Objectifs

Ce répertoire a été créé avec l'objectif principal d'augmenter la transparence des traitements effectués sur Datagrosyst.

Ce répertoire permet aussi aux personnes qui le souhaitent de partager leur travail aux autres utilisateurs des données.

> La plupart des scripts disponibles sur ce répertoire (entrepôt, outils, magasin) sont automatiquement mobilisés dans Datagrosyst. Il ne sera donc, à priori, pas utile à l'utilisateur de les faire tourner.

Pour un utilisateur désireux de mieux comprendre les données, d'autres ressources plus accessibles existent, [voir notre inventaire de ressources liées à Datagrosyst](https://nextcloud.inrae.fr/s/3oZbgECQebej2Js).


## Organisation du répertoire

### 00_config
Contient : 
- un fichier requirements.txt listant les libraries python utilisées.
- un fichier config.ini listant les connexions aux bases de données ou le chemin de données: 

### 01_entrepot
Permet la génération de l'entrepot de données d'agrosyst. 
Les données issues de cette source correspondent à un remaniement des tables de la base de données opérationnelle d'Agrosyst, elles n'ont pas été corrigées ou modifiées.

### 02_outils
Permet la génération des outils d'aide à la valorisation.
Ces outils sont produits à partir des données de l'entrepot, ou font intervenir des données externes (données spatiales par exemple). 

Plus d'informations sont disponibles dans le [README.md](./02_outils/README.md) du répertoire.

### 03_magasins
Permet la génération de magasins de données. 
Chaque sous-repertoire correspond à un magasin conçu pour un usage spécifique.Les scripts générant un magasin se basent sur l'entrepot et les outils.

Plus d'informations sont disponibles dans le [README.md](./03_magasins/README.md) du répertoire.

### 04_datapaper
Permet la génération d'un datapaper. 
Un datapaper consiste en un remaniement d'un magasin de données (sélection et renommage des colonnes). Un utilisateur ne peut pas télécharger un datapaper directement sur Datagrosyst, il est redirigé vers la publication officielle (datagouv, hal...). 

Plus d'informations sont disponibles dans le [README.md](./04_datapaper/README.md) du répertoire.

### 05_prise_en_main
Contient des exemples de script de prise en main des données. Seul répertoire vraiment utile si vous ne souhaitez pas consulter les hypothèses de traitement de Datagrosyst. 

Plus d'informations sont disponibles dans le [README.md](./05_prise_en_main/README.md) du répertoire.

## Contribuer
Le catalogue des scripts d'agrosyst est libre et collaboratif. Si vous souhaitez participer en ajoutant des scripts générant des outils de prétraitements ou des scripts générant un magasin, il vous suffit d'effectuer les étapes décrites ci-dessous.

Les scripts ajoutés seront étudiés et modifiés par l'équipe Agrosyst afin d'entrer dans les scripts d'outils officiels.

> [!NOTE]  
> Pour permettre d'intégrer les nouveaux scripts dans le processus automatisé, ceux-ci doivent être **rédigés en python**.  
Pour les utilisateurs d'autres langages simplement désireux d'archiver leur code, un **répertoire de dépôt des scripts d'outils est disponible dans [02_outils/depot/](02_outils/depot/).** Si ceux-ci sont jugés d'interêt général pour la communauté de chercheur, alors ils pourront faire l'objet d'une traduction vers python par l'équipe Agrosyst. Dans ce cas, **fournir un jeu de test complet (cf [Mettre en place des tests unitaires](#mettre-en-place-des-tests-unitaires))**  est essentiel. 

### Télécharger les données de l'entrepot sur datagrosyst et indiquer le chemin des données

Modifier le chemin de localisation des données **data_path**.
Garder la configuration **type=local**.

>Cela signifie que l'ensemble des scripts utilisent les données en .csv téléchargées sur la machine dans data_path et les sorties de scripts sont des .csv
Le mode distant utilise et crée les données stockées en base de données.

### Créer une branche

1. `git checkout main` depuis n'importe quel dossier de votre dépôt local `catalogue_script_agrosyst`.
1. `git pull origin main` pour vous assurer que vous avez le dernier code principal.
1. `git checkout -b nom-de-ma-branche` (en remplaçant nom-de-ma-branche par un nom approprié) pour créer une branche

### Générer l'ensemble des outils

Générer les outils avec `python main.py` dans le repertoire 02_outils/.

Vous pouvez aussi les télécharger via Datagrosyst et les deposer dans data_path.

### Effectuer des changements
Vous pouvez soit ajouter un prétraitement dans outils ou bien creer un nouveau magasin.
Pour créer un magasin, il faut créer un nouveau repertoire dans [03_magasins/](03_magasins/) et y deposer tous vos scripts. 

> [!NOTE]  
> Si vous pensez que des fonctions peuvent être utiles à plusieurs magasins, alors les ajouter en tant qu'outils au dossier [02_outils/scripts](02_outils/scripts)
> Si vous avez besoin de fonctions intermédiaires ne donnant pas lieu à une sortie de test, alors les ajout au dossier [02_outils/scripts/utils](02_outils/scripts/utils/)

Si vous souhaitez ajouter un outil :
1. Vous pouvez utiliser les fonctions existantes : par exemple dans [02_outils/scripts/utils/fonctions_utiles.py](02_outils/scripts/utils/fonctions_utiles.py) et l'utiliser dans [02_outils/scripts/nettoyage.py](02_outils/scripts/nettoyage.py)
1. Créer une ou plusieurs fonction qui créent de nouveaux dataframes (prendre pour exemple : indicateur_utilisation_intrant dans [02_outils/scripts/indicateur.py](scripts/outils/indicateur.py))

> [!WARNING]  
> Le nouveau script doit respecter les contraintes imposées par pylint (https://pylint.pycqa.org/en/latest/tutorial.html)
> Il sera inspecté lors de la publication des changements. Pour analyser vos script en local, vous pouvez par exemple travailer sur vs-code et télécharger l'extension pylint

Si vous souhaitez archiver un script qui ne s'intègre pas dans le processus automatisé :

1. Déposer simplement votre nouveau script dans le répertoire [02_outils/depot/](02_outils/depot/)

### Mettre en place des tests unitaires
Les tests unitaires sont des exemples permettant d'assurer que les fonctions crées ont le comportement attendu. 

Les tests unitaires nécessitent :
1) la valeur attendue de chaque sortie de fonction de prétraitement sous forme de tableau .csv 
2) l'ensemble des tables nécessaire sous format .csv afin d'executer les fonctions pour retrouver les valeurs attendues

> [!CAUTION]  
> Si votre fonction integre des données de référentiels (catégorie reférentiel sur datagrosyst), s'en référer à la [documentation](02_outils/tests/README.md).

### Pousser les changement

1. `git add -A && git commit -m "Mon message"` (en remplaçant Mon message par un message de commit, tel que "Ajout du script de filtration des mélanges d'espèce réel.") pour ajouter et valider vos modifications.
1. `git push nom-de-ma-branche`
1. Allez sur le [dépôt catalogue_script_agrosyst](https://github.com/beren2/catalogue_script_agrosyst) et vous devriez voir les branches récemment poussées.

1. Pour que votre modification soit accessible par tous les utilisateurs, créer une pull request vers le main ou envoyer un mail à l'équipe (`datagrosyst.support@inrae.fr`). Votre demande sera analysée par l'équipe Agrosyst.


