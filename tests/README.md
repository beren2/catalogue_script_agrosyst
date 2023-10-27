## Tests des fonctions 

### Contexte 
Afin de s'assurer que les fonctions utilisées sont correctes, on fourni aussi des tests unitaires permettant d'éprouver la fiabilité sur des exemples. 

### Mise en place
Le test des fonctions s'effectue dans le fichier [scripts/tests/test_nettoyage.py](test_nettoyage.py). 

Chacun des tests réalisé dispose de son environnement de test, c'est à dire du sous-ensemble de données. 
Dans le repertoire [scripts/tests/data](data/), on peut trouver un dossier par test, qui contient les fichiers utilisés pour le test. 

En plus de l'environnement de test, certains tests requièrent l'utilisation de référentiels. Ces référentiels sont mutualisés pour l'ensemble des test et sont donc accessibles dans le repertoires  [data/encrypted_ref_test/](../data/encrypted_ref_test/)
> À terme, les référentiels ne seront plus mutualisés entre les tests pour permettre l'indépendance des tests et garantir une mise à jour des référentiels de tests plus simple.


La description de chacun des tests est donnée dans le fichier [tests/data/metadonnees_tests_unitaires](data/metadonnees_tests_unitaires.csv).

### Point de vigilance
Ces environnements de tests ont vocation à être envoyés et disponibles de façon clair sur le git. Ceci impose deux précautions :
- les fichiers ne doivent pas être trop volumineux (en dessous de 500ko)
- les fichiers ne doivent pas contenir d'informations sensibles (noms des domaines par exemple)


Certains des tests requièrent aussi l'utilisation de référentiels. Comme ces informations sont en elles-mêmes sensibles (soumis à des clauses de partages à Agrosyst) et en vue de maintenir une automatisation des tests à chaque push, ces fichiers sont encryptés. La procédure de test vient ensuite decrypté ces fichiers grace à une clé secrète stockée sur le git. 

### Exemple de procédure d'ajout d'une fonction 

- Étape 1 : Création de la fonction 
- Étape 2 : Création du test de la fonction
- Étape 3 : Génération des données pour le tests
- Étape 4 : Génération et chiffrement des référentiels pour le test. Utiliser le fichier [data/encrypted_ref_test/generation_ref_test.ipynb](../data/encrypted_ref_test/generation_ref_test.ipynb). La clé publique utilisée pour le chiffrement des données est diponible dans le fichier. 
- Étape 6 : Push. 

Les tests ne sont réalisés que lorsqu'on push sur la branche principal. Il est donc pertinent de créer une nouvelle branche de travail pour tout nouveau développement. Une fois que le travail est terminé, le merge avec la branche principal enclenchera l'exécution des tests.


### Précisison(s)

Si les tests sur le git ne portent que sur les données de référentiels disponible sur le repértoire distant, rien n'empêche d'utiliser les données de référentiels complètes en local.