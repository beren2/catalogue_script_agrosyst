
# Procédure de mise à jour des données de surface en GCPE

## Ressources

### Données départementales SAA

**source :** Statistique Agricole Annuelle (SAA) - Série longue depuis 2010

**lien :** https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/

**nom du fichier :**
`SAA_2010-2025_provisoires_donnees_departementales.xlsx`

**date de dernière mise à jour** : 23/09/2026

### Récapitulatif des données nécessaires

Le tableau ci-dessous récapitule l'ensemble des données nécessaires et l'endroit où les trouver dans les ressources.

| Données nécessaires          | Ressource                 | Feuilles | Lignes                                               | Colonnes              |
|------------------------------|---------------------------|----------|------------------------------------------------------|-----------------------|
| surface betterave sucrière   | Données départementales SAA | IND      | 01 – Betterave industrielle                         | SURF_2010 → SURF_2025 |
| surface maïs fourrage        | Données départementales SAA | FOU      | 06 – Total maïs fourrage et ensilage (04 + 05)         | SURF_2010 → SURF_2025 |
| surface prairies non permanentes | Données départementales SAA | FOU  | 13 – Total prairies non permanentes (11 + 12)          | SURF_2010 → SURF_2025 |
| surface pomme de terre       | Données départementales SAA | PDT      | 07 – Pommes de terre (01 + … + 05)                    | SURF_2010 → SURF_2025 |
| surface canne à sucre        | Données départementales SAA | IND      | 02 – Canne à sucre                                  | SURF_2010 → SURF_2025 |
| surface soja                 | Données départementales SAA | COP      | 33 – Soja                                            | SURF_2010 → SURF_2025 |
| surface lin fibre            | Données départementales SAA | IND      | 05 – Lin textile                                     | SURF_2010 → SURF_2025 |
| surface Blé tendre           | Données départementales SAA | COP      | 03 – Total blé tendre (01 + 02)                      | SURF_2010 → SURF_2026 |
| surface Blé dur              | Données départementales SAA | COP      | 06 – Total blé dur (04 + 05)                         | SURF_2010 → SURF_2027 |
| surface Orge dhiver          | Données départementales SAA | COP      | 08 – Orge dhiver et escourgeon                       | SURF_2010 → SURF_2028 |
| surface Maïs grain           | Données départementales SAA | COP      | 18 – Total maïs grain et maïs semence (16 + 17)      | SURF_2010 → SURF_2029 |
| surface Triticale            | Données départementales SAA | COP      | 20 – Triticale                                      | SURF_2010 → SURF_2030 |
| surface Colza                | Données départementales SAA | COP      | 31 – Total colza grain et navette (29 + 30)           | SURF_2010 → SURF_2031 |
| surface Tournesol            | Données départementales SAA | COP      | 32 – Tournesol                                      | SURF_2010 → SURF_2032 |
| surface Pois protéagineux     | Données départementales SAA | COP      | 41 – Pois protéagineux                               | SURF_2010 → SURF_2033 |

## Procédure de mise à jour 

1. Téléchargement des données

Aller sur le lien indiqué et télécharger le jeu de données 

2. Déposer les fichier `SAA_2010-2025_provisoires_donnees_departementales.xlsx` dans le répertoire courant. 

3. Exporter toutes les feuilles utiles dans le répertoire [brut]('./brut') avec la convention, `surface_departementales_brut_FEUILLE.csv`, où FEUILLE est le code donnée dans le tableau récapitulatif ci-dessous (nom de la feuille, exemple : "COP"). 

4. Exécuter l'ensemble du notebook [get_surface_espece_ancienne_region.ipynb](./get_surface_espece_ancienne_region.ipynb)
