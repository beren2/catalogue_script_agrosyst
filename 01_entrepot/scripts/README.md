### Alimentation de l'entrepôt de données 

Ce repertoire rassemble les requetes sql permettant de génerer les tables de l'entrepôt à partir d'une copie de la base de donnée en prod.
L'entrepot est donc un remaniement des tables de la base de donnée opérationnelle.

### Etapes de génération des tables de l'entrepôt
1. Realiser un dump de la prod
2. Lancer le calcul des performances dessus
3. Generation des tables de l'entrepot. Elles commencent toutes par entrepot_*
4. ?

### Criteres de selection
#### Selection des domaines et dispositifs
Une table entrepot_criteres_selection a été crée pour appliquer un filtrage des données concernant des domaines et dispositifs actifs.
Ce filtrage s'effectue en réalisant une jointure "join" de la table voulue avec cette table.
Attention un domaine peut avoir plusieurs dispositifs. Lors que l'on joint cette table avec comme clé le domaine_id, il faut realiser un distinct avant.

D'autres criteres de selection au niveau du domaine ou dispositifs peuvent être ajoutés. ex : l'année, le type de dispositif ...

#### Sélection des sdc, parcelle et zone
Pour les tables systeme de culture (sdc), parcelle et zone, les entités actives sont selectionnées lors de la création de leur table respectives.

#### Imbrication des tables
Les tables domaines, dispositifs, sdc, parcelles et zones sont imbriquées les unes aux autres.

domaines > dispositifs > sdc > parcelles > zones . 

Ainsi la selection de ces entités dépend de leut propre status d'actif ainsi que du status actif de leur(s) parent(s). 
Ex : dans la table entrepot_domaine figure uniquement des domaines actifs
dans la table entrepot_zone figure uniquement des zones actives qui ont une parcelle active

Attention ! Cas particulier des parcelles :

Certaines parcelles ne sont pas attachées à un sdc (import edaplos à corriger).

Pour les parcelles avec un sdc, elles sont jointes avec growingsystem puis verification que le dispositif lié au sdc est actif. (comme c'est un left join, la jointure ne se fait pas avec entrepot_sdc)

Pour les parcelles sans sdc, elles sont jointes avec le domaine provenant de critere_selection.

