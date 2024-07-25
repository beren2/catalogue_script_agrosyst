## Outils

### Contexte
Toutes les tables générés par ce repértoire permettent de manipuler efficacement l'entrepôt de données Agrosyst. Les catégories générées sont décrites ci-dessous.

### Catégories


#### Nettoyage

Nettoyage.py consiste en une fonction pour chaque echelle (utilisation_intrant_realise, intervention_realise) produisant une table avec en colonne l'id de l'entité + une colonne pour chaque test.

Pour chaque table/échelle, sont appliquées les fonctions de test de conformité présentes dans le répertoire [scripts/nettoyage_global/fonctions_tests](../../scripts/nettoyage_global/fonctions_tests/). Ces tests attribuent à chaque entité une note de conformité, consistant en un vecteur binaire indiquant les tests passés et les tests échoués (1 pour passé, 0 pour raté).

La liste et description des ces tests sont donnés dans le fichier [data/metadonnees_tests.csv](../../data/metadonnees_tests.csv).

Les fonctions tests utilisent des **seuils à dire d'experts** listés et décrits dans le fichier [data/metadonnees_seuils.csv](../../data/metadonnees_seuils.csv).

Certains des tests utilisent aussi des fonctions utiles, déclarées dans le fichier [scripts/utils/fonctions_utiles](../../scripts/utils/fonctions_utiles.py).


```mermaid
graph LR

subgraph Data
        metadata_seuil[Metadata seuils]:::gray 
        metadata_test[Metadata tests]:::gray 
end

fonction_test[Fonction test]:::gray 
fonction_utils[Fonction utiles]:::gray 
nettoyage[Nettoyage.py <br> 1 fonction par table/échelle <br> -> 1 table id + 1 colonne par test]:::gray 

metadata_seuil --> fonction_test
fonction_utils --> fonction_test
metadata_test -- Liste des tests à chaque <br> échelle--> nettoyage
fonction_test --> nettoyage

%% Colors %%
classDef gray fill: #f1f1f1  ,stroke:#BBB,stroke-width:1px,color:#000
```

#### Agregation
Les tables générées par ce fichier permettent de **'sauter' efficacement d'une échelle à une autre** dans les données. Par exemple, elles permettent d'obtenir directement le domaine associé à une utilisation d'intrant sans être obligé d'effectuer toutes les fusions à la main.

```mermaid
graph BT

Intrant_1[intrant 1]:::gray --> Intervention_1[intervention 1]:::gray
Intrant_2[intrant 2]:::gray --> Intervention_2[intervention 2]:::gray

Intervention_1 --> culture[Culture]:::gray
Intervention_2 --> culture[Culture]:::gray

culture --> sdc[Sdc]:::gray
culture --> sdc[Sdc]:::gray

Intrant_2 -.-> sdc[Sdc]

%% Colors %%
linkStyle 6 stroke:green
classDef gray fill: #f1f1f1  ,stroke:#BBB,stroke-width:1px,color:#000

```

#### Restructuration
Les tables de restructuration permettent essentiellement de corriger des problèmes dans les données issues du synthétisé. 

Notamment, elles permettent de proposer de travailler avec des identifiants 'id' plutôt qu'avec des 'code'. Les prétraitement consistent bien souvent à aller rechercher l'année du domaine de rattachement et à sélectionner parmis les idenfiants possibles avec le même code, celui de la bonne année.

#### Indicateurs
Les tables Indicateurs proposent des informations supplémentaires sur des indicateurs non retournés par Agrosyst. 
