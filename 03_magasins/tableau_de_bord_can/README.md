
## Le projet magasin tableau de bord CAN

## Résumé

Historiquement, le magasin de données était constitué par la Cellule Référence sur la base de l’export fourni par Agrosyst. Les traitements effectués devaient permettre d’alimenter le tableau de bord, service mis à dispositions des ingénieurs du réseau DEPHY pour visualiser l’état de leurs saisies. Les données compilées permettaient aussi à la Cellule Référence de mettre à jour les données support à l’animation interne du réseau.

## Tables 
- itk_gcpe
- itk_maraich
- sdc_arbo
- sdc_gcpe
- sdc_horti
- sdc_maraich
- sdc_viti

## Différences cahier des charges

Certaines différences par rapport au cahier des charges sont encore présentes et seront corrigées pendant la durée du projet de développement.

### sdc_arbo

#### Colonnes attendues mais absentes 
- nb_manip_produit_danger_SDC -> voir quantite_mat_active_danger_SDC
- nb_manip_prod_danger_enviro_SDC -> voir qte_mat_active_danger_env_SDC
- situation_production_mill -> vu avec cellule ref, ok pour suppression

#### État : validé 

### sdc_gcpe

#### Colonnes attendues mais absentes
- surface_sans_espece_SDC -> à quoi cette colonne correspond ?

#### Colonnes à valider 
- div_cult_sdc -> attention, actuellement, `indicateur_diversite_outils_dirodur.typodirodur_culture_richesse`, est-ce bien ce qui est attendu ?
- departement -> numéro, ok ?
- surface_sdc_itk -> que mettre ?

### sdc_maraich

#### Colonnes supprimées
- toutes les colonne du type `MED_xxx` car pas disponibles

### sdc_itk
#### Colonnes à valider 
- ab_conv --> les "en transition" sont considérés comme bio. Pour le détail, considérer sdc_type_agriculture



## Participants

#### Équipe Agrosyst :
- Bérenger Vuittenez
- Thomas Badie
- Solenne Rousselet
- Thibault Peyrard

#### Équipe Cellule Référence DEPHY
- Matthieu Babiar
- Baptiste Drut
- Nicolas Chartier


## Dates
Le travail préliminaire autour du magasin de données a commencé en 2025. Sa réalisation pratique a commencé mi-2026.
