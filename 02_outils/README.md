## Outils

### Contexte
Toutes les tables générés par ce repértoire permettent de manipuler efficacement l'entrepôt de données Agrosyst. Les catégories générées sont décrites ci-dessous.

### Catégories


#### Nettoyage
Les scripts présents dans le répertoire [02_outils/scripts/utils/fonction_nettoyage](02_outils/scripts/utils/fonction_nettoyage) permettent de réaliser ces tests de conformités. Ils attribuent à chaque entité une note de conformité, consistant en un vecteur binaire indiquant les tests passés et les tests échoués (1 pour passé, 0 pour raté). La description de ces tests ainsi que leur position dans le vecteur binaire sont donnés dans le fichier [02_outils/data/metadonnees_tests.csv](02_outils/data/metadonnees_tests.csv). La description des seuils utilisés pour ces tests est disponible dans le fichier [02_outils/data/data/metadonnees_seuils.csv](02_outils/data/metadonnees_seuils.csv).

Certains des tests utilisent aussi des fonctions utiles, déclarées dans le fichier [02_outils/scripts/utils/](02_outils/scripts/utils/).

#### Agregation
Les tables générées par ce fichier permettent de 'sauter' efficacement d'une échelle à une autre dans les données. Par exemple, elles permettent d'obtenir directement le domaine associé à une utilisation d'intrant sans être obligé d'effectuer toutes les fusions à la main.

#### Restructuration
Les tables de restructuration permettent essentiellement de corriger des problèmes dans les données issues du synthétisé. Notamment, elles permettent de proposer de travailler avec des identifiants 'id' plutôt qu'avec des 'code'. Les prétraitement consistent bien souvent à aller rechercher l'année du domaine de rattachement et à sélectionner parmis les idenfiants possibles avec le même code, celui de la bonne année.

#### Indicateurs
Les tables Indicateurs proposent des informations supplémentaires sur des indicateurs non retournés par Agrosyst. 
