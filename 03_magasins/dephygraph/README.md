# Documentation - mag_dephygraph.py

## Objectif Général
Script de génération du magasin DEPHYGraph : traitement, nettoyage et agrégation des données de performances agricoles du réseau DEPHY.

## Source des Données
Les données proviennent du script `02_outils/scripts/mag_dephygraph.py` qui traite :
- **Entrepôt** : données synthétisées et réalisées (SDC, dispositifs, domaines)
- **Performances** : indicateurs IFT, économiques, fertilisation, temps de travail
- **Référentiel géographique** : les geoVec utilisés par DEPHYGraph pour la carto. Afin d'être sur d'uiliser les bonnes propriétés
- **Outils** : identification pz0, entités uniques par SDC

## Étapes Principales du Processus

1. **Nettoyage numéros DEPHY** : extraction pattern AAAANNNN/AAAAXNNN
2. **Filtre 1** : DEPHY Ferme Détaillés avec Type agriculture non-null
3. **Filtre 2** : campagnes entre 2005 et année en cours (-1 si avant avril) exclu 
4. **Identification pz0** : points zéro (états initiaux) et post
5. **Explosion campagnes** : multi-annuelles → lignes séparées
6. **Gestion doublons** : suffixation code_dephy dupliqués
7. **Sélection pz0 unique** : un seul pz0 par code_dephy (le plus récent)
8. **Ajout espèces/variétés** : pour cultures pérennes
9. **Typologies simplifiées** : par filière (arboriculture, maraîchage, etc.)
10. **Infos géographiques** : latitude/longitude, départements, régions
11. **Filtre 3 cohérence** : cohérence des valeurs et des colonnes pour espèces en fonciton des filières ; Semis Direct en AB
12. **Filtre 4 validité** : ≥2 campagnes et ≥1 pz0 par code_dephy
13. **Filtre 5 disponibilité** : variables selon filières (éco/IFT → GCPE uniquement)
14. **Détection outliers IQR** : valeurs aberrantes (coef=2) avec suppression avec cascade de dépendances
15. **Détection alertes CAN** : filtre de valeurs expertisées avec cascade de dépendances
16. **Calcul évolutions IFT** : différences par rapport au pz0
17. **Modification modalités** : libellés pas présentable → libellés présentable
18. **Finalisation** : index unique, colonnes essentielles, ID final

## Fonction Principale
**`all_steps_for_maj_dephygraph(donnees, demande_rapport=False)`**

Agrège toutes les étapes ci-dessus. Retourne le DataFrame final, les index des outliers détectés et un rapport optionnel.

## Variables Clés Maintenues

### Identifiants
- `id` : identifiant unique (code_dephy_campagne)
- `code_dephy` : numéro DEPHY nettoyé

### Temporalité
- `new_campagne` : année campagne
- `pz0` : état initial/post
- `c103_networkYears` : années depuis pz0

### Géographie
- `latitude / longitude`
- `arrondissement / departement / region`

### Performances
- **IFT** : chimique total, par type (herbicide, fongicide, etc.), biocontrôle
- **Économiques** : produit brut, marges, charges
- **Fertilisation** : N/P/K total/minéral/organique
- **Temps travail** : manuel, matériel, total

## Fichier SQL

### Renommage
Le magasin généré est ensuite renommé selon les conventions définies dans `03_magasins/dephygraph/scripts/rename_dephygraph.sql` pour l'intégration finale dans le système.

### Ajout Culture tropicales
Dans `03_magasins/dephygraph/scripts/rename_dephygraph.sql`.  
Ajout des données de culture tropicales qui est préparé et qui n'a plus qu'a être concaténé.
Les données de Cultures tropicales sont encore peu ou mal renseignés dans Agrosyst, et ce à cause du fait que l’outil est peu adapté à cette filière. Cependant les données ont été récupérées dans une table Excel, compilées et mises au format par la Cellule Référence. Ces données ne concernent que les IFT et ont été vérifié par l’expert filière, il n’y a donc pas besoin de passer par les filtres et nettoyages. Le fichier en question : dephygraph_CAN_files/Ajouts_donnees_TROP_enquete_format_magasin_donnees_10102022.xlsx.  
Pour plus d’infos, voir le mail du lun. 10/10/2022 16:57.  
Ces données ne sont pas destinées à être implémentées de cette manière, mais via la base de données Agrosyst quand l’outil permettra des saisies plus adaptées à la filière Culture tropicales.  

### Ajout IPMworks
Ajout des données IPMworks qui est préparé et qui n'a plus qu'a être concaténé.

## Notes Importantes
- **Ordre critique** : filtres 1-5 suppriment des lignes, cohérence/outliers modifient des valeurs
- **Cascade valeurs** : variables liées (DICT_VAR_IMPACTED) - suppression parent → enfants
- **Unicité index** : `code_dephy * new_campagne` doit être unique après transformations

## Dépendances Python
```
pandas
numpy
datetime
ydata_profiling
```
