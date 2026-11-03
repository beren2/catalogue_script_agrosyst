
# Procédure de mise à jour des données en GCPE

## Objectif(s)
L'objectif est de diposer, pour chaque année `XXXX` étudiée, d'un fichier `agreste_ift_gcpe_reference_region_XXXX.csv`, disposant des colonnes : 
- **nom_ancienne_region** : nom de l'ancienne région avec la fusion de 2016 (*exemple : Franche-Comté*)
- **ift_moyen_gcpe_can** : indice de fréquence de traitement moyen chimique sans traitement de semence dans la région, d'après l'enquête Agreste, en pondérant l'assolement en considérant les prairies (plus pertinent pour les systèmes en polyculture-élevage)
- **ift_moyen_gcpe_can_sans_prairie** : indice de fréquence de traitement moyen chimique sans traitement de semence dans la région, d'après l'enquête Agreste, en pondérant l'assolement sans considérer les prairies (plus pertinent pour les systèmes en grandes cultures)

L'IFT moyen calculé grâce à une procédure mise au point par la cellule référence du réseau DEPHY. Il consiste en l'évaluation d'un système de culture virtuel présentant l'assolement moyen au niveau régional. 

1) Identification des assolements régionaux pour l'année `XXXX` et les cultures données : on attribue à chaque culture étudiée un poids dans l'assolement régional (*exemple : le blé tendre représentait, en 2017, en Alsace, environ 21.8% de la surface agricole totale allouée aux cultures étudiées en considérant les prairies, 22.9% en ne considérant pas les prairies*)

2) Pondération de l'assolement par l'IFT Agreste de la culture pour obtenir la contribution de la culture à l'IFT (*pour l'exemple précédent, l'IFT Blé tendre de l'Alsace en 2017 est 3.4, on multiplie donc 3.4 par 21.8% pour obtenir la contribution du blé dans l'IFT du système virtuel*). On somme toutes les contributions des cultures étudiées pour obtenir l'IFT moyen total.



## Difficultés
La structuration de ces fichiers est rendue complexes par plusieurs facteurs : 
- **l'hétérogénéïté de la structure des fichiers transmis par Agreste** : chaque année enquêtées, les `.xlsx` transmis par Agreste évoluent, il faut donc adapter les scripts de traitement nous permettant de reccueillir les informations.
- **les évolutions de suivis dans les enquêtes Agreste** : au delà de la structure des fichiers, certaines modalités de suivis des données ont évoluées. (*exemple : en 2021, les données relatives à l'orge de printemps et l'orge d'hiver étaient séparées alors qu'elles étaient traitées ensemble antérieurement*), cf [01_restructuration.ipynb](./01_restructuration.ipynb). 
- **l'absence de certaines donnees** : en 2021, il n'est plus possible de trouver les données d'IFT hors traitements de semences des anciennes régions. On peut alors utiliser deux approches : 
    - obtenir le détail des traitements de semence par culture et considérer que les variations sont négligeables entre anciennes régions. Au moment de la pondération de l'assolement moyen par l'IFT, on retire alors la valeur du traitement de semence pour la culture considérée (cf [02_finalisation](./02_finalisation.ipynb)). 
    - obtenir les données via une personne ayant accès aux CASD et à l'ensemble des données Agreste.
    
    Pour l'intant, c'est la première approche qu'on retient pour sa meilleure capacité à être partiellement automatisée.

## IFT
Pour mettre à jour les données relatives à l'IFT, s'en référer à la procédure [ici](./ift/README.md)

## Surface
Pour mettre à jour les données relatives aux surfaces, s'en référer à la procédure [ici](./surface/README.md)

## Mise à jour finale
Comme mentionné précédemment, il est nécessaire d'apporter quelques modifications aux fichiers obtenus via Agreste. 

Une fois toutes les données obtenues, il est donc nécessaire d'exécuter les jupyter notebook :
- [01_restructuration.ipynb](./01_restructuration.ipynb)
- [02_finalisation.ipynb](./01_finalisation.ipynb)


## Différences avec la méthodologie de la cellule référence du réseau DEPHY

Plusieurs différences sont à observer par rapport à la méthodologie de constitution de la cellule référence du réseau DEPHY. 

### Plus de cultures
Les données de surfaces comptabilisent plus de cultures qu'initiallement :
- Soja
- Lin fibre
- Prairie non permanente

Les pourcentages des surfaces allouées aux autres cultures prennent donc en compte l'existence de ces cultures sur les différentes régions.

> Attention même si on distingue certaines cultures au moment de la création du fichier [surface_espece_ancienne_region](surface/gcpe/surface_espece_ancienne_region.csv) (par exemple Orge hiver et Orge printemps), elles sont fusionnées par la suite lors de la restructuration et ne sont donc pas accessibles dans les fichiers finaux.


### Prise en compte des traitements de semences
Pour obtenir les IFT Agreste sans traitement de semence, on retranche, par culture, l'IFT traitement de semence obtenu sur Agreste. Attention, c'est le IFT traitement de semence pour toutes les régions confondues.