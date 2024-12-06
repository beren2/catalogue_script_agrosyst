"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "CAN".
"""
import pandas as pd
import numpy as np


# FONCTIONS GÉNÉRALES 

UNITE_APPLICATION = {
    'AA_HA': 'Aa/ha',
    'ADULTES_M2': 'adultes/m²',
    'ANA_LINE_SEMAINE_HA': 'Ana-line/semaine/ha',
    'AUXILIAIRES_M2': 'auxiliaires/m²',
    'CARTONETTES_HA': 'cartonettes/ha',
    'DIFFUSEURS_HA': 'diffuseurs/ha',
    'DI_HA': 'Di/ha',
    'DOSES_200M2': 'doses/200 m²',
    'DS_HA': 'Ds/ha',
    'DS_M2': 'Ds/m²',
    'ELEVAGES_500M2': 'élevages/500 m²',
    'G': 'g',
    'G_100KG': 'g/100 kg',
    'G_100L_D_EAU': "g/100 L d'eau",
    'G_100M2': 'g/100 m²',
    'G_10M2': 'g/10 m²',
    'G_160M2': 'g/160 m²',
    'G_BOUTURE': 'g/bouture',
    'G_HA': 'g/ha',
    'G_HL': 'g/hL',
    'G_KG': 'g/kg',
    'G_L': 'g/L',
    'G_L_10M2': 'g/L/10 m²',
    'G_M2': 'g/m²',
    'G_M3': 'g/m³',
    'G_PALME': 'g/palme',
    'G_PIED': 'g/pied',
    'G_PLANT': 'g/plant',
    'G_Q': 'g/q',
    'G_T': 'g/t',
    'G_UNITE_SEMENCES': 'g/unité de semences',
    'HM_M2': 'hm/m²',
    'INDIVIDUS_ARBRE': 'individus/arbre',
    'INDIVIDUS_FOYER': 'individus/foyer',
    'INDIVIDUS_HA': 'individus/ha',
    'INDIVIDUS_M2': 'individus/m²',
    'IND_M2': 'ind/m²',
    'KG_100M2': 'kg/100 m²',
    'KG_HA': 'kg/ha',
    'KG_HL': 'kg/hL',
    'KG_M2': 'kg/m²',
    'KG_M3': 'kg/m³',
    'KG_Q': 'kg/q',
    'KG_T': 'kg/t',
    'KG_UNITE': 'kg/unité',
    'LARVES_50PUCERONS': 'larves/50 pucerons',
    'LARVES_5_A_10M2': 'larves/5 à 10 m²',
    'LARVES_D_AB_COLONIE_DE_PUCERONS': "larves d'Ab/colonie de pucerons",
    'LARVES_M2': 'larves/m²',
    'L_100000_GRAINES': 'L/100000 graines',
    'L_1000M2': 'l/1000m²',
    'L_1000PLANTS': 'L/1000 plants',
    'L_100M2': 'L/100 m²',
    'L_100M3': 'L/100 m³',
    'L_10M2': 'L/10 m²',
    'L_HA': 'L/ha',
    'L_HL': 'L/hL',
    'L_KG': 'L/kg',
    'L_KG_APPAT': 'L/kg appat',
    'L_M2': 'L/m²',
    'L_M3': 'L/m³',
    'L_OU_KG_KG': 'L ou kg/kg',
    'L_PALMIER': 'L/palmier',
    'L_Q': 'L/q',
    'L_T': 'L/t',
    'L_UNITE': 'L/unité',
    'L_UNITE_SEMENCES': 'L/unité de semences',
    'MG_PLANT': 'mg/plant',
    'MILLIARDS_HA': 'milliards/ha',
    'MILLIONS_100M2': 'millions/100 m²',
    'MILLIONS_ARBRE': 'millions/arbre',
    'MILLIONS_L_BOUILLIE': 'millions/L de bouillie',
    'MILLIONS_M2': 'millions/m²',
    'ML_100M2': 'mL/100 m²',
    'ML_10M2': 'ml/10 m²',
    'ML_5000GRAINES': 'mL/5000 graines',
    'ML_HA': 'mL/ha',
    'ML_KG': 'mL/kg',
    'ML_L': 'mL/L',
    'ML_M2': 'mL/m²',
    'ML_T': 'mL/t',
    'ML_UNIT': 'ml/unité',
    'MOMIES_500M2': 'momies/500 m²',
    'MOMIES_M2': 'momies/m²',
    'PERCENT': '%',
    'PER_M2': '/m²',
    'PIEGES_HA': 'pièges/ha',
    'SACHETS_HA': 'sachets/ha',
    'TABLETTES_HA': 'tablettes/ha',
    'TA_HA': 'Ta/ha',
    'T_HA': 't/ha',
    'UNITE_HA': 'unité/ha',
    'UNITE_HL': 'unité/hl'
}

UNITE_RENDEMENT = {
    'DEG_BRIX': '° Brix',
    'DEG_PURE_ALCOHOL_HA': '° d\'alcool pur/ha',
    'HL_HA': 'hl/ha',
    'HL_JUICE_HA': 'hl jus/ha',
    'HL_VIN_HA': 'hL vin/ha',
    'KG_M2': 'kg/m²',
    'KG_RAISIN_HA': 'kg raisin/ha',
    'L_HA': 'l/ha',
    'NB_CLUSTERS_HA': 'nb régime/ha',
    'NB_HA': 'nb/ha',
    'Q_HA': 'q/ha',
    'Q_HA_TO_STANDARD_HUMIDITY': 'q/ha (humidité ramenée à la norme)',
    'TONNE_HA': 't/ha',
    'TONNE_MS_HA': 't MS/ha',
    'TONNE_RACINES_HA_16_POURC': 't de racines/ha (16% de richesse)',
    'TONNE_SUGAR_HA': 't sucre/ha',
    'UNITE_HA': 'unité/ha',
    'UNITE_M2': 'unité/m²'
}

TYPE_ACTION = {
    'APPLICATION_DE_PRODUITS_FERTILISANTS_MINERAUX': 'Application de produits minéraux',
    'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES' : 'Traitements phytosanitaires : Lutte chimique et biocontrôle (produits avec AMM)',
    'AUTRE' : 'Autre',
    'ENTRETIEN_TAILLE_VIGNE_ET_VERGER': 'Entretien/Taille de vigne et verger',
    'EPANDAGES_ORGANIQUES': 'Épandage organique',
    'IRRIGATION' : 'Irrigation',
    'LUTTE_BIOLOGIQUE' : 'Traitements phytosanitaires : Produits sans AMM et macroorganismes',
    'RECOLTE' : 'Récolte',
    'SEMIS' : 'Semis',
    'TRANSPORT' :'Transport',
    'TRAVAIL_DU_SOL' : 'Travail du sol'
}

MOLECULES = {
    'n' : 'N', 
    'p' : 'P₂O₅',
    'k' : 'K₂O',
    'cao' : 'CaO',
    's' : 'S'
}


def map_boolean(values, sep='; '):
    """ permet de transformer les booléen en string """
    mapping = {'f': 'non', 't': 'oui'}
    return ', '.join(mapping[val] for val in values)
 
def convert_to_int(x):
    """ permet de convertir une colonne en int"""
    try:
        # Convert to float first, then to int
        return str(int(float(x)))
    except (ValueError, TypeError):
        return x    

def get_composant_culture_outils_can(donnees):
    """
    Permet d'obtenir toutes les informations sur les composants de culture dans le format attendu par la CAN.
    
    Arguments:
        donnees (dict): Un dictionnaire contenant les DataFrames nécessaires, incluant les données sur les composants de culture, les espèces, et les variétés.

    Retourne:
        pd.DataFrame: Un DataFrame avec les colonnes suivantes :
            - `culture_id` : Identifiant de la culture.
            - `esp_complet_var` : Espèce et variété complète (par exemple, "Trèfle blanc - Aber dai").
            - `esp_complet` : Description complète de l'espèce (par exemple, "Trèfle blanc, Qualifiant: AEE, Type saisonnier: AEE").
            - `esp` : Nom de l'espèce (par exemple, "Trèfle blanc").
            - `var` : Nom de la variété (par exemple, "Aber dai").

    Exemple d'utilisation :
        donnees = {
            'composant_culture': pd.DataFrame(...),
            'espece': pd.DataFrame(...),
            'variete': pd.DataFrame(...),
            ...
        }
        result = get_composant_culture_outils_can(donnees)

    Notes:
        - Les valeurs manquantes sont remplacées par des chaînes vides pour éviter les erreurs lors des manipulations de données.
        - Les doublons sont supprimés pour éviter plusieurs occurrences des mêmes informations dans le résultat final.
    """
    # Ajout des informations sur le composant de culture
    df_composant_culture = donnees['composant_culture'].set_index('id')
    df_espece = donnees['espece'].set_index('id')
    df_variete = donnees['variete'].set_index('id')

    # on créer un dataframe df_composant_culture_extanded contenant toutes les informations nécessaires (espece + var)
    left = df_composant_culture
    right = df_espece[
        ['libelle_espece_botanique', 'libelle_qualifiant_aee', 
         'libelle_type_saisonnier_aee', 'libelle_destination_aee']
    ]
    df_composant_culture_extanded = pd.merge(left, right, left_on='espece_id', right_index=True, how='left')

    left = df_composant_culture_extanded
    right = df_variete[
        ['denomination']
    ].rename(columns={'denomination' : 'var'})
    df_composant_culture_extanded = pd.merge(left, right, left_on='variete_id', right_index=True, how='left')

    # On fill les NaN avec ''
    df_composant_culture_extanded= df_composant_culture_extanded.fillna('')

    # On crée la description succinte de l'espèce 
    df_composant_culture_extanded.loc[:, 'esp'] = df_composant_culture_extanded[['libelle_espece_botanique']]

    # On créé la chaîne correspondant à la description complète du composant de culture
    df_composant_culture_extanded.loc[:, 'esp_complet'] = df_composant_culture_extanded[[
        'libelle_espece_botanique', 
        'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 
        'libelle_destination_aee'
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    # On ajoute l'information de la variété
    df_composant_culture_extanded.loc[
        df_composant_culture_extanded['var'] !=  '', 'var'
    ] = df_composant_culture_extanded.loc[df_composant_culture_extanded['var'] !=  '']['var']

    df_composant_culture_extanded['var'] = df_composant_culture_extanded['var'].fillna('')
    
    df_composant_cutlure_with_var = df_composant_culture_extanded.loc[df_composant_culture_extanded['var'] != '']
    df_composant_culture_extanded.loc[:,'esp_complet_var'] = df_composant_culture_extanded['esp_complet']
    df_composant_culture_extanded.loc[df_composant_cutlure_with_var.index,'esp_complet_var'] = df_composant_culture_extanded['esp_complet'] + \
        ' - '+ df_composant_culture_extanded['var']
    


    # On supprime les dupplications pour ne pas avoir plusieurs fois la même information
    df_composant_culture_extanded = df_composant_culture_extanded[
        ['culture_id', 'esp_complet_var', 'esp_complet', 'esp', 'var']
    ].drop_duplicates(subset=['esp_complet_var', 'culture_id'], keep='first')

    return df_composant_culture_extanded

# FONCTIONS POUR LES FILTRES (ACTIF + DEPHY)
def dispositif_filtres_outils_can(
        donnees
):
    """
    Sélectionne les `dispositif_id` à conserver selon les critères de la CAN.

    Cette fonction filtre les dispositifs valides en appliquant les règles suivantes :
    - Appartenance à un domaine dont la campagne est :
        - Postérieure à 1999.
        - Antérieure à 2026.
    - Le type du dispositif ne doit pas être égal à `NOT_DEPHY`.
    - Les dispositifs sont présupposés actifs dans les données fournies.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'dispositif' : DataFrame contenant les informations sur les dispositifs :
                - `id` : Identifiant unique du dispositif.
                - `domaine_id` : Référence au domaine associé.
                - `type` : Type de dispositif (ex. : `NOT_DEPHY`).
            - 'domaine' : DataFrame contenant les informations sur les domaines :
                - `id` : Identifiant unique du domaine.
                - `campagne` : Année de la campagne associée.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant une colonne `id` correspondant aux identifiants des dispositifs
            valides selon les critères CAN.

    Exemple d'utilisation :
        donnees = {
            'dispositif': pd.DataFrame(...),
            'domaine': pd.DataFrame(...)
        }
        dispositifs_filtres = dispositif_filtres_outils_can(donnees)
    """

    # dans l'entrepôt, les filtrations sur les actifs sont déjà réalisés
    df_dispositif = donnees['dispositif'].set_index('id')
    df_domaine = donnees['domaine'].set_index('id')

    # on ajoute les informations sur le domaine
    left = df_dispositif.copy()
    right = df_domaine[['campagne']].rename(columns={'campagne' : 'domaine_campagne'})
    df_dispositif = pd.merge(left, right, left_on='domaine_id', right_index=True)

    # on ne sélectionne que les domaines qui nous intéressent
    df_dispositif_filtered = df_dispositif.loc[
        (df_dispositif['domaine_campagne'] > 1999) & (df_dispositif['domaine_campagne'] < 2026) & 
        (df_dispositif['type'] != 'NOT_DEPHY')
    ]

    return  df_dispositif_filtered.reset_index()[['id']]

def domaine_filtres_outils_can(
        donnees
):
    """
    Sélectionne les `domaine_id` à conserver selon les critères de la CAN.

    Cette fonction identifie les domaines valides en appliquant les règles suivantes :
    - Les domaines doivent contenir au moins un dispositif actif.
    - Les dispositifs associés doivent respecter les critères suivants :
        - Appartenir à des campagnes postérieures à 1999 et antérieures à 2026.
        - Ne pas avoir un type de dispositif égal à `NOT_DEPHY`.
    - Remarque : Les filtrages liés aux domaines ou dispositifs actifs sont présupposés effectués
      dans les données fournies.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'dispositif' : Informations sur les dispositifs, avec les colonnes :
                - `id` : Identifiant du dispositif.
                - `domaine_id` : Référence au domaine associé.
                - `type` : Type de dispositif (ex. : `NOT_DEPHY`).
            - 'domaine' : Informations sur les domaines, avec les colonnes :
                - `id` : Identifiant du domaine.
                - `campagne` : Année de la campagne associée.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les identifiants (`id`) des domaines valides selon les critères CAN.

    Exemple d'utilisation :
        donnees = {
            'dispositif': pd.DataFrame(...),
            'domaine': pd.DataFrame(...)
        }
        result = domaine_filtres_outils_can(donnees)
    """
    df_dispositif = donnees['dispositif'].set_index('id')
    df_domaine = donnees['domaine'].set_index('id')

    # on rajoute au dispositif les informations utiles du domaine
    left = df_dispositif.copy()
    right = df_domaine[['campagne']].rename(columns={'campagne' : 'domaine_campagne'})
    df_dispositif = pd.merge(left, right, left_on='domaine_id', right_index=True)

    # on ne sélectionne que les dispositifs qui nous intéressent
    df_dispositif_filtered = df_dispositif.loc[
        (df_dispositif['domaine_campagne'] > 1999) & (df_dispositif['domaine_campagne'] < 2026) & 
        (df_dispositif['type'] != 'NOT_DEPHY')
    ]

    # on ne sélectionne que les domaines qui contiennent au moins un dispositif qui nous intéresse
    df_domaine_filtered = df_domaine.loc[
        df_domaine.index.isin(list(df_dispositif_filtered['domaine_id']))
    ]

    return  df_domaine_filtered.reset_index()[['id']]


# FONCTIONS POUR LES INTERVENTIONS EN RÉALISÉS
def get_intervention_realise_action_outils_can(
        donnees
):
    """
    Construit un DataFrame contenant les détails et les indicateurs 
    associés aux interventions réalisées, dans le format attendu par la CAN.

    Args:
        donnees (dict): 
            Un dictionnaire contenant les DataFrames suivants :
            - 'action_realise' : Actions réalisées
            - 'intervention_realise' : Interventions réalisées

    Returns:
        pd.DataFrame:
            Un DataFrame consolidé contenant les informations suivantes :
            - id : Identifiant unique de l'intervention.
            - interventions_actions : concaténation des types d'actions mobilisées dans l'intervention.
            - interventions_actions_details : concaténation des types d'actions, du psci, de la quantité d'eau... mobilisées dans l'intervention.
            - proportion_surface_traitee_phyto : Proportion de surface traitée pour les phytosanitaires.
            - proportion_surface_traitee_lutte_bio : Proportion de surface traitée pour la lutte biologique.           
            - psci_phyto : Indicateur PSCI pour les phytosanitaires.
            - psci_lutte_bio : Indicateur PSCI pour la lutte biologique.
            - quantite_eau_mm : Quantité d’eau utilisée (en mm) pour l’irrigation.

    Notes:
        - Les actions spécifiques (produits phytosanitaires, lutte biologique, irrigation) 
          sont traitées séparément pour calculer des indicateurs spécifiques.
        - Les informations sont concaténées pour obtenir des colonnes interprétables facilement

    Exemple d'utilisation :
        donnees = {
            'action_realise': pd.DataFrame(...),
            'intervention_realise': pd.DataFrame(...)
        }
        result = get_intervention_realise_action_outils_can(donnees)
    """
    df_action_realise = donnees['action_realise']
    df_intervention_realise = donnees['intervention_realise']

    # on rajoute aux actions des informations sur l'intervention
    left =  df_action_realise
    right = df_intervention_realise[['id', 'freq_spatiale', 'nombre_de_passage', 'psci_intervention', 'type']].rename(
        columns={'id' : 'intervention_realise_id', 'type' : 'type_intervention'}
    )
    df_action_realise_extanded = pd.merge(left, right, on='intervention_realise_id', how='left')

    # On rajoute l'information des types actions tel qu'attendus
    df_type_action = pd.DataFrame.from_records([TYPE_ACTION]).melt().rename(
        columns={'variable' : 'action_agrosyst', 'value' : 'action_str'}
    )

    left = df_action_realise_extanded
    right = df_type_action
    df_action_realise_extanded = pd.merge(left, right, left_on='type', right_on='action_agrosyst', how='left')


    # Pour les applications de produits phytosanitaires :
    df_action_produit_phyto = df_action_realise_extanded.loc[df_action_realise_extanded['type'] == 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES'].copy()
    df_action_produit_phyto.loc[: , 'proportion_surface_traitee_phyto'] = df_action_produit_phyto['proportion_surface_traitee']
    df_action_produit_phyto.loc[: ,'psci_phyto'] = df_action_produit_phyto['proportion_surface_traitee'] * \
          df_action_produit_phyto['freq_spatiale'] * df_action_produit_phyto['nombre_de_passage']
    # Pour la lutte biologique :
    df_action_lutte_bio = df_action_realise_extanded.loc[df_action_realise_extanded['type'] == 'LUTTE_BIOLOGIQUE'].copy()
    df_action_lutte_bio.loc[: ,'proportion_surface_traitee_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee']
    df_action_lutte_bio.loc[: ,'psci_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee'] * \
          df_action_lutte_bio['freq_spatiale'] * df_action_lutte_bio['nombre_de_passage']

    # Pour l'irrigation :
    df_action_irrigation = df_action_realise_extanded.loc[df_action_realise_extanded['type'] == 'IRRIGATION'].copy()
    df_action_irrigation.loc[: ,'quantite_eau_mm'] = df_action_irrigation['eau_qte_moy_mm'] 

    # Pour les autres :
    df_action_autres = df_action_realise_extanded.loc[
        (df_action_realise_extanded['type'] != 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES') &
        (df_action_realise_extanded['type'] != 'LUTTE_BIOLOGIQUE') &
        (df_action_realise_extanded['type'] != 'IRRIGATION')
    ].copy().groupby(['intervention_realise_id']).agg({
        'label' : ' ; '.join, 
    }).reset_index()
    
    # On obtient un dataframe qui contient tous les labels pour le détail des actions
    keeped_column_produit_phyto = ['proportion_surface_traitee_phyto', 'psci_phyto']
    keeped_column_lutte_bio = ['proportion_surface_traitee_lutte_bio', 'psci_lutte_bio']
    keeped_column_irrigation = ['quantite_eau_mm']
    keeped_column_autre = []
    merge = pd.merge(df_action_produit_phyto[keeped_column_produit_phyto+['intervention_realise_id', 'label']], 
                     df_action_lutte_bio[keeped_column_lutte_bio+['intervention_realise_id', 'label']], 
                     on='intervention_realise_id', how='outer', suffixes = ('', '_lutte_bio'))

    merge = pd.merge(merge.set_index('intervention_realise_id'), 
                     df_action_autres[keeped_column_autre+['intervention_realise_id', 'label']], 
                     left_index=True, suffixes = ('', '_autre'),
                     right_on='intervention_realise_id', how='outer').drop_duplicates(subset=['intervention_realise_id'])
    
    merge = pd.merge(merge.set_index('intervention_realise_id'), 
                     df_action_irrigation[keeped_column_irrigation+['intervention_realise_id', 'label']], 
                     left_index=True, suffixes = ('', '_irrigation'),
                     right_on='intervention_realise_id', how='outer').drop_duplicates(subset=['intervention_realise_id'])
    
    merge = merge.set_index('intervention_realise_id')

    # pour constituer la chaîne finale, on utilise une méthode vectorisée.
    merge.loc[: , 'interventions_actions_details'] = merge[['label', 'label_lutte_bio', 'label_autre', 'label_irrigation']] \
    .fillna('') \
    .agg(' ; '.join, axis=1) \
    .str.replace(r'( ; )+', ' ; ', regex=True) \
    .str.strip(' ;')

    # on groupe les actions par intervention
    df_intervention_realise_extanded = df_action_realise_extanded[['action_str', 'intervention_realise_id']].rename(columns={
        'action_str' : 'interventions_actions'
    }).groupby('intervention_realise_id').agg({
        'interventions_actions' :  lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])), 
    })

    # on rajoute à ce dataframe l'information du type d'intervention
    left = merge.reset_index()
    right = df_intervention_realise_extanded
    merge = pd.merge(left, right, left_on='intervention_realise_id', right_index=True, how='left')

    # À ce stade, on a encore des dupplication d'intervention_id : on doit grouper par intervention_id en joignant le nom des actions, mais en gardant
    # à chaque fois la valeur non nulle pour les colonnes
    intervention_actions_indicateurs = merge[[
        'intervention_realise_id', 'interventions_actions', 'interventions_actions_details', 'proportion_surface_traitee_phyto', 'psci_phyto', 
        'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm' 
    ]].rename(columns={'intervention_realise_id' : 'id'})

    return intervention_actions_indicateurs

def get_intervention_realise_semence_outils_can(
        donnees
    ):
    """
    Construit un DataFrame consolidé contenant les informations relatives 
    aux interventions de semis, dans le format attendu par la CAN.

    Args:
        donnees (dict): 
            Un dictionnaire contenant les DataFrames suivants :
            - 'semence' : Semences
            - 'composant_culture' : Composants des cultures.
            - 'espece' : Espèces.
            - 'utilisation_intrant_realise' : Utilisations d'intrants en réalisé.

    Returns:
        pd.DataFrame:
            Un DataFrame regroupant les informations suivantes par intervention réalisée :
            - especes_semees : Description complète des espèces semées (concaténation des libellés).
            - type_semence : Concaténation des types de semences utilisées.
            - densite_semis : Concaténation des doses de semis (concaténation des doses associées).
            - unite_semis : Concaténation des unités des doses de semis.
            - inoculation_biologique_semis : Concaténation du statut d’inoculation biologique (booléen oui/non) 
                                                pour toutes semences utilisées
            - traitement_chimique_semis : Concaténation du statut de traitement chimique (booléen oui/non).
                                                pour toutes les semences utilisées
    Notes:
        - Les descriptions des espèces semées sont générées à partir des colonnes :
          `libelle_espece_botanique`, `libelle_qualifiant_aee`, `libelle_type_saisonnier_aee`, 
          et `libelle_destination_aee`.
        - Les informations sur les semences sont croisées avec celles des intrants pour inclure 
          les doses et les unités associées.
        - Les champs booléens (inoculation biologique, traitement chimique) sont regroupés et 
          concaténés sous forme lisible.

    Exemple d'utilisation :
        donnees = {
            'semence': pd.DataFrame(...),
            'composant_culture': pd.DataFrame(...),
            'espece': pd.DataFrame(...),
            'utilisation_intrant_realise': pd.DataFrame(...)
        }
        result = get_intervention_realise_semence_outils_can(donnees)
    """
    df_semence = donnees['semence']
    df_composant_culture = donnees['composant_culture']
    df_espece = donnees['espece']
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise']

    # OBTENTION DES INFORMATIONS POUR LES INTERVENTIONS DE TYPE SEMENCES.
    left = df_semence.rename(columns={'espece_id':'composant_culture_id'}) # attention, on est obligé de corriger car il y a une erreur dans le nom de la colonne sur Datagrosyst.
    right = df_composant_culture[['id', 'espece_id', 'variete_id']].rename(columns={'id' : 'composant_culture_id'})
    df_semence_extanded = pd.merge(left, right, on='composant_culture_id', how='left')

    left = df_semence_extanded
    right = df_espece[['id', 'libelle_espece_botanique', 'libelle_qualifiant_aee', 'libelle_type_saisonnier_aee', 'libelle_destination_aee']].rename(columns={'id' : 'espece_id'})
    df_semence_extanded = pd.merge(left, right, on='espece_id', how='left')

    df_semence_extanded = df_semence_extanded.fillna('')

    df_semence_extanded['description'] = df_semence_extanded[[
        'libelle_espece_botanique', 'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 'libelle_destination_aee', 
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    # ajout des informations des semences sur les utilsiation d'intrants
    left = df_utilisation_intrant_realise[['intervention_realise_id', 'intrant_id', 'dose', 'unite', 'semence_id']].dropna(subset=['semence_id'])
    right = df_semence_extanded.rename(columns={'id' : 'semence_id'})
    df_utilisation_intrant_realise_extanded = pd.merge(left, right, on='semence_id', how='inner')

    df_utilisation_intrant_realise_extanded['dose'] = df_utilisation_intrant_realise_extanded['dose'].astype('str')

    # on groupe par intervention
    df_intervention_semence = df_utilisation_intrant_realise_extanded.fillna('').groupby([
        'intervention_realise_id'
    ]).agg({
        'description' :  ' ; '.join,
        'type_semence' :  ', '.join,
        'dose' : ' , '.join,
        'unite' : ', '.join, 
        'inoculation_biologique' : lambda x: map_boolean(x, sep=', '),
        'traitement_chimique' : lambda x: map_boolean(x, sep=', ')
    })

    return df_intervention_semence.rename(columns={
        'description' : 'especes_semees', 
        'dose' : 'densite_semis', 
        'unite' : 'unite_semis', 
        'traitement_chimique' : 'traitement_chimique_semis',
        'inoculation_biologique' : 'inoculation_biologique_semis'
    })

def get_intervention_realise_outils_can_context(
    donnees
):
    """
    Construit un DataFrame contenant le contexte des interventions réalisées,
    en regroupant les informations sur les actions, les semences et les indicateurs associés,
    au format attendu par la CAN.

    Args:
        donnees (dict): 
            Un dictionnaire contenant les DataFrames nécessaires à la construction :
            - 'intervention_realise' : Détails des interventions réalisées.
            - Autres tables nécessaires pour appeler les fonctions :
              `get_intervention_realise_action_outils_can` et 
              `get_intervention_realise_semence_outils_can`.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations des interventions :
            - id : Identifiant unique de l'intervention.
            - interventions_actions : Concaténation des types d'actions mobilisées.
            - especes_semees : Concaténation des description complète des espèces semées.
            - densite_semis : Concaténation des densités des semis (concaténation des doses associées).
            - unite_semis : Concaténation des unités des densités de semis.
            - traitement_chimique_semis : Concaténation des statuts de traitement chimique des semences.
            - inoculation_biologique_semis : Concaténation des statuts d’inoculation biologique des semences.
            - type_semence : Concaténation des types de semences utilisées.
            - proportion_surface_traitee_phyto : Proportion de surface traitée (phytosanitaires).
            - proportion_surface_traitee_lutte_bio : Proportion de surface traitée (lutte biologique).
            - psci_phyto : Indicateur PSCI (phytosanitaires).
            - psci_lutte_bio : Indicateur PSCI (lutte biologique).
            - quantite_eau_mm : Quantité d’eau utilisée (en mm) pour l’irrigation.

    Notes:
        - Cette fonction utilise les résultats des fonctions 
          `get_intervention_realise_action_outils_can` et 
          `get_intervention_realise_semence_outils_can` pour enrichir les données.
        - Les colonnes finales sont sélectionnées pour correspondre au format attendu par la CAN.

    Exemple d'utilisation :
        donnees = {
            'intervention_realise': pd.DataFrame(...),
            'action_realise': pd.DataFrame(...),
            'semence': pd.DataFrame(...),
            ...
        }
        result = get_intervention_realise_outils_can_context(donnees)
    """
    df_intervention_realise = donnees['intervention_realise']

    # ajout des informations sur les différents indicateurs
    left = df_intervention_realise
    right = get_intervention_realise_action_outils_can(donnees).rename(columns={'intervention_realise_id': 'id'} )
    merge = pd.merge(left, right, on='id', how='left')
    
    # ajout des informations sur la table semis
    left = merge 
    right = get_intervention_realise_semence_outils_can(donnees).reset_index().rename(columns={'intervention_realise_id': 'id'})
    merge = pd.merge(left, right, on='id', how='left')

    columns = ['id', 'interventions_actions', 'especes_semees', 'densite_semis', 'unite_semis', 'traitement_chimique_semis', 
               'inoculation_biologique_semis', 'type_semence', 'proportion_surface_traitee_phyto', 'psci_phyto', 
               'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    # ajout des informations sur les espèces concernées
    return merge[columns]

def get_intervention_realise_combinaison_outils_can(
    donnees
):
    """
    Génère un DataFrame contenant les informations détaillées sur les combinaisons d'outils 
    utilisées dans les interventions.

    Cette fonction enrichit les données des interventions en ajoutant des détails sur 
    les combinaisons d'outils, y compris les informations sur les tracteurs, les matériels 
    associés et leurs caractéristiques.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - `intervention_realise` : 
                - `id` : Identifiant unique de l'intervention.
                - `combinaison_outil_id` : Référence à une combinaison d'outils.
            - `combinaison_outil` :
                - `id` : Identifiant unique de la combinaison d'outils.
                - `nom` : Nom de la combinaison d'outils.
                - `tracteur_materiel_id` : Référence au tracteur ou matériel principal.
            - `materiel` :
                - `id` : Identifiant unique du matériel.
                - `nom` : Nom du matériel.
                - `type_materiel` : Type du matériel.
                - `materiel_caracteristique1` : Première caractéristique du matériel 
                  (ex. : tracteur ou automoteur, type d'outil).
            - `combinaison_outil_materiel` :
                - `combinaison_outil_id` : Référence à une combinaison d'outils.
                - `materiel_id` : Référence à un matériel spécifique.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les colonnes suivantes :
            - `id` : Identifiant unique de l'intervention.
            - `combinaison_outils_nom` : Nom de la combinaison d'outils associée.
            - `tracteur_ou_automoteur` : Type du tracteur ou automoteur utilisé.
            - `outils` : Concaténation des outils utilisés, séparés par `;`.

    Exemple d'utilisation :
        donnees = {
            'intervention_realise': pd.DataFrame(...),
            'combinaison_outil': pd.DataFrame(...),
            'materiel': pd.DataFrame(...),
            'combinaison_outil_materiel': pd.DataFrame(...)
        }
        result = get_intervention_realise_combinaison_outils_can(donnees)
    """
    df_intervention_realise = donnees['intervention_realise']
    df_combinaison_outil = donnees['combinaison_outil'].set_index('id')
    df_materiel = donnees['materiel'].set_index('id')
    df_combinaison_outil_materiel = donnees['combinaison_outil_materiel']

    # Ajout des informations sur le tracteur à la combinaison d'outils 
    left = df_combinaison_outil[['nom', 'tracteur_materiel_id']]
    right = df_materiel[['nom', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'nom_tracteur', 'materiel_caracteristique1' : 'tracteur_ou_automoteur'}
    )
    df_combinaison_outil_extanded = pd.merge(left, right, left_on='tracteur_materiel_id', right_index=True, how='left')

    # Ajout des informations sur le materiel à la combinaison d'outils
    left = df_combinaison_outil_materiel
    right = df_materiel[['nom', 'type_materiel', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'combinaison_outils_nom', 'materiel_caracteristique1' : 'outils'}
    )
    df_combinaison_outil_materiel= pd.merge(left, right, left_on='materiel_id', right_index=True, how='left')

    # On considère que si plusieurs matériels ont les mêmes caractéristiques (outils)
    # Alors il n'y a pas besoin de remonter plusieurs fois l'information dans l'agrégation 
    # (Correction par rapport aux exports en masse historiques)
    df_combinaison_outil_materiel = df_combinaison_outil_materiel.drop_duplicates(
        subset=['combinaison_outil_id', 'outils']
    )

    # On rassemble tous les materiels pour n'avoir qu'une description par combinaison d'outils
    df_combinaison_outil_materiel['outils'] = df_combinaison_outil_materiel['outils'].fillna('')
    df_combinaison_outil_materiel_grouped = df_combinaison_outil_materiel.groupby('combinaison_outil_id').agg({
        'outils' : ' ; '.join, # delete NaN
    })

    # On mets toutes les informations dans le même dataframe
    left = df_combinaison_outil_extanded
    right = df_combinaison_outil_materiel_grouped
    df_combinaison_outil_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # On agrège les informations au dataframe des interventions
    left = df_intervention_realise[['id', 'combinaison_outil_id']]
    right = df_combinaison_outil_extanded.rename(columns={'nom' : 'combinaison_outils_nom'})[
        ['combinaison_outils_nom', 'tracteur_ou_automoteur', 'outils']
    ]

    merge = pd.merge(left, right, left_on='combinaison_outil_id', right_index=True, how='left')

    return merge

def get_intervention_realise_culture_outils_can(
    donnees
):
    """
    Construit un DataFrame consolidé contenant les informations relatives aux cultures 
    dans le cadre des interventions réalisées, selon le format attendu par la CAN.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'intervention_realise' : Informations sur les interventions réalisées.
            - 'noeuds_realise' : Détails sur les noeuds réalisés, incluant les cultures annuelles (assolées) et intermédiaires.
            - 'plantation_perenne_realise' : Informations sur les cultures pérennes.
            - 'plantation_perenne_phases_realise' : Détails sur les phases des plantations pérennes.
            - 'composant_culture_concerne_intervention_realise' : Liens entre les composants culture et les interventions.
            - 'connection_realise' : Informations sur les connexions des noeuds réalisés, incluant les cultures intermédiaires.
            - 'composant_culture' : Composants de culture.

    Returns:
        pd.DataFrame:
            Un DataFrame regroupant les informations suivantes par intervention réalisée :
            - `esp_complet_var` : Concaténation complète des espèces et variétés associées.
            - `esp_complet` : Concaténation des espèces complètes sans doublons.
            - `esp` : Concaténation des espèces associées (sans doublons) pour chaque intervention.
            - `var` : Concaténation des variétés associées (sans doublons) pour chaque intervention.

    Notes:
        - Les informations sont combinées pour inclure à la fois les cultures annuelles, intermédiaires, et pérennes.
        - Les doublons dans les listes d'espèces et variétés sont supprimés pour fournir des descriptions uniques.
        - La concaténation des informations est réalisée avec des séparateurs lisibles (ex. : '; ' pour les listes).

    Exemple d'utilisation :
        donnees = {
            'intervention_realise': pd.DataFrame(...),
            'noeuds_realise': pd.DataFrame(...),
            'plantation_perenne_realise': pd.DataFrame(...),
            'plantation_perenne_phases_realise': pd.DataFrame(...),
            'composant_culture_concerne_intervention_realise': pd.DataFrame(...),
            'connection_realise': pd.DataFrame(...),
            'composant_culture': pd.DataFrame(...)
        }
        result = get_intervention_realise_culture_outils_can(donnees)
    """
    df_intervention_realise = donnees['intervention_realise'].set_index('id')
    df_noeuds_realise = donnees['noeuds_realise'].set_index('id')
    df_plantation_perenne_phases_realise = donnees['plantation_perenne_phases_realise'].set_index('id')
    df_plantation_perenne_realise = donnees['plantation_perenne_realise'].set_index('id')
    df_composant_culture_concerne_intervention_realise = donnees[
        'composant_culture_concerne_intervention_realise'
    ].set_index('id')
    df_connection_realise = donnees['connection_realise'].set_index('id')

    # informations sur le composants cultures, dans le format attendu
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees)

    # on ajoute aussi l'information de la culture intermédiaire si il y en a une
    left = df_noeuds_realise.reset_index()
    right = df_connection_realise.reset_index().rename(columns={'id' : 'connection_realise_id'})
    df_noeuds_realise_extanded = pd.merge(left, right, left_on='id', right_on='cible_noeuds_realise_id', how='left').set_index('id')

    left = df_noeuds_realise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_noeuds_realise_extanded_ci = pd.merge(left, right, left_on='culture_intermediaire_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    # informations assolée
    left = df_noeuds_realise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_noeuds_realise_extanded = pd.merge(left, right, left_on='culture_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    # informations perennes
    left = df_plantation_perenne_realise.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_plantation_perenne_realise_extanded = pd.merge(
        left, right, left_on='culture_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    left = df_plantation_perenne_phases_realise.reset_index()
    right = df_plantation_perenne_realise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_realise_id'})
    df_plantation_perenne_phases_realise_extanded = pd.merge(
        left, right, on='plantation_perenne_realise_id', how='left').set_index('id')

    # on ajoute l'information du noeuds où porte l'intervention
    left = df_composant_culture_concerne_intervention_realise
    right = df_intervention_realise[['noeuds_realise_id', 'plantation_perenne_phases_realise_id']]
    df_composant_culture_concerne_intervention_extanded = pd.merge(
        left, right, left_on='intervention_realise_id', right_index=True, how='left')

    # maintenant qu'on a tout, pour l'assolée :
    left = df_composant_culture_concerne_intervention_extanded.dropna(subset=['noeuds_realise_id'])
    right = df_noeuds_realise_extanded
    df_composant_culture_concerne_intervention_extanded_assolee = pd.merge(left, right, 
        left_on=['noeuds_realise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    left = df_composant_culture_concerne_intervention_extanded.dropna(subset=['noeuds_realise_id'])
    right = df_noeuds_realise_extanded_ci
    df_composant_culture_concerne_intervention_extanded_assolee_ci = pd.merge(left, right, 
        left_on=['noeuds_realise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    df_composant_culture_concerne_intervention_extanded_assolee = pd.concat([
        df_composant_culture_concerne_intervention_extanded_assolee,
        df_composant_culture_concerne_intervention_extanded_assolee_ci
    ])

    # pour le perenne :
    left = df_composant_culture_concerne_intervention_extanded.reset_index().dropna(subset=['plantation_perenne_phases_realise_id'])
    right = df_plantation_perenne_phases_realise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_phases_realise_id'})

    df_composant_culture_concerne_intervention_extanded_perenne = pd.merge(left, right,
        on=['plantation_perenne_phases_realise_id', 'composant_culture_id'],
        how='inner'
    )

    df_final_perenne = df_composant_culture_concerne_intervention_extanded_perenne.groupby([
        'intervention_realise_id'
    ]).agg({
        'esp_complet_var' : ' ; '.join, 
        'esp_complet' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'esp': lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'var' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()]))
    })
    df_final_assolee = df_composant_culture_concerne_intervention_extanded_assolee.groupby([
        'intervention_realise_id'
    ]).agg({
        'esp_complet_var' : ' ; '.join,
        'esp_complet' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'esp': lambda x: ' ; '.join(dict.fromkeys([item for item in x if item.strip()])),
        'var' : lambda x: '; '.join(dict.fromkeys([item for item in x if item.strip()]))
    })

    df_intervention_realise_final = pd.concat([df_final_assolee, df_final_perenne])

    return df_intervention_realise_final.reset_index().rename(columns={'intervention_realise_id' : 'id'})

def get_intervention_realise_culture_prec_outils_can(
        donnees
):
    """
    Permet d'obtenir le DataFrame des informations sur les cultures précédentes pour les interventions
    dans le cadre de la CAN.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'intervention_realise' : Informations sur les interventions réalisées.
            - 'noeuds_realise' : Détails sur les noeuds réalisés, incluant les cultures annuelles et leurs connexions.
            - 'connection_realise' : Informations sur les connexions entre les noeuds réalisés.
            - 'culture' : Informations sur les cultures et les composants associés (espèces, variétés, etc.).

    Returns:
        pd.DataFrame:
            Un DataFrame avec les informations suivantes par intervention réalisée :
            - `precedent_id` : Identifiant de la culture précédente (ou du noeud précédent).
            - `precedent_nom` : Nom de la culture précédente (ou du noeud précédent).
            - `precedent_especes_edi` : Espèces associées à la culture précédente dans le format attendu par la CAN.

    Exemple d'utilisation :
        donnees = {
            'intervention_realise': pd.DataFrame(...),
            'noeuds_realise': pd.DataFrame(...),
            'connection_realise': pd.DataFrame(...),
            'culture': pd.DataFrame(...)
        }
        result = get_intervention_realise_culture_prec_outils_can(donnees)
    """
    df_intervention_realise = donnees['intervention_realise'].set_index('id')
    df_noeuds_realise = donnees['noeuds_realise'].set_index('id')
    df_connection_realise = donnees['connection_realise'].set_index('id')
    df_culture = donnees['culture'].set_index('id')

    # Obtention des informations sur le composant culture, dans le format attendu par la CAN
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees)

    df_culture_grouped = df_composant_culture_extanded.groupby('culture_id').agg({
        'esp_complet' : ' ; '.join
    })

    left = df_culture
    right = df_culture_grouped
    df_culture_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df_noeuds_realise
    right = df_culture_extanded[['nom', 'esp_complet']]
    df_noeuds_realise_extanded = pd.merge(
        left, right, left_on='culture_id', right_index=True, how='left'
    )

    left = df_connection_realise.dropna(subset=['source_noeuds_realise_id'])
    right = df_noeuds_realise_extanded.rename(
        columns={
            'culture_id' : 'precedent_id', 
            'esp_complet' : 'precedent_especes_edi', 
            'nom': 'precedent_nom'
        }
    )
    df_connection_realise_extanded = pd.merge(
        left, right, left_on='source_noeuds_realise_id', right_index=True, how='left'
    )

    left = df_intervention_realise.reset_index().dropna(subset=['noeuds_realise_id'])
    right = df_connection_realise_extanded
    df_intervention_realise_extanded = pd.merge(
        left, right, left_on='noeuds_realise_id', right_on='cible_noeuds_realise_id', how='inner'
    ).set_index('id')

    final = df_intervention_realise_extanded[
        ['precedent_id', 'precedent_nom', 'precedent_especes_edi']
    ]
    return final.reset_index()

def get_intervention_realise_outils_can(
    donnees
):
    """
    Permet d'obtenir un DataFrame contenant toutes les colonnes complexes nécessaires pour le DataFrame
    `intervention_realise` du magasin CAN (sert également pour `intervention_realise_performance`).

    Cette fonction effectue une série de fusions entre plusieurs DataFrames afin de collecter toutes les informations
    pertinentes liées aux interventions réalisées, telles que les informations sur les outils utilisés, les cultures
    concernées, les intrants, les rendements, les cibles d'intervention et le nombre d'intrants associés.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'intervention_realise' : Détails sur les interventions réalisées.
            - 'combinaison_outil' : Détails sur les combinaisons d'outils utilisés dans les interventions.
            - 'culture' : Informations sur les cultures concernées.
            - 'culture_prec' : Informations sur les cultures précédentes.
            - 'intrants' : Informations sur les intrants utilisés lors des interventions.
            - 'cibles' : Cibles d'intervention définies.
            - 'rendement' : Informations sur les rendements obtenus suite aux interventions.
            - 'nb_intrants' : Informations sur le nombre d'intrants utilisés dans les interventions.

    Returns:
        pd.DataFrame:
            Un DataFrame qui contient les informations suivantes par intervention réalisée :
            - Détails sur l'intervention, les outils utilisés, les cultures concernées, les rendements, les intrants, etc.

    Notes:
        - Les colonnes calculées, comme `nb_intrants`, sont traitées pour garantir l'intégrité des données, par exemple
          avec des valeurs `NaN` remplacées par 0.

    Exemple d'utilisation :
        donnees = {
            'intervention_realise': pd.DataFrame(...),
            'combinaison_outil': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'culture_prec': pd.DataFrame(...),
            'intrants': pd.DataFrame(...),
            'cibles': pd.DataFrame(...),
            'rendement': pd.DataFrame(...),
            'nb_intrants': pd.DataFrame(...)
        }
        result = get_intervention_realise_outils_can(donnees)
    """
    # ajout des informations de contexte sur l'intervention
    left = get_intervention_realise_outils_can_context(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    right = get_intervention_realise_combinaison_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # ajout des informations sur la culture concernée par l'intervention
    left = merge
    right = get_intervention_realise_culture_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # ajout des informations sur la culture précédente
    left = merge
    right = get_intervention_realise_culture_prec_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # ajout des informations sur les intrants utilisés dans l'intervention :
    left = merge
    right = get_intervention_realise_intrants_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # # ajout des informations sur les interventions cible : 
    left = merge
    right = get_intervention_realise_cibles_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # ajout des informations sur les rendements :
    left = merge 
    right = get_intervention_realise_rendement_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # ajout des informations sur le nombre d'intrants dans l'intervention
    left = merge
    right = get_intervention_realise_nb_intrant_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')
    merge.loc[:, 'nb_intrants'] = merge['nb_intrants'].fillna(0)


    return merge.rename(columns={'intervention_realise_id': 'id'})


def get_intervention_realise_intrants_outils_can(
        donnees
):
    """
    Permet d'obtenir, pour chaque intervention synthétisée, la liste des intrants utilisés dans l'intervention,
    dans le format attendu par la CAN. Par exemple, pour une intervention spécifique, la sortie peut ressembler à :
    "CUPROXAT SC (0.5 L/ha), CUIVROL (0.5 kg/ha), HELIOSOUFRE S (4.0 L/ha), LAMINAFLOR (2.0 l/ha)".

    Cette fonction traite les informations relatives aux intrants, leur type (autre, semis, etc.), et les doses utilisées
    dans l'intervention, puis les assemble dans une chaîne de caractères formatée. 

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'utilisation_intrant_realise' : Détails sur les intrants utilisés dans chaque intervention.
            - 'intrant' : Informations sur les intrants (nom, type, unité).
        variable(s) globale(s) :
            'UNITE_APPLICATION' : Information sur les unités d'application des intrants.
    Returns:
        pd.DataFrame:
            Un DataFrame contenant les intrants utilisés pour chaque intervention, formaté comme suit :
            - `interventions_intrants` : Liste des intrants utilisés, formatée avec leur nom, dose et unité.
            - `biocontrole` : Indication de si un biocontrôle a été utilisé (`'oui'` ou `'non'`).

    Notes:
        - La fonction traite différemment les intrants de type 'AUTRE' et 'SEMIS' par rapport aux autres types.
        - Les valeurs `NaN` sont remplies par des chaînes vides ou des valeurs par défaut.
        
    Exemple d'utilisation :
        UNITE_APPLICATION = {'AA_HA': 'Aa/ha', ...}
        donnees = {
            'utilisation_intrant_realise': pd.DataFrame(...),
            'intrant': pd.DataFrame(...),
        }
        result = get_intervention_realise_intrants_outils_can(donnees)
    """
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise'].set_index('id')
    df_intrant = donnees['intrant'].set_index('id')

    df_unite_application = pd.DataFrame.from_records([UNITE_APPLICATION]).melt().rename(
        columns={'variable' : 'unite_agrosyst', 'value' : 'unite_utilisateur'}
    )

    left = df_utilisation_intrant_realise
    right = df_intrant
    merge = pd.merge(left, right, left_on='intrant_id', right_index=True, how='left')

    # ON TRAITE DIFFÉREMENT SI IL S'AGIT D'UN INTRANT AUTRE OU NON (CAS != INTRANT AUTRE )
    left = merge.loc[(merge['type'] != 'AUTRE') & (merge['type'] != 'SEMIS')].reset_index()
    right = df_unite_application
    merge_application = pd.merge(left, right, left_on='unite', right_on='unite_agrosyst', how='left').set_index('id')

    # utiliser le ref_nom ou le nom utilisateur ? --> il semble que ce soit le nom_utilisateur
    merge_application.loc[:, 'interventions_intrants'] = (merge_application['nom_utilisateur']) + ' ('+merge_application['dose'].astype('str')+ ' '+merge_application['unite_utilisateur']+')'
    merge_application['interventions_intrants'] = merge_application['interventions_intrants'].fillna('')

    # INTRANT AUTRE
    merge_autre = merge.loc[(merge['type'] == 'AUTRE')]
    merge_autre.loc[:, 'interventions_intrants'] = (merge_autre['type']) + ' - ' + (merge_autre['nom_utilisateur'])
    merge_autre['interventions_intrants'] = merge_autre['interventions_intrants'].fillna('')

    # INTRANT SEMIS
    merge_semis = merge.loc[(merge['type'] == 'SEMIS')]
    merge_semis.loc[:, 'interventions_intrants'] = (merge_semis['nom_utilisateur'])
    merge_semis['interventions_intrants'] = merge_semis['interventions_intrants'].fillna('')

    merge = pd.concat([merge_application, merge_autre, merge_semis])
    merge['biocontrole'] = merge['biocontrole'].fillna('f').replace({'t': True, 'f': False})

    res = merge[['interventions_intrants', 'intervention_realise_id', 'biocontrole']].groupby('intervention_realise_id').agg({
        'interventions_intrants' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'biocontrole' : 'max'
    })

    res['biocontrole'] = res['biocontrole'].replace({False: 'non', True : 'oui'})


    return res.reset_index().rename(columns={'intervention_realise_id' : 'id'})


def get_intervention_realise_cibles_outils_can(
        donnees
):
    """
    Permet d'obtenir, pour chaque intervention réalisée, un champs de concaténation des cibles concernées par l'intervention,
    dans le format attendu par la CAN. Par exemple, pour une intervention spécifique, la sortie pourrait être :
    "Helminthosporiose, Rhynchosporiose".

    Cette fonction traite les cibles d'intrants (nuisibles, adventices) associées aux interventions réalisées et les
    concatène dans une chaîne de caractères formatée, séparée par des virgules.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'utilisation_intrant_realise' : Détails sur les intrants utilisés dans chaque intervention.
            - 'utilisation_intrant_cible' : Détails sur les cibles associées aux intrants dans chaque intervention.
            - 'nuisible_edi' : Informations sur les nuisibles (avec une colonne `label_nuisible`).
            - 'adventice' : Informations sur les adventices (avec une colonne `label`).

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les cibles associées à chaque intervention, formaté comme suit :
            - `interventions_cibles_trait` : Liste des cibles concernées par l'intervention, formatée comme une chaîne de caractères séparée par des virgules.

    Notes:
        - La fonction regroupe les cibles par intervention et les formatte en une seule ligne pour chaque intervention.
        - Les cibles qui n'ont pas de nom (valeurs `NaN`) se voient attribuer un nom vide.
        - Les cibles sont regroupées par leur `intervention_realise_id`.

    Exemple d'utilisation :
        donnees = {
            'utilisation_intrant_realise': pd.DataFrame(...),
            'utilisation_intrant_cible': pd.DataFrame(...),
            'nuisible_edi': pd.DataFrame(...),
            'adventice': pd.DataFrame(...)
        }
        result = get_intervention_realise_cibles_outils_can(donnees)
    """
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise'].set_index('id')
    df_utilisation_intrant_cible = donnees['utilisation_intrant_cible'].set_index('id')
    df_nuisible_edi = donnees['nuisible_edi'].set_index('id')
    df_adventice = donnees['adventice'].set_index('id')

    # on associe à chaque cible d'utilisation d'intrants les informations sur la cible
    left = df_utilisation_intrant_cible
    df_nuisible_edi = df_nuisible_edi[['label_nuisible']].rename(columns={'label_nuisible' : 'label'})
    right = pd.concat([df_nuisible_edi, df_adventice])
    merge = pd.merge(left, right, left_on='ref_cible_id', right_index=True, how='left')[['label', 'utilisation_intrant_id']]

    # on ajoute l'information de l'intervention
    left = merge 
    right = df_utilisation_intrant_realise[['intervention_realise_id']]
    merge = pd.merge(left, right, left_on='utilisation_intrant_id', right_index=True, how='left')
    
    # pour les cibles qui n'ont pas de noms, on affecte un nom vide
    merge['label'] = merge['label'].fillna('')

    res = merge.groupby(['intervention_realise_id']).agg({
        'label' :  lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()]))
    }).rename(columns={'label' : 'interventions_cibles_trait'})

    return res.reset_index().rename(columns={'intervention_synthetise_id' : 'id'})


def get_intervention_realise_rendement_outils_can(
    donnees
):
    """
    Permet d'obtenir, pour chaque intervention réalisée, la liste des rendements et destinations
    associées à l'intervention, formatée comme attendu par la CAN. Par exemple, pour une intervention spécifique 
    (fr.inra.agrosyst.api.entities.effective.EffectiveIntervention_1bca5b10-af00-4883-bfb9-52674a4b5da6) :
    "[Grain (alimentation humaine)]|43,0|q/ha (humidité ramenée à la norme)".

    Cette fonction collecte les informations de rendement, les formate selon les conventions attendues,
    puis les agrège pour chaque intervention.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'recolte_rendement_prix' : Informations sur les rendements, destinations et unités.
            - 'action_realise' : Actions associées aux interventions réalisées.
        variable(s) globale(s) :
            'UNITE_RENDEMENT' : Dictionnaire global contenant la correspondance entre les unités internes 
              et les unités utilisateur.
    Returns:
        pd.DataFrame:
            Un DataFrame contenant, pour chaque intervention, les rendements associés formatés comme suit :
            - `id` : Identifiant unique de l'intervention réalisée.
            - `rendement_total` : Chaîne de caractères représentant les rendements formatés, 
              séparés par des `#` s'il y a plusieurs rendements. 

    Notes:
        - Le format final d'un rendement est : `[Destination]|Rendement Moyen|Unité`.
        - Les rendements sont regroupés par `intervention_realise_id`.
        - L'unité interne (`rendement_unite`) est convertie dans une unité utilisateur via le mapping `UNITE_RENDEMENT`.

    Exemple d'utilisation :
        donnees = {
            'recolte_rendement_prix': pd.DataFrame(...),
            'action_realise': pd.DataFrame(...),
        }
        UNITE_RENDEMENT = {}
        result = get_intervention_realise_rendement_outils_can(donnees)
    """
    recolte_rendement_prix = donnees['recolte_rendement_prix'].set_index('id')
    action_realise = donnees['action_realise'].set_index('id')
    unite_rendement = pd.DataFrame.from_records([UNITE_RENDEMENT]).melt().rename(
        columns={'variable' : 'unite_agrosyst', 'value' : 'unite_utilisateur'}
    )

    left = recolte_rendement_prix
    right = action_realise[['intervention_realise_id']]
    recolte_rendement_prix_extanded = pd.merge(left, right, left_on='action_id', right_index=True, how='left')

    left = recolte_rendement_prix_extanded
    right = unite_rendement
    recolte_rendement_prix_extanded = pd.merge(left, right, left_on='rendement_unite', right_on='unite_agrosyst', how='left')


    recolte_rendement_prix_extanded['rendement_total'] = '['+recolte_rendement_prix_extanded['destination'].astype('str')+']'+'|'+\
        recolte_rendement_prix_extanded['rendement_moy'].astype('str')+'|'+\
            recolte_rendement_prix_extanded['unite_utilisateur'].astype('str')

    
    res = recolte_rendement_prix_extanded.groupby('intervention_realise_id').agg({
        'rendement_total' : lambda x: '#'.join(dict.fromkeys([item for item in x if item.strip()])),
    })

    return res.reset_index().rename(columns={'intervention_realise_id' : 'id'})


def get_intervention_realise_nb_intrant_outils_can(
        donnees
):
    """
    Permet d'obtenir, pour chaque intervention réalisée, le nombre d'utilisations d'intrants 
    associées à cette intervention.

    Par exemple :
    Pour l'intervention `EffectiveIntervention_b33f89ad-3489-4a84-873b-eddafd9db459`, le résultat serait `0` 
    si aucun intrant n'a été utilisé.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'utilisation_intrant_realise' : Informations sur les utilisations d'intrants.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant, pour chaque intervention réalisée, le nombre total d'utilisations 
            d'intrants :
            - `id` : Identifiant unique de l'intervention réalisée.
            - `nb_intrants` : Nombre d'utilisations d'intrants pour cette intervention.

    Exemple d'utilisation :
        donnees = {
            'utilisation_intrant_realise': pd.DataFrame(...)
        }
        result = get_intervention_realise_nb_intrant_outils_can(donnees)
    """
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise']

    res = df_utilisation_intrant_realise.groupby('intervention_realise_id').agg({
        'id' : 'count'
    }).rename(columns={'id' : 'nb_intrants'})

    return res.reset_index().rename(columns={'intervention_realise_id' : 'id'})

# FONCTIONS POUR LES INTERVENTIONS EN SYNTHÉTISÉ

def get_intervention_synthetise_culture_outils_can(
      donnees  
):
    """
    Permet d'obtenir un DataFrame contenant les informations détaillées sur les cultures 
    associées aux interventions synthétisées, dans un format conforme à celui attendu par la CAN.

    Cette fonction agrège et restructure des données complexes provenant de plusieurs tables 
    pour fournir des informations synthétisées sur les cultures (assolées et pérennes) 
    dans les interventions.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'intervention_synthetise' : Informations sur les interventions synthétisées.
            - 'noeuds_synthetise' : Détails sur les nœuds de culture synthétisés.
            - 'connection_synthetise' : Informations sur les connections entre les nœuds.
            - 'plantation_perenne_phases_synthetise' : Données sur les phases des plantations pérennes.
            - 'plantation_perenne_synthetise' : Détails sur les plantations pérennes.
            - 'composant_culture_concerne_intervention_synthetise' : Composants de culture associés aux interventions.
            - 'noeuds_synthetise_restructure' : Dataframe de restructuration des nœuds synthétisés.
            - 'plantation_perenne_synthetise_restructure' : Dataframe de restructuration des plantations pérennes.
            - 'ccc_intervention_synthetise_restructure' : Dataframe de restructuration des composants de culture.
            - 'connection_synthetise_restructure' : Dataframe de restructuration des connections synthétisées.
            - 'culture' : Informations générales sur les cultures.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations sur les cultures par intervention synthétisée :
            - `id` : Identifiant de l'intervention synthétisée.
            - `esp_complet_var` : Liste complète des espèces et variétés concernées, séparées par des "; ".
            - `esp_complet` : Liste unique des espèces complètes, séparées par des ", ".
            - `esp` : Liste unique des espèces, séparées par des ", ".
            - `var` : Liste unique des variétés, séparées par des ", ".
            - `culture_id` : Identifiant unique de la culture.
            - `culture_nom` : Nom de la culture.

    Exemple d'utilisation :
        donnees = {
            'intervention_synthetise': pd.DataFrame(...),
            'noeuds_synthetise': pd.DataFrame(...),
            'connection_synthetise': pd.DataFrame(...),
            ...
        }
        result = get_intervention_synthetise_culture_outils_can(donnees)
    """
    df_intervention_synthetise = donnees['intervention_synthetise'].set_index('id')
    df_noeuds_synthetise = donnees['noeuds_synthetise'].set_index('id')
    df_connection_synthetise = donnees['connection_synthetise'].set_index('id')
    df_plantation_perenne_phases_synthetise = donnees['plantation_perenne_phases_synthetise'].set_index('id')
    df_plantation_perenne_synthetise = donnees['plantation_perenne_synthetise'].set_index('id')
    df_composant_culture_concerne_intervention_synthetise = donnees[
        'composant_culture_concerne_intervention_synthetise'
    ].set_index('id')
    df_noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure'].set_index('id')
    df_plantation_perenne_synthetise_restructure = donnees['plantation_perenne_synthetise_restructure'].set_index('id')
    df_composant_culture_concerne_intervention_synthetise_restructure = donnees[
        'ccc_intervention_synthetise_restructure'
    ].set_index('id')
    df_connection_synthetise_restructure = donnees['connection_synthetise_restructure'].set_index('id')
    df_culture = donnees['culture'].set_index('id')

    left = df_connection_synthetise
    right = df_connection_synthetise_restructure
    df_connection_synthetise_extanded_prim = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # informations sur les composants cultures, dans le format attendu par la CAN
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees)

    # reconstitution du culture_id pour le synthétisé
    left = df_noeuds_synthetise
    right = df_noeuds_synthetise_restructure
    df_noeuds_synthetise_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # informations assolée
    left = df_noeuds_synthetise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_noeuds_synthetise_extanded = pd.merge(left, right, left_on='culture_id', right_on='culture_id', how='left')

    left = df_connection_synthetise_extanded_prim.reset_index()
    right = df_noeuds_synthetise_extanded.rename(columns={'id' : 'noeuds_synthetise_id'})
    df_connection_synthetise_extanded = pd.merge(
        left, right, left_on='cible_noeuds_synthetise_id', right_on='noeuds_synthetise_id', how='left'
    ).set_index(
        ['id', 'composant_culture_id']
    )

    left = df_plantation_perenne_synthetise
    right = df_plantation_perenne_synthetise_restructure
    df_plantation_perenne_synthetise_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # informations perennes
    left = df_plantation_perenne_synthetise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_plantation_perenne_synthetise_extanded = pd.merge(
        left, right, left_on='culture_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    left = df_plantation_perenne_phases_synthetise.reset_index()
    right = df_plantation_perenne_synthetise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_synthetise_id'})
    df_plantation_perenne_phases_synthetise_extanded = pd.merge(
        left, right, on='plantation_perenne_synthetise_id', how='left'
    ).set_index('id')


    # on ajoute l'information de la connection où porte l'intervention
    left = df_composant_culture_concerne_intervention_synthetise
    right = df_composant_culture_concerne_intervention_synthetise_restructure
    df_composant_culture_intervention_synthetise_restructure = pd.merge(
        left, right, left_index=True, right_index=True, how='left'
    )

    left = df_composant_culture_intervention_synthetise_restructure
    right = df_intervention_synthetise[['connection_synthetise_id', 'plantation_perenne_phases_synthetise_id','concerne_ci']]
    df_composant_culture_concerne_intervention_extanded = pd.merge(
        left, right, left_on='intervention_synthetise_id', right_index=True, how='left')

    # pour les cultures intermédiaires, on est obligé de faire un traitement spécifique : 
    left = df_connection_synthetise_extanded_prim.reset_index()
    right = df_composant_culture_extanded[['culture_id', 'esp_complet_var']].reset_index().rename(columns={'id': 'composant_culture_id'})
    df_connection_synthetise_extanded_ci = pd.merge(
        left, right, left_on='culture_intermediaire_id', right_on='culture_id', how='inner'
    ).set_index(['id', 'composant_culture_id'])

    
    # maintenant qu'on a tout, pour l'assolée :
    left = df_composant_culture_concerne_intervention_extanded
    right = df_connection_synthetise_extanded
    df_composant_culture_concerne_intervention_extanded_assolee = pd.merge(left, right, 
        left_on=['connection_synthetise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    left = df_composant_culture_concerne_intervention_extanded
    right = df_connection_synthetise_extanded_ci
    df_composant_culture_concerne_intervention_extanded_assolee_ci = pd.merge(left, right, 
        left_on=['connection_synthetise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    df_composant_culture_concerne_intervention_extanded_assolee = pd.concat([
        df_composant_culture_concerne_intervention_extanded_assolee,
        df_composant_culture_concerne_intervention_extanded_assolee_ci
    ])

    # pour le perenne :
    left = df_composant_culture_concerne_intervention_extanded.reset_index()
    right = df_plantation_perenne_phases_synthetise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_phases_synthetise_id'})
    df_composant_culture_concerne_intervention_extanded_perenne = pd.merge(left, right,
        on=['plantation_perenne_phases_synthetise_id', 'composant_culture_id'],
        how='inner'
    )

    df_composant_culture_concerne_intervention_extanded_perenne = df_composant_culture_concerne_intervention_extanded_perenne.fillna('')
    df_composant_culture_concerne_intervention_extanded_assolee = df_composant_culture_concerne_intervention_extanded_assolee.fillna('')

    df_final_perenne = df_composant_culture_concerne_intervention_extanded_perenne.groupby([
        'intervention_synthetise_id'
    ]).agg({
        'esp_complet_var' : ' ; '.join, 
        'esp_complet' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'esp': lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'var' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'culture_id' : lambda x: next(iter(x)),
    })

    df_final_assolee = df_composant_culture_concerne_intervention_extanded_assolee.groupby([
        'intervention_synthetise_id'
    ]).agg({
        'esp_complet_var' : ' ; '.join,
        'esp_complet' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'esp': lambda x: ' ; '.join(dict.fromkeys([item for item in x if item.strip()])),
        'var' : lambda x: '; '.join(dict.fromkeys([item for item in x if item.strip()])),
        'culture_id' : lambda x: next(iter(x)),
        'concerne_ci' : lambda x: next(iter(x)),
        'culture_intermediaire_id': lambda x: next(iter(x))
    })
    df_final_assolee['culture_id'] = np.where(df_final_assolee['concerne_ci'] == 't', df_final_assolee['culture_intermediaire_id'], df_final_assolee['culture_id'])
    df_final_assolee = df_final_assolee.drop(['concerne_ci'], axis = 1)
    df_final_assolee = df_final_assolee.drop(['culture_intermediaire_id'], axis = 1)


    df_intervention_synthetise_v1 = pd.concat([df_final_assolee, df_final_perenne])

    # On merge le nom de la culture ('nom') par la 'culture_id'
    left = df_intervention_synthetise_v1.reset_index()
    right = df_culture.reset_index().rename(columns={'id' : 'culture_id', 'nom' : 'culture_nom'})
    right = right[['culture_id','culture_nom']]
    df_intervention_synthetise_v2 = pd.merge(left, right,
        on='culture_id',
        how='left'
    )
    df_intervention_synthetise_final = df_intervention_synthetise_v2

    return df_intervention_synthetise_final.reset_index().rename(
        columns={'intervention_synthetise_id' : 'id'}
    )

def get_intervention_synthetise_culture_prec_outils_can(
        donnees
):
    """
    Permet d'obtenir un DataFrame contenant les informations sur les cultures précédentes
    associées aux interventions synthétisées, dans un format conforme à la CAN.

    Cette fonction extrait et associe les informations des cultures précédentes
    (nom, espèces, identifiant) liées aux nœuds et connexions des interventions.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'intervention_synthetise' : Interventions synthétisées.
            - 'noeuds_synthetise' : Détails sur les nœuds synthétisés.
            - 'connection_synthetise' : Informations sur les connexions entre les nœuds.
            - 'culture' : Informations générales sur les cultures.
            - 'noeuds_synthetise_restructure' : Dataframe de restructuration des nœuds synthétisés.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations des cultures précédentes par intervention synthétisée :
            - `id` : Identifiant de l'intervention synthétisée.
            - `precedent_code` : Code de la culture précédente.
            - `precedent_nom` : Nom de la culture précédente.
            - `precedent_especes_edi` : Liste des espèces précédentes dans un format enrichi.
            - `precedent_id` : Identifiant unique de la culture précédente.

    Exemple d'utilisation :
        donnees = {
            'intervention_synthetise': pd.DataFrame(...),
            'noeuds_synthetise': pd.DataFrame(...),
            'connection_synthetise': pd.DataFrame(...),
            ...
        }
        result = get_intervention_synthetise_culture_prec_outils_can(donnees)
    """
    df_intervention_synthetise = donnees['intervention_synthetise'].set_index('id')
    df_noeuds_synthetise = donnees['noeuds_synthetise'].set_index('id')
    df_connection_synthetise = donnees['connection_synthetise'].set_index('id')
    df_culture = donnees['culture'].set_index('id')
    df_noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure'].set_index('id')

    # Obtention des informations sur le composant culture, dans le format attendu par la CAN
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees)

    df_culture_grouped = df_composant_culture_extanded.groupby('culture_id').agg({
        'esp_complet' : ' ; '.join
    })

    # ajout des infos sur la culture
    left = df_culture
    right = df_culture_grouped
    df_culture_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # ajout du composant_culture_id pour ne pas avoir à travailler avec le composant_culture_code
    left = df_noeuds_synthetise
    right = df_noeuds_synthetise_restructure
    df_noeuds_synthetise = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # ajout des informations de la culture au noeud
    left = df_noeuds_synthetise
    right = df_culture_extanded[['nom', 'esp_complet']]
    df_noeuds_synthetise_extanded = pd.merge(
        left, right, left_on='culture_id', right_index=True, how='left'
    )

    # ajout des informations du noeud précédent à la connexion
    left = df_connection_synthetise
    right = df_noeuds_synthetise_extanded.rename(
        columns={
            'culture_code' : 'precedent_code', 
            'esp_complet' : 'precedent_especes_edi', 
            'nom': 'precedent_nom',
            'culture_id' : 'precedent_id'
        }
    )
    df_connection_synthetise_extanded = pd.merge(
        left, right, left_on='source_noeuds_synthetise_id', right_index=True, how='left'
    )

    # ajout des informations de la connexion sur laquelle porte l'intervention
    left = df_intervention_synthetise.reset_index()
    right = df_connection_synthetise_extanded
    df_intervention_synthetise_extanded = pd.merge(
        left, right, left_on='connection_synthetise_id', right_index=True, how='inner'
    ).set_index('id')

    final = df_intervention_synthetise_extanded[
        ['precedent_code', 'precedent_nom', 'precedent_especes_edi', 'precedent_id']
    ]
    return final.reset_index()

def get_intervention_synthetise_action_outils_can(
        donnees
):
    """
    Permet d'obtenir un DataFrame contenant des informations détaillées sur les actions
    associées aux interventions synthétisées, adaptées au format attendu par la CAN.

    Cette fonction intègre différentes catégories d'actions (application de produits phytosanitaires,
    lutte biologique, irrigation, et autres) et calcule des indicateurs spécifiques
    en fonction du type d'action.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'action_synthetise' : Détails sur les actions synthétisées.
            - 'intervention_synthetise' : Informations sur les interventions synthétisées.

    Returns:
        pd.DataFrame:
            Un DataFrame avec les colonnes suivantes :
            - `id` : Identifiant de l'intervention synthétisée.
            - `interventions_actions` : Liste des types d'actions sous forme de chaîne.
            - `interventions_actions_details` : Description détaillée des actions (concatenée).
            - `proportion_surface_traitee_phyto` : Proportion de surface traitée pour les produits phytosanitaires.
            - `proportion_surface_traitee_lutte_bio` : Proportion de surface traitée pour la lutte biologique.
            - `psci_phyto` : Indicateur PSCI pour les produits phytosanitaires.
            - `psci_lutte_bio` : Indicateur PSCI pour la lutte biologique.
            - `quantite_eau_mm` : Quantité d'eau utilisée pour l'irrigation, en mm.

    Exemple d'utilisation :
        donnees = {
            'action_synthetise': pd.DataFrame(...),
            'intervention_synthetise': pd.DataFrame(...)
        }
        result = get_intervention_synthetise_action_outils_can(donnees)
    """
    
    df_action_synthetise = donnees['action_synthetise']
    df_intervention_synthetise = donnees['intervention_synthetise']

    # on rajoute aux actions des informations sur l'intervention
    left =  df_action_synthetise
    right = df_intervention_synthetise[['id', 'freq_spatiale', 'freq_temporelle', 'psci_intervention']].rename(columns={'id' : 'intervention_synthetise_id'})
    df_action_synthetise_extanded = pd.merge(left, right, on='intervention_synthetise_id', how='left')


    # On rajoute l'information des types actions tel qu'attendus
    df_type_action = pd.DataFrame.from_records([TYPE_ACTION]).melt().rename(
        columns={'variable' : 'action_agrosyst', 'value' : 'action_str'}
    )

    left = df_action_synthetise_extanded
    right = df_type_action
    df_action_synthetise_extanded = pd.merge(left, right, left_on='type', right_on='action_agrosyst', how='left')

    # On recalcul à présent le psci adapté en fonction du type d'action 

    # Pour les applications de produits phytosanitaires :
    df_action_produit_phyto = df_action_synthetise_extanded.loc[df_action_synthetise_extanded['type'] == 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES'].copy()
    df_action_produit_phyto.loc[: , 'proportion_surface_traitee_phyto'] = df_action_produit_phyto['proportion_surface_traitee']
    df_action_produit_phyto.loc[: ,'psci_phyto'] = df_action_produit_phyto['proportion_surface_traitee'] * \
          df_action_produit_phyto['freq_spatiale'] * df_action_produit_phyto['freq_temporelle']

    # Pour la lutte biologique :
    df_action_lutte_bio = df_action_synthetise_extanded.loc[df_action_synthetise_extanded['type'] == 'LUTTE_BIOLOGIQUE'].copy()
    df_action_lutte_bio.loc[: ,'proportion_surface_traitee_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee']
    df_action_lutte_bio.loc[: ,'psci_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee'] * \
          df_action_lutte_bio['freq_spatiale'] * df_action_lutte_bio['freq_temporelle']

    # Pour l'irrigation :
    df_action_irrigation = df_action_synthetise_extanded.loc[df_action_synthetise_extanded['type'] == 'IRRIGATION'].copy()
    df_action_irrigation.loc[: ,'quantite_eau_mm'] = df_action_irrigation['eau_qte_moy_mm'] 

    # Pour les autres :
    df_action_autres = df_action_synthetise_extanded.loc[
        (df_action_synthetise_extanded['type'] != 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES') &
        (df_action_synthetise_extanded['type'] != 'LUTTE_BIOLOGIQUE') &
        (df_action_synthetise_extanded['type'] != 'IRRIGATION')
    ].copy().groupby(['intervention_synthetise_id']).agg({
        'label' : ' ; '.join
    }).reset_index()
    
    keeped_column_produit_phyto = ['proportion_surface_traitee_phyto', 'psci_phyto']
    keeped_column_lutte_bio = ['proportion_surface_traitee_lutte_bio', 'psci_lutte_bio']
    keeped_column_irrigation = ['quantite_eau_mm']
    merge = pd.merge(df_action_produit_phyto[keeped_column_produit_phyto+['intervention_synthetise_id', 'label']],
                    df_action_lutte_bio[keeped_column_lutte_bio+['intervention_synthetise_id', 'label']],
                    on='intervention_synthetise_id', how='outer', suffixes = ('', '_lutte_bio'))

    merge = pd.merge(merge.set_index('intervention_synthetise_id'),
                     df_action_autres[['intervention_synthetise_id', 'label']],
                     left_index=True, suffixes = ('', '_autre'),
                     right_on='intervention_synthetise_id', how='outer').drop_duplicates(subset=['intervention_synthetise_id'])
    
    merge = pd.merge(merge.set_index('intervention_synthetise_id'), 
                     df_action_irrigation[keeped_column_irrigation+['intervention_synthetise_id', 'label']],
                     left_index=True, suffixes = ('', '_irrigation'),
                     right_on='intervention_synthetise_id', how='outer').drop_duplicates(subset=['intervention_synthetise_id'])
    
    merge = merge.set_index('intervention_synthetise_id')

    # pour constituer la chaîne finale, on utilise une méthode vectorisée.
    merge.loc[: , 'interventions_actions_details'] = merge[['label', 'label_lutte_bio', 'label_autre', 'label_irrigation']] \
    .fillna('') \
    .agg(' ; '.join, axis=1) \
    .str.replace(r'( ; )+', ' ; ', regex=True) \
    .str.strip(' ;')

    # on groupe les actions par intervention
    df_intervention_synthetise_extanded = df_action_synthetise_extanded[['action_str', 'intervention_synthetise_id']].rename(columns={
        'action_str' : 'interventions_actions'
    }).groupby('intervention_synthetise_id').agg({
        'interventions_actions' :  lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])), 
    })

    # on rajoute à ce dataframe l'information du type d'intervention
    left = merge.reset_index()
    right = df_intervention_synthetise_extanded
    merge = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True, how='left')

    # À ce stade, on a encore des dupplication d'intervention_id : on doit grouper par intervention_id en joignant le nom des actions, mais en gardant
    # à chaque fois la valeur non nulle pour les colonnes
    intervention_actions_indicateurs = merge[[
         'intervention_synthetise_id', 'interventions_actions', 'interventions_actions_details', 'proportion_surface_traitee_phyto', 'psci_phyto', 
        'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm'
    ]].rename(columns={'intervention_synthetise_id' : 'id'})

    return intervention_actions_indicateurs

def get_intervention_synthetise_semence_outils_can(
        donnees
    ):
    """
    Permet d'obtenir un DataFrame contenant des informations détaillées sur les interventions
    de type "SEMIS" dans le format attendu par la CAN.

    La fonction récupère et enrichit les données des semences utilisées dans les interventions
    synthétisées, incluant les espèces semées, les densités de semis, et les traitements associés.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'semence' : Informations sur les semences utilisées.
            - 'composant_culture' : Détails des composants de culture (espèces, variétés, etc.).
            - 'espece' : Informations sur les espèces botaniques.
            - 'utilisation_intrant_synthetise' : Utilisation des intrants (incluant les semences).

    Returns:
        pd.DataFrame:
            Un DataFrame avec les colonnes suivantes :
            - `id` : Identifiant de l'intervention synthétisée.
            - `especes_semees` : Description des espèces semées (nom botanique et autres attributs) (concaténée)
            - `densite_semis` : Densité de semis utilisée (concaténée).
            - `unite_semis` : Unité de mesure pour la densité de semis (concaténée).
            - `traitement_chimique_semis` : Indique si un traitement chimique a été appliqué (concaténé).
            - `inoculation_biologique_semis` : Indique si une inoculation biologique a été réalisée (concaténée).

    Exemple d'utilisation :
        donnees = {
            'semence': pd.DataFrame(...),
            'composant_culture': pd.DataFrame(...),
            'espece': pd.DataFrame(...),
            'utilisation_intrant_synthetise': pd.DataFrame(...)
        }
        result = get_intervention_synthetise_semence_outils_can(donnees)
    """
    df_semence = donnees['semence']
    df_composant_culture = donnees['composant_culture']
    df_espece = donnees['espece']
    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise'].loc[~donnees['utilisation_intrant_synthetise']['semence_id'].isna()]

    # OBTENTION DES INFORMATIONS POUR LES INTERVENTIONS DE TYPE SEMENCES.
    left = df_semence.rename(columns={'espece_id':'composant_culture_id'}) # attention, on est obligé de corriger car il y a une erreur dans le nom de la colonne sur Datagrosyst.
    right = df_composant_culture[['id', 'espece_id', 'variete_id']].rename(columns={'id' : 'composant_culture_id'})
    df_semence_extanded = pd.merge(left, right, on='composant_culture_id', how='left')

    left = df_semence_extanded
    right = df_espece[['id', 'libelle_espece_botanique', 'libelle_qualifiant_aee', 'libelle_type_saisonnier_aee', 'libelle_destination_aee']].rename(columns={'id' : 'espece_id'})
    df_semence_extanded = pd.merge(left, right, on='espece_id', how='left')

    df_semence_extanded = df_semence_extanded.fillna('')

    df_semence_extanded['description'] = df_semence_extanded[[
        'libelle_espece_botanique', 'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 'libelle_destination_aee', 
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    # ajout des informations des semences sur les utilisations d'intrants
    left = df_utilisation_intrant_synthetise[['intervention_synthetise_id', 'intrant_id', 'dose', 'unite', 'semence_id']]
    right = df_semence_extanded.rename(columns={'id' : 'semence_id'})
    df_utilisation_intrant_synthetise_extanded = pd.merge(left, right, on='semence_id', how='inner')

    df_utilisation_intrant_synthetise_extanded['dose'] = df_utilisation_intrant_synthetise_extanded['dose'].astype('str')

    # on groupe par intervention
    df_intervention_semence = df_utilisation_intrant_synthetise_extanded.fillna('').groupby([
        'intervention_synthetise_id'
    ]).agg({
        'description' :  ' ; '.join,
        'type_semence' :  ', '.join,
        'dose' : ', '.join,
        'unite' : ', '.join, 
        'inoculation_biologique' : lambda x: map_boolean(x, sep=', '),
        'traitement_chimique' : lambda x: map_boolean(x, sep=', ')
    })

    df_intervention_semence['dose'] = df_intervention_semence[['dose']].map(convert_to_int)

    return df_intervention_semence.reset_index().rename(columns={
        'intervention_synthetise_id' : 'id',
        'description' : 'especes_semees', 
        'dose' : 'densite_semis', 
        'unite' : 'unite_semis', 
        'traitement_chimique' : 'traitement_chimique_semis',
        'inoculation_biologique' : 'inoculation_biologique_semis'
    })

def get_intervention_synthetise_outils_can_context(
    donnees
):
    """
    Permet d'obtenir un DataFrame intermédiaire contenant les informations
    des interventions dans le format attendu par la CAN

    La fonction combine plusieurs sources de données pour synthétiser :
    - Les actions associées aux interventions.
    - Les informations sur les semences utilisées.
    - Les indicateurs spécifiques liés à différents types d'actions et de traitements.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'intervention_synthetise' : Données de base sur les interventions synthétisées.
            - Les autres tables utilisées dans `get_intervention_synthetise_action_outils_can`
              et `get_intervention_synthetise_semence_outils_can`.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les colonnes consolidées suivantes :
            - `id` : Identifiant unique de l'intervention synthétisée.
            - `interventions_actions` : Liste des actions associées à l'intervention.
            - `especes_semees` : Description des espèces semées.
            - `densite_semis` : Densité des semis.
            - `unite_semis` : Unité de mesure pour la densité de semis.
            - `traitement_chimique_semis` : Indique si un traitement chimique a été appliqué.
            - `inoculation_biologique_semis` : Indique si une inoculation biologique a été réalisée.
            - `type_semence` : Type de semences utilisées.
            - `proportion_surface_traitee_phyto` : Proportion de surface traitée par produits phytosanitaires.
            - `psci_phyto` : Indicateur de pression spécifique pour les phytosanitaires.
            - `proportion_surface_traitee_lutte_bio` : Proportion de surface traitée en lutte biologique.
            - `psci_lutte_bio` : Indicateur de pression spécifique pour la lutte biologique.
            - `quantite_eau_mm` : Quantité d’eau utilisée pour l’irrigation (en millimètres).

    Exemple d'utilisation :
        donnees = {
            'intervention_synthetise': pd.DataFrame(...),
            ...
        }
        result = get_intervention_synthetise_outils_can_context(donnees)
    """
    df_intervention_synthetise = donnees['intervention_synthetise']

    # ajout des informations sur les différents indicateurs
    left = df_intervention_synthetise
    right = get_intervention_synthetise_action_outils_can(donnees)
    merge = pd.merge(left, right, on='id', how='left')
    
    # ajout des informations sur la table semis
    left = merge
    right = get_intervention_synthetise_semence_outils_can(donnees).reset_index()
    merge = pd.merge(left, right, on='id', how='left')



    columns = ['id', 'interventions_actions', 'especes_semees', 'densite_semis', 'unite_semis', 'traitement_chimique_semis', 
               'inoculation_biologique_semis', 'type_semence', 'proportion_surface_traitee_phyto', 'psci_phyto', 
               'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    # ajout des informations sur les espèces concernées
    return merge[columns]

def get_intervention_synthetise_combinaison_outils_can(
    donnees
):
    """
    Permet d'obtenir un DataFrame contenant des informations détaillées sur les combinaisons d'outils
    utilisées dans les interventions, avec les caractéristiques associées aux matériels et aux tracteurs.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'intervention_synthetise' : Données de base sur les interventions synthétisées.
            - 'combinaison_outil' : Détails des combinaisons d'outils.
            - 'materiel' : Informations sur les matériels associés aux outils.
            - 'combinaison_outil_materiel' : Lien entre les combinaisons d'outils et les matériels.
            - 'intervention_synthetise_restructure' : Dataframe restructuré des interventions synthétisé (pour éviter 
            d'avoir à travailler avec des codes)

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations consolidées suivantes pour chaque intervention :
            - `combinaison_outils_nom` : Nom de la combinaison d'outils.
            - `tracteur_ou_automoteur` : Information sur le tracteur ou automoteur associé.
            - `outils` : Liste des outils associés à la combinaison d'outils, séparés par `;`.

    Exemple d'utilisation :
        donnees = {
            'intervention_synthetise': pd.DataFrame(...),
            'combinaison_outil': pd.DataFrame(...),
            'materiel': pd.DataFrame(...),
            'combinaison_outil_materiel': pd.DataFrame(...),
            'intervention_synthetise_restructure': pd.DataFrame(...)
        }
        result = get_intervention_synthetise_combinaison_outils_can(donnees)
    """
    df_intervention_synthetise = donnees['intervention_synthetise'].set_index('id')
    df_combinaison_outil = donnees['combinaison_outil'].set_index('id')
    df_materiel = donnees['materiel'].set_index('id')
    df_combinaison_outil_materiel = donnees['combinaison_outil_materiel']
    df_intervention_synthetise_restructure = donnees['intervention_synthetise_restructure'].set_index('id')

    # Ajout du combinaison_outil_id pour ne pas avoir à travailler avec combinaison_outil_code
    left = df_intervention_synthetise
    right = df_intervention_synthetise_restructure
    df_intervention_synthetise_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # Ajout des informations sur le tracteur à la combinaison d'outils 
    left = df_combinaison_outil[['nom', 'tracteur_materiel_id']]
    right = df_materiel[['nom', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'nom_tracteur', 'materiel_caracteristique1' : 'tracteur_ou_automoteur'}
    )
    df_combinaison_outil_extanded = pd.merge(left, right, left_on='tracteur_materiel_id', right_index=True, how='left')

    # Ajout des informations sur le materiel à la combinaison d'outils
    left = df_combinaison_outil_materiel
    right = df_materiel[['nom', 'type_materiel', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'combinaison_outils_nom', 'materiel_caracteristique1' : 'outils'}
    )
    df_combinaison_outil_materiel= pd.merge(left, right, left_on='materiel_id', right_index=True, how='left')

    # On considère que si plusieurs matériels ont les mêmes caractéristiques (outils)
    # Alors il n'y a pas besoin de remonter plusieurs fois l'information dans l'agrégation 
    # (Correction par rapport aux exports en masse historiques)
    df_combinaison_outil_materiel = df_combinaison_outil_materiel.drop_duplicates(
        subset=['combinaison_outil_id', 'outils']
    )

    # On rassemble tous les materiels pour n'avoir qu'une description par combinaison d'outils
    df_combinaison_outil_materiel['outils'] = df_combinaison_outil_materiel['outils'].fillna('')
    df_combinaison_outil_materiel_grouped = df_combinaison_outil_materiel.groupby('combinaison_outil_id').agg({
        'outils' : ' ; '.join, # delete NaN
    })

    # On mets toutes les informations dans le même dataframe
    left = df_combinaison_outil_extanded
    right = df_combinaison_outil_materiel_grouped
    df_combinaison_outil_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # On agrège les informations au dataframe des interventions
    left = df_intervention_synthetise_extanded[['combinaison_outil_id']]
    right = df_combinaison_outil_extanded.rename(columns={'nom' : 'combinaison_outils_nom'})[
        ['combinaison_outils_nom', 'tracteur_ou_automoteur', 'outils']
    ]

    merge = pd.merge(left, right, left_on='combinaison_outil_id', right_index=True, how='left')

    return merge.reset_index()

def get_intervention_synthetise_outils_can(
    donnees
):
    """
    Permet d'obtenir le DataFrame final des interventions synthétisées pour la CAN.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'intervention_synthetise' : Données de base sur les interventions synthétisées.
            - Les autres tables utilisées dans `get_intervention_synthetise_outils_can_context`,
            `get_intervention_synthetise_combinaison_outils_can`, `get_intervention_synthetise_culture_outils_ca`
            `get_intervention_synthetise_culture_prec_outils_can`, `get_intervention_synthetise_cibles_outils_ca`, 
            `get_intervention_synthetise_rendement_outils_can`, `get_intervention_synthetise_nb_intrant_outils_can`

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations consolidées suivantes pour chaque intervention :
            - `intervention_synthetise_id` : Identifiant unique de l'intervention.
            - `interventions_actions` : Description des actions effectuées lors de l'intervention.
            - `especes_semees` : Liste des espèces semées dans le cadre de l'intervention.
            - `densite_semis` : Densité des semis (quantité de semences par unité de surface).
            - `unite_semis` : Unité de mesure de la densité des semis.
            - `traitement_chimique_semis` : Indicateur de l'utilisation d'un traitement chimique pour les semis (oui/non).
            - `inoculation_biologique_semis` : Indicateur de l'utilisation d'inoculation biologique pour les semis (oui/non).
            - `type_semence` : Type de semence utilisée pour l'intervention.
            - `proportion_surface_traitee_phyto` : Proportion de la surface traitée avec des produits phytosanitaires.
            - `proportion_surface_traitee_lutte_bio` : Proportion de la surface traitée avec des méthodes de lutte biologique.
            - `psci_phyto` : Indicateur PSCI phyto.
            - `psci_lutte_bio` : Indicateur PSCI lutte biologique.
            - `quantite_eau_mm` : Quantité d'eau utilisée pour l'intervention (en millimètres).
            - `combinaison_outils_nom` : Nom de la combinaison d'outils utilisés pour l'intervention.
            - `tracteur_ou_automoteur` : Information sur le tracteur ou l'automoteur associé à la combinaison d'outils.
            - `outils` : Liste des outils utilisés dans la combinaison d'outils.

    Exemple d'utilisation :
        donnees = {
            'intervention_synthetise': pd.DataFrame(...),
            'combinaison_outil': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'intrants': pd.DataFrame(...),
            # autres DataFrames requis
        }
        result = get_intervention_synthetise_outils_can(donnees)
    """

    # ajout des informations de contexte sur l'intervention
    left = get_intervention_synthetise_outils_can_context(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    right = get_intervention_synthetise_combinaison_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur la culture concernée par l'intervention
    left = merge
    right = get_intervention_synthetise_culture_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur la culture précédente
    left = merge
    right = get_intervention_synthetise_culture_prec_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur les intrants utilisés dans l'intervention :
    left = merge
    right = get_intervention_synthetise_intrants_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur les interventions cible : 
    left = merge
    right = get_intervention_synthetise_cibles_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur les rendements :
    left = merge 
    right = get_intervention_synthetise_rendement_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur le nombre d'intrants dans l'intervention
    left = merge
    right = get_intervention_synthetise_nb_intrant_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')
    merge.loc[:, 'nb_intrants'] = merge['nb_intrants'].fillna(0)
    
    return merge.rename(columns={'intervention_synthetise_id': 'id'})

def get_intervention_synthetise_intrants_outils_can(
        donnees
):
    """
    Permet d'obtenir pour chaque intervention synthétisée, la liste des intrants utilisés dans l'intervention, 
    dans le format attendu par la CAN.

    Cette fonction regroupe les informations sur les intrants appliqués lors de chaque intervention et les formate en indiquant notamment 
    les produits chimiques et leurs doses, les types d'intrants 
    (autre, semis, etc.), et les méthodes de biocontrôle utilisées.

    Par exemple, pour l'intervention `fr.inra.agrosyst.api.entities.practiced.PracticedIntervention_fb063bae-d233-40a5-97ff-e31f19d1efc1`, 
    la sortie doit être : 
    "CUPROXAT SC (0.5 L/ha), CUIVROL (0.5 kg/ha), HELIOSOUFRE S (4.0 L/ha), LAMINAFLOR (2.0 l/ha)".

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'utilisation_intrant_synthetise' : Données relatives à l'utilisation des intrants par intervention.
            - 'intrant' : Informations sur les intrants utilisés (par exemple, type et nom des intrants).
        variable(s) globale(s) :
            'UNITE_APPLICATION' : Information sur les unités d'application des intrants.
    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations suivantes pour chaque intervention :
            - `intervention_synthetise_id` : Identifiant unique de l'intervention.
            - `interventions_intrants` : Liste des intrants utilisés dans l'intervention sous le format attendu par la CAN.
            - `biocontrole` : Indicateur de l'utilisation de biocontrole (valeurs 'oui' ou 'non').

    Exemple d'utilisation :
        donnees = {
            'utilisation_intrant_synthetise': pd.DataFrame(...),
            'intrant': pd.DataFrame(...),
        }
        UNITE_APPLICATION = {'AA_HA': 'Aa/ha', ...}

        result = get_intervention_synthetise_intrants_outils_can(donnees)
    """
    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise'].set_index('id')
    df_intrant = donnees['intrant'].set_index('id')

    df_unite_application = pd.DataFrame.from_records([UNITE_APPLICATION]).melt().rename(
        columns={'variable' : 'unite_agrosyst', 'value' : 'unite_utilisateur'}
    )

    left = df_utilisation_intrant_synthetise
    right = df_intrant
    merge = pd.merge(left, right, left_on='intrant_id', right_index=True, how='left')

    # ON TRAITE DIFFÉREMENT SI IL S'AGIT D'UN INTRANT AUTRE OU NON (CAS != INTRANT AUTRE )
    left = merge.loc[(merge['type'] != 'AUTRE') & (merge['type'] != 'SEMIS')]
    right = df_unite_application
    merge_application = pd.merge(left, right, left_on='unite', right_on='unite_agrosyst', how='left')

    # utiliser le ref_nom ou le nom utilisateur ? --> il semble que ce soit le nom_utilisateur
    merge_application.loc[:, 'interventions_intrants'] = (merge_application['nom_utilisateur']) + ' ('+merge_application['dose'].astype('str')+ ' '+merge_application['unite_utilisateur']+')'
    merge_application['interventions_intrants'] = merge_application['interventions_intrants'].fillna('')

    # INTRANT AUTRE
    merge_autre = merge.loc[(merge['type'] == 'AUTRE')].copy()
    merge_autre.loc[:, 'interventions_intrants'] = (merge_autre['type']) + ' - ' + (merge_autre['nom_utilisateur'])
    merge_autre['interventions_intrants'] = merge_autre['interventions_intrants'].fillna('')

    # INTRANT SEMIS
    merge_semis = merge.loc[(merge['type'] == 'SEMIS')].copy()
    merge_semis.loc[:, 'interventions_intrants'] = (merge_semis['nom_utilisateur'])
    merge_semis['interventions_intrants'] = merge_semis['interventions_intrants'].fillna('')

 
    merge = pd.concat([df for df in (merge_application, merge_autre, merge_semis) if not df.empty])
    merge['biocontrole'] = merge['biocontrole'].fillna('f').replace({'t': True, 'f': False})

    res = merge[['interventions_intrants', 'intervention_synthetise_id', 'biocontrole']].groupby('intervention_synthetise_id').agg({
        'interventions_intrants' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'biocontrole' : 'max'
    })

    res['biocontrole'] = res['biocontrole'].replace({False: 'non', True : 'oui'})

    return res.reset_index().rename(columns={'intervention_synthetise_id' : 'id'})

def get_intervention_synthetise_cibles_outils_can(
        donnees
):
    """
    Permet d'obtenir pour chaque intervention synthétisée, la liste des cibles concernées par l'intervention, 
    dans le format attendu par la CAN.

    Cette fonction identifie les cibles (adventices ou nuisibles) qui sont concernées par l'intervention 
    et les formate en indiquant notamment les groupes cibles associés.

    Par exemple, pour l'intervention `fr.inra.agrosyst.api.entities.practiced.PracticedIntervention_fb063bae-d233-40a5-97ff-e31f19d1efc1`, 
    la sortie pourrait être : 
    `"Mildiou, Oïdium"`.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'utilisation_intrant_synthetise' : Données relatives à l'utilisation des intrants par intervention.
            - 'utilisation_intrant_cible' : Informations sur les cibles associées aux intrants utilisés.
            - 'nuisible_edi' : Nuisibles.
            - 'adventice' : Adventices.
            - 'groupe_cible' : Groupes cibles des interventions (pour les cibles spécifiques).

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations suivantes pour chaque intervention :
            - `id` : Identifiant unique de l'intervention.
            - `interventions_cibles_trait` : Liste des cibles concernées par l'intervention sous le format attendu par la CAN.
            - `interventions_groupe_cible` : Liste des groupes cibles associés à l'intervention.

    Exemple d'utilisation :
        donnees = {
            'utilisation_intrant_synthetise': pd.DataFrame(...),
            'utilisation_intrant_cible': pd.DataFrame(...),
            'nuisible_edi': pd.DataFrame(...),
            'adventice': pd.DataFrame(...),
            'groupe_cible': pd.DataFrame(...),
        }
        result = get_intervention_synthetise_cibles_outils_can(donnees)
    """

    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise'].set_index('id')
    df_utilisation_intrant_cible = donnees['utilisation_intrant_cible'].set_index('id')
    df_nuisible_edi = donnees['nuisible_edi'].set_index('id')
    df_adventice = donnees['adventice'].set_index('id')
    df_groupe_cible = donnees['groupe_cible'].set_index('id')

    # correction des mauvaises interprétations de colonnes
    df_nuisible_edi['reference_id'] = df_nuisible_edi['reference_id'].astype('str')
    df_groupe_cible['cible_edi_ref_id'] = df_groupe_cible['cible_edi_ref_id'].astype('str')


    # on associe à chaque cible d'utilisation d'intrants les informations sur la cible (adventices ou nuisibles)
    left = df_utilisation_intrant_cible
    df_nuisible_edi = df_nuisible_edi[['label_nuisible', 'reference_id']].rename(columns={'label_nuisible' : 'label'})
    right = pd.concat([df_nuisible_edi, df_adventice])
    merge = pd.merge(left, right, left_on='ref_cible_id', right_index=True, how='left')[[
        'label', 'utilisation_intrant_id', 'code_groupe_cible_maa', 'reference_id'
    ]]

    # on ajoute l'information de l'intervention
    left = merge 
    right = df_utilisation_intrant_synthetise[['intervention_synthetise_id']]
    merge = pd.merge(left, right, left_on='utilisation_intrant_id', right_index=True, how='left')

    # on ajoute l'information du groupe cible
    left = merge
    right = df_groupe_cible[['groupe_cible_maa', 'cible_edi_ref_id', 'code_groupe_cible_maa']]
    merge = pd.merge(left, right, left_on=['reference_id', 'code_groupe_cible_maa'], right_on=['cible_edi_ref_id', 'code_groupe_cible_maa'], how='left')


    merge['label'] = merge['label'].fillna('')
    merge['groupe_cible_maa'] = merge['groupe_cible_maa'].fillna('')
    
    res = merge.groupby(['intervention_synthetise_id']).agg({
        'label' :  lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])), 
        'groupe_cible_maa':  lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()]))
    }).rename(columns={'label' : 'interventions_cibles_trait'})

    return res.reset_index().rename(columns={
        'intervention_synthetise_id' : 'id',
        'groupe_cible_maa' : 'interventions_groupe_cible'
    })



def get_intervention_synthetise_nb_intrant_outils_can(
        donnees
):
    """
    Permet d'obtenir pour chaque intervention synthétisée, le nombre d'utilisations d'intrants associées à l'intervention.

    Cette fonction calcule le nombre total d'intrants utilisés dans chaque intervention synthétisée en comptabilisant 
    le nombre d'occurrences des intrants dans les données d'utilisation des intrants.

    Par exemple, pour l'intervention `fr.inra.agrosyst.api.entities.practiced.PracticedIntervention_fb063bae-d233-40a5-97ff-e31f19d1efc1`, 
    la sortie doit être : 
    `4`.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'utilisation_intrant_synthetise' : Données relatives à l'utilisation des intrants par intervention.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations suivantes pour chaque intervention :
            - `id` : Identifiant unique de l'intervention.
            - `nb_intrants` : Nombre d'intrants utilisés dans l'intervention.

    Exemple d'utilisation :
        donnees = {
            'utilisation_intrant_synthetise': pd.DataFrame(...),
        }
        result = get_intervention_synthetise_nb_intrant_outils_can(donnees)
    """
    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise']

    res = df_utilisation_intrant_synthetise.groupby('intervention_synthetise_id').agg({
        'id' : 'count'
    }).rename(columns={'id' : 'nb_intrants'})

    return res.reset_index().rename(columns={'intervention_synthetise_id' : 'id'})

def get_intervention_synthetise_rendement_outils_can(
        donnees
):
    """
    Permet d'obtenir pour chaque intervention synthétisée, la liste des rendements et destinations associés à l'intervention,
    dans le format attendu par la CAN.

    Cette fonction génère une liste des rendements et de leurs destinations dans un format spécifique, par exemple :

    Par exemple, pour l'intervention `fr.inra.agrosyst.api.entities.practiced.PracticedIntervention_aadac31e-c5ff-450e-97e9-a4fc13a361ec`,
    la sortie pourrait être :
    `[Fourrage (enrubannage)]|6,000000|t MS/ha#[Fourrage (foin)]|5,000000|t MS/ha`

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'recolte_rendement_prix' : Données relatives aux rendements associés aux récoltes.
            - 'recolte_rendement_prix_restructure' : Données restructurées des rendements.
            - 'action_synthetise' : Données sur les actions liées à chaque intervention.
        variable(s) globale(s) :
            'UNITE_RENDEMENT' : Dictionnaire global contenant la correspondance entre les unités internes 
              et les unités utilisateur.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations suivantes pour chaque intervention :
            - `id` : Identifiant unique de l'intervention.
            - `rendement_total` : Liste des rendements et de leurs destinations, sous le format spécifié.

    Exemple d'utilisation :
        donnees = {
            'recolte_rendement_prix': pd.DataFrame(...),
            'recolte_rendement_prix_restructure': pd.DataFrame(...),
            'action_synthetise': pd.DataFrame(...),
        }

        UNITE_RENDEMENT = {}

        result = get_intervention_synthetise_rendement_outils_can(donnees)
    """
    recolte_rendement_prix = donnees['recolte_rendement_prix'].set_index('id')
    recolte_rendement_prix_restructure = donnees['recolte_rendement_prix_restructure'].set_index('id')
    action_synthetise = donnees['action_synthetise'].set_index('id')
    unite_rendement = pd.DataFrame.from_records([UNITE_RENDEMENT]).melt().rename(
        columns={'variable' : 'unite_agrosyst', 'value' : 'unite_utilisateur'}
    )

    left = recolte_rendement_prix
    right = recolte_rendement_prix_restructure
    recolte_rendement_prix_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = recolte_rendement_prix_extanded
    right = action_synthetise[['intervention_synthetise_id']]
    recolte_rendement_prix_extanded = pd.merge(left, right, left_on='action_id', right_index=True, how='left')

    left = recolte_rendement_prix_extanded
    right = unite_rendement
    recolte_rendement_prix_extanded = pd.merge(left, right, left_on='rendement_unite', right_on='unite_agrosyst', how='left')


    recolte_rendement_prix_extanded['rendement_total'] = '['+recolte_rendement_prix_extanded['destination'].astype('str')+']'+'|'+\
        recolte_rendement_prix_extanded['rendement_moy'].astype('str')+'|'+\
            recolte_rendement_prix_extanded['unite_utilisateur'].astype('str')

    
    res = recolte_rendement_prix_extanded.groupby('intervention_synthetise_id').agg({
        'rendement_total' : '#'.join
    })

    return res.reset_index().rename(columns={'intervention_synthetise_id' : 'id'})

# FONCTIONS POUR LES PARCELLES NON-RATTACHÉES

def get_parcelles_non_rattachees_outils_can(
    donnees
):
    """
    Permet d'obtenir des informations sur les parcelles non-rattachées et agrège toutes les informations au niveau du domaine
    auquel elles appartiennent.

    Cette fonction filtre les parcelles pour ne conserver que celles qui :
    - Contiennent des interventions réalisées.
    - Ont une surface > 0.

    Les informations agrégées incluent des données sur les réseaux, les dispositifs et les domaines associés.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'parcelle' : Données des parcelles.
            - 'reseau' : Données des réseaux associés aux dispositifs.
            - 'liaison_reseaux' : Liaison des réseaux et autres données associées.
            - 'liaison_sdc_reseau' : Affectation des systèmes de cultures à un ou plusieurs réseaux.
            - 'sdc' : Données des systèmes de cutlures.
            - 'dispositif' : Données des dispositifs.
            - 'intervention_realise_agrege' : Données des interventions réalisées.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations agrégées sur les parcelles non-rattachées, avec les colonnes suivantes :
            - `id` : Identifiant du domaine.
            - `nb_parcelles_sans_sdc` : Nombre de parcelles sans SDC rattaché.
            - `nb_parcelles_avec_id_edaplos` : Nombre de parcelles avec un identifiant Edaplos.
            - `reseaux_ir` : Liste des réseaux associés au domaine.
            - `reseaux_it` : Liste des réseaux parents associés au domaine.
            - `codes_convention_dephy` : Liste des codes de convention Dephy associés.

    Exemple d'utilisation :
        donnees = {
            'parcelle': pd.DataFrame(...),
            'reseau': pd.DataFrame(...),
            'liaison_reseaux': pd.DataFrame(...),
            'liaison_sdc_reseau': pd.DataFrame(...),
            'sdc': pd.DataFrame(...),
            'dispositif': pd.DataFrame(...),
            'intervention_realise_agrege': pd.DataFrame(...),
        }
        result = get_parcelles_non_rattachees_outils_can(donnees)
    """
    df_parcelle = donnees['parcelle'].set_index('id')
    df_reseau = donnees['reseau'].set_index('id')
    df_liaison_reseaux = donnees['liaison_reseaux']
    df_liaison_sdc_reseau = donnees['liaison_sdc_reseau']
    df_sdc = donnees['sdc'].set_index('id')
    df_dispositif = donnees['dispositif'].set_index('id')
    df_intervention_realise_agrege = donnees['intervention_realise_agrege'].set_index('id')


    # on ne garde que les parcelles non rattachées
    df_parcelles_non_rattachees = df_parcelle.loc[
        (df_parcelle['sdc_id'].isna()) &
        (df_parcelle.index.isin(df_intervention_realise_agrege['parcelle_id'])) &
        (df_parcelle['surface'] > 0)
    ]

    # pour chaque liaison de réseau, on obtient l'information complète
    left = df_liaison_sdc_reseau
    right = df_sdc[['dispositif_id']]
    merge = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    # pour chaque laison, on ajoute les informations sur le réseau
    left = merge 
    right = df_reseau[['nom', 'code_convention_dephy']]
    merge = pd.merge(left, right, left_on='reseau_id', right_index=True, how='left')

    # on obtient le domaine associé au sdc
    left = merge
    right = df_dispositif[['domaine_id']]
    merge = pd.merge(left, right, left_on='dispositif_id', right_index=True, how='left')

    # on obtient aussi le lien vers le parent du réseau
    left = merge
    right = df_liaison_reseaux
    merge = pd.merge(left, right, on='reseau_id', how='left')

    # on ajoute les informations sur le réseau parent
    left = merge
    right = df_reseau.rename(columns={'nom' : 'nom_reseau_parent', 'code_convention_dephy' : 'code_convention_dephy_reseau_parent'})
    merge = pd.merge(left, right, left_on='reseau_parent_id', right_index=True).dropna(subset=['nom', 'nom_reseau_parent']).fillna('')

    res_reseaux_domaine = merge.groupby('domaine_id').agg({
        'nom' : lambda x: '|'.join(x.unique()),
        'nom_reseau_parent' : lambda x: '|'.join(x.unique()),
        'code_convention_dephy' : lambda x: '|'.join(x.unique())
    }).rename(columns={
        'nom' : 'reseaux_ir',
        'nom_reseau_parent' : 'reseaux_it',
        'code_convention_dephy' : 'codes_convention_dephy'
    })

    df_parcelles_non_rattachees = df_parcelles_non_rattachees.reset_index().groupby('domaine_id').agg({
        'id' : 'count', 
        'edaplos_utilisateur_id' : 'count'
    }).reset_index().rename(columns={
        'id' : 'nb_parcelles_sans_sdc', 
        'edaplos_utilisateur_id':'nb_parcelles_avec_id_edaplos',
        'domaine_id' : 'id'
    }).set_index('id')

    left = df_parcelles_non_rattachees
    right = res_reseaux_domaine
    final = pd.merge(left, right, left_index=True, right_index=True, how='left')

    return final.reset_index()


# FONCTIONS POUR LES CULTURES
def get_culture_outils_can(
    donnees
):
    """
    Permet d'obtenir des informations agrégées sur les cultures, sous le format désiré par la CAN.

    Cette fonction agrège les informations concernant les espèces et les variétés des cultures. Elle inclut des informations
    détaillées sur les espèces, telles que leur nom botanique, type saisonnier, destination et d'autres caractéristiques.
    Elle fournit également un format nettoyé pour les performances et une liste des variétés associées à chaque culture.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'composant_culture' : Données des composants des cultures.
            - 'espece' : Données des espèces associées aux cultures.
            - 'variete' : Données des variétés associées aux cultures.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations agrégées sur les cultures, avec les colonnes suivantes :
            - `id` : Identifiant de la culture.
            - `complet_espece_edi` : Description complète de l'espèce (avec libellés complets, séparée par des `;`).
            - `complet_espece_edi_nettoye` : Description simplifiée de l'espèce (nom botanique uniquement, séparée par des `,`).
            - `variete_nom` : Liste des variétés associées à la culture, séparée par des `,`.

    Exemple d'utilisation :
        donnees = {
            'composant_culture': pd.DataFrame(...),
            'espece': pd.DataFrame(...),
            'variete': pd.DataFrame(...),
        }
        result = get_culture_outils_can(donnees)
    """
    df_composant_culture = donnees['composant_culture'].set_index('id')
    df_espece = donnees['espece'].set_index('id')
    df_variete = donnees['variete'].set_index('id')

    df_espece = df_espece.fillna('')

    # on a besoin d'agréger toutes les informations sur les espèces de la culture
    df_espece['complet_espece_edi'] = (
        df_espece['libelle_espece_botanique']
        +' '
        +df_espece['libelle_qualifiant_aee']
        +' '
        +df_espece['libelle_type_saisonnier_aee']
        +' '
        +df_espece['libelle_destination_aee']
    ).str.replace('\n', '<br>').str.replace('  ', ' ').str.strip().str.replace('  ', ' ')

    # on a aussi besoin, pour les performances, de l'information sans toutes les informations
    df_espece['complet_espece_edi_nettoye'] = (
        df_espece['libelle_espece_botanique']
    ).str.replace('\n', '<br>').str.replace('  ', ' ').str.strip()

    # et de l'information juste des variétés...
    df_variete['variete_nom'] = (
        df_variete['denomination']
    ).str.replace('\n', '<br>').str.replace('  ', ' ').str.strip()

    # ajout des informations utiles sur l'espèce au composant de culture
    left = df_composant_culture
    right = df_espece[['complet_espece_edi', 'complet_espece_edi_nettoye']]
    df_composant_culture_extanded = pd.merge(left, right, left_on='espece_id', right_index=True, how='left')


    # ajout des informations utiles sur la variété au composant de culture
    left = df_composant_culture_extanded
    right = df_variete[['variete_nom']]
    df_composant_culture_extanded = pd.merge(left, right, left_on='variete_id', right_index=True, how='left').fillna('')

    res = df_composant_culture_extanded.groupby('culture_id').agg({
        'complet_espece_edi' : lambda x: ' ; '.join(dict.fromkeys([item for item in x if item.strip()])),
        'complet_espece_edi_nettoye' :  lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'variete_nom' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
    })


    return res.reset_index().rename(columns={'culture_id' : 'id'})


def get_recolte_realise_outils_can(
        donnees
):
    """
    Permet d'obtenir les informations sur les récoltes en réalisé, en ajustant les rendements et en prenant en compte
    les mélanges d'espèces et de variétés. La fonction corrige les surfaces relatives des récoltes et calcule des valeurs
    agrégées par destination et unité de rendement.

    Args:
        donnees (dict): 
            Un dictionnaire contenant plusieurs DataFrames nécessaires à l'agrégation des informations sur les récoltes réalisées :
            - 'composant_culture' : Données des composants des cultures.
            - 'culture' : Données des cultures associées aux composants.
            - 'composant_culture_concerne_intervention_realise' : Données des composants concernés par les interventions réalisées.
            - 'recolte_rendement_prix' : Données des rendements des récoltes.
            - 'recolte_rendement_prix_restructure' : Données des rendements restructurés.
            - 'action_realise' : Données des actions réalisées associées aux récoltes.

    Returns:
        pd.DataFrame:
            Un DataFrame avec des informations agrégées par destination, unité de rendement et action réalisée :
            - `destination` : La destination des récoltes.
            - `rendement_unite` : L'unité de mesure du rendement.
            - `action_id` : L'identifiant de l'action réalisée.
            - `rendement_moy_corr`, `rendement_median_corr`, `rendement_max_corr`, `rendement_min_corr` : Rendements corrigés par surface relative.
            - `commercialisation_pct_corr`, `autoconsommation_pct_corr`, `nonvalorisation_pct_corr` : Pourcentages corrigés par surface relative de commercialisation, autoconsommation, et non valorisation.

    Exemple d'utilisation :
        donnees = {
            'composant_culture': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'composant_culture_concerne_intervention_realise': pd.DataFrame(...),
            'recolte_rendement_prix': pd.DataFrame(...),
            'recolte_rendement_prix_restructure': pd.DataFrame(...),
            'action_realise': pd.DataFrame(...),
        }
        result = get_recolte_realise_outils_can(donnees)
    """
    df = donnees.copy()
    df['composant_culture'] = df['composant_culture'].set_index('id')
    df['culture'] = df['culture'].set_index('id')
    df['composant_culture_concerne_intervention_realise'] = df['composant_culture_concerne_intervention_realise'].set_index('id')
    df['recolte_rendement_prix'] = df['recolte_rendement_prix'].set_index('id')
    df['recolte_rendement_prix_restructure'] = df['recolte_rendement_prix_restructure'].set_index('id')
    df['action_realise'] = df['action_realise'].set_index('id')

    # on veut savoir pour chaque composant culture si celui-ci appartient à une culture "melange espece" / "melange variété"
    left = df['composant_culture']
    right = df['culture'][['melange_especes', 'melange_varietes']]
    df['composant_culture_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    left = df['composant_culture_concerne_intervention_realise']
    right = df['composant_culture_extanded'][['surface_relative', 'melange_especes', 'melange_varietes']]
    merge = pd.merge(left, right, left_on='composant_culture_id', right_index=True)

    # on commence par compter le nombre de composants de culture concernés par l'intervention
    nombre_composant_culture_concerne_intervention = pd.DataFrame(merge.groupby('intervention_realise_id').size()).rename(columns={0:'nombre'})

    # on fusionne ce résultat avec notre merge
    left = merge
    right = nombre_composant_culture_concerne_intervention
    merge = pd.merge(left, right, left_on='intervention_realise_id', right_index=True )

    # Attention, pour tout ceux qui ont déjà une surface relative, on doit recalculer la VRAIE surface relative...
    surface_totale = merge.loc[~merge['surface_relative'].isna()].groupby('intervention_realise_id')['surface_relative'].sum()

    left = merge
    right = surface_totale.rename('surface_relative_totale')
    merge = pd.merge(left, right, left_on='intervention_realise_id', right_index=True, how='left')


    # calcul de la surface relative corrigée dans les cas historiques qui posent problème
    merge.loc[merge['surface_relative_totale']>100, 'surface_relative_corrigee'] = (
        merge.loc[merge['surface_relative_totale']>100]['surface_relative'] / merge.loc[merge['surface_relative_totale']>100]['surface_relative_totale']
    )*100

    # affectation de la surface relative pour les cas qui ne posent pas problème 
    merge.loc[merge['surface_relative_totale']<=100, 'surface_relative_corrigee'] = merge.loc[merge['surface_relative_totale']<=100]['surface_relative']

    # affectation des surfaces relatives pour ceux qui ne sont pas saisis du tout
    merge.loc[merge['surface_relative_corrigee'].isna(), 'surface_relative_corrigee'] = (100 / merge.loc[merge['surface_relative_corrigee'].isna()]['nombre'])

    # on rajoute toutes les informations qu'on doit avoir pour fusionner avec le dataframe merge qu'on vient d'obtenir
    left = df['recolte_rendement_prix']
    right = df['recolte_rendement_prix_restructure']
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['recolte_rendement_prix_extanded']
    right = df['action_realise'][['intervention_realise_id']]
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='action_id', right_index=True, how='inner')

    left = df['recolte_rendement_prix_extanded'].reset_index()
    right = merge
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, on = ['composant_culture_id', 'intervention_realise_id'], how='left').set_index('id')

    # on remplace les données manquantes
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']].fillna('t')
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']].fillna('t')


    left = df['recolte_rendement_prix_extanded']
    right = merge.groupby('intervention_realise_id')['surface_relative_corrigee'].sum().rename('surface_relative_corrigee_totale')
    final_realise = pd.merge(left, right, left_on='intervention_realise_id', right_index=True, how='left')

    # Attention, on ne doit corriger que si ce n'est pas un mélange de variété / ou d'espèce !
    final_realise_1 = final_realise.loc[(final_realise['melange_especes']=='f') & (final_realise['melange_varietes'] == 'f')]
    final_realise_2 = final_realise.loc[(final_realise['melange_especes']=='t') | (final_realise['melange_varietes'] == 't')]

    # pour ceux qui ne sont pas des mélanges d'espèces : 
    final_realise.loc[final_realise_1.index, 'rendement_moy_corr'] = final_realise_1['rendement_moy'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'rendement_median_corr'] = final_realise_1['rendement_median'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'rendement_max_corr'] = final_realise_1['rendement_max'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index,'rendement_min_corr'] = final_realise_1['rendement_min'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'commercialisation_pct_corr'] = final_realise_1['commercialisation_pct'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'autoconsommation_pct_corr'] = final_realise_1['autoconsommation_pct'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'nonvalorisation_pct_corr'] = final_realise_1['nonvalorisation_pct'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']

    # pour ceux qui sont des mélanges d'espèces : 
    final_realise.loc[final_realise_2.index, 'rendement_moy_corr'] = final_realise_2['rendement_moy']
    final_realise.loc[final_realise_2.index, 'rendement_median_corr'] = final_realise_2['rendement_median']
    final_realise.loc[final_realise_2.index, 'rendement_max_corr'] = final_realise_2['rendement_max']
    final_realise.loc[final_realise_2.index,'rendement_min_corr'] = final_realise_2['rendement_min']
    final_realise.loc[final_realise_2.index, 'commercialisation_pct_corr'] = final_realise_2['commercialisation_pct']
    final_realise.loc[final_realise_2.index, 'autoconsommation_pct_corr'] = final_realise_2['autoconsommation_pct']
    final_realise.loc[final_realise_2.index, 'nonvalorisation_pct_corr'] = final_realise_2['nonvalorisation_pct']

    # on groupe pour obtenir un seul résultat par action / destination / rendement unite
    final_realise = final_realise.groupby(['destination', 'rendement_unite', 'action_id']).agg({
        'rendement_moy_corr' : 'sum',
        'rendement_median_corr' : 'sum',
        'rendement_max_corr' : 'sum',
        'rendement_min_corr' : 'sum', 
        'commercialisation_pct_corr' : 'sum',
        'autoconsommation_pct_corr' :'sum',
        'nonvalorisation_pct_corr' : 'sum'
    }).reset_index().replace(0, np.nan).round(2)

    return final_realise

def get_recolte_synthetise_outils_can(
        donnees
):
    """
    Permet d'obtenir une version synthétisée des informations relatives aux récoltes. 
    Cette fonction effectue plusieurs étapes d'agrégation et de correction des données, notamment en prenant 
    en compte les surfaces relatives et les mélanges d'espèces ou de variétés. Les résultats sont ensuite 
    regroupés par destination et unité de rendement.

    La fonction suit les étapes suivantes :
    1. Fusionne les informations sur les composants de culture avec les cultures, pour déterminer si un composant 
       appartient à un "mélange espèce" ou "mélange variété".
    2. Calcule la surface relative corrigée en tenant compte des surfaces relatives existantes et en les ajustant 
       si nécessaire.
    3. Agrège les données de rendement et d'interventions pour calculer les rendements corrigés (moyens, médian, 
       maximum et minimum).
    4. Regroupe les données finales par destination, unité de rendement et identifiant d'action, puis calcule les 
       totaux pour chaque groupe.

    Args:
        donnees (dict): Un dictionnaire contenant plusieurs DataFrames nécessaires à l'agrégation des informations
                        sur les récoltes :
                        - 'composant_culture' : Données des composants des cultures.
                        - 'culture' : Données des cultures associées aux composants.
                        - 'composant_culture_concerne_intervention_synthetise' : Données des composants 
                          concernés par les interventions réalisées.
                        - 'ccc_intervention_synthetise_restructure' : Données sur les interventions restructurées.
                        - 'recolte_rendement_prix' : Données des rendements des récoltes.
                        - 'recolte_rendement_prix_restructure' : Données des rendements restructurés.
                        - 'action_synthetise' : Données des actions synthétisées associées aux récoltes.

    Returns:
        pd.DataFrame: Un DataFrame avec des informations agrégées et corrigées sur les récoltes :
                      - `destination` : La destination des récoltes.
                      - `rendement_unite` : L'unité de mesure du rendement.
                      - `action_id` : L'identifiant de l'action réalisée.
                      - `rendement_moy_corr`, `rendement_median_corr`, `rendement_max_corr`, 
                        `rendement_min_corr` : Rendements corrigés par surface relative.
                      - `commercialisation_pct_corr`, `autoconsommation_pct_corr`, 
                        `nonvalorisation_pct_corr` : Pourcentages corrigés par surface relative de 
                        commercialisation, autoconsommation, et non valorisation.

    Exemple d'utilisation :
        donnees = {
            'composant_culture': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'composant_culture_concerne_intervention_synthetise': pd.DataFrame(...),
            'ccc_intervention_synthetise_restructure': pd.DataFrame(...),
            'recolte_rendement_prix': pd.DataFrame(...),
            'recolte_rendement_prix_restructure': pd.DataFrame(...),
            'action_synthetise': pd.DataFrame(...),
        }
        result = get_recolte_synthetise_outils_can(donnees)

    Notes:
        - La fonction traite des données historiques et applique des corrections spécifiques dans certains cas où 
          les surfaces totales dépassent 100%. 
        - Les résultats sont regroupés par destination et unité de rendement, et les rendements sont ajustés 
          en fonction des surfaces relatives corrigées.
    """
    df = donnees.copy()
    df['composant_culture'] = df['composant_culture'].set_index('id')
    df['culture'] = df['culture'].set_index('id')
    df['composant_culture_concerne_intervention_synthetise'] = df['composant_culture_concerne_intervention_synthetise'].set_index('id')
    df['ccc_intervention_synthetise_restructure'] = df['ccc_intervention_synthetise_restructure'].set_index('id')
    df['recolte_rendement_prix'] = df['recolte_rendement_prix'].set_index('id')
    df['recolte_rendement_prix_restructure'] = df['recolte_rendement_prix_restructure'].set_index('id')
    df['action_synthetise'] = df['action_synthetise'].set_index('id')

    # on veut savoir pour chaque composant culture si celui-ci appartient à une culture "melange espece" / "melange variété"
    left = df['composant_culture']
    right = df['culture'][['melange_especes', 'melange_varietes']]
    df['composant_culture_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    left = df['composant_culture_concerne_intervention_synthetise']
    right = df['ccc_intervention_synthetise_restructure']
    df['composant_culture_concerne_intervention_synthetise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['composant_culture_concerne_intervention_synthetise_extanded'] 
    right = df['composant_culture_extanded'][['surface_relative', 'melange_especes', 'melange_varietes']]
    merge = pd.merge(left, right, left_on='composant_culture_id', right_index=True)

    # on commence par compter le nombre de composants de culture concernés par l'intervention
    nombre_composant_culture_concerne_intervention = pd.DataFrame(merge.groupby('intervention_synthetise_id').size()).rename(columns={0:'nombre'})

    # on fusionne ce résultat avec notre merge
    left = merge
    right = nombre_composant_culture_concerne_intervention
    merge = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True , how='left')

    # Attention, pour tout ceux qui ont déjà une surface relative, on doit recalculer la VRAIE surface relative...
    surface_totale = merge.loc[~merge['surface_relative'].isna()].groupby('intervention_synthetise_id')['surface_relative'].sum()

    left = merge
    right = surface_totale.rename('surface_relative_totale')
    merge = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True, how='left')


    # calcul de la surface relative corrigée dans les cas historiques qui posent problème
    merge.loc[merge['surface_relative_totale']>100, 'surface_relative_corrigee'] = (
        merge.loc[merge['surface_relative_totale']>100]['surface_relative'] / merge.loc[merge['surface_relative_totale']>100]['surface_relative_totale']
    )*100

    # affectation de la surface relative pour les cas qui ne posent pas problème 
    merge.loc[merge['surface_relative_totale']<=100, 'surface_relative_corrigee'] = merge.loc[merge['surface_relative_totale']<=100]['surface_relative']

    # affectation des surfaces relatives pour ceux qui ne sont pas saisis du tout
    merge.loc[merge['surface_relative_corrigee'].isna(), 'surface_relative_corrigee'] = (100 / merge.loc[merge['surface_relative_corrigee'].isna()]['nombre'])

    # on rajoute toutes les informations qu'on doit avoir pour fusionner avec le dataframe merge qu'on vient d'obtenir
    left = df['recolte_rendement_prix']
    right = df['recolte_rendement_prix_restructure']
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['recolte_rendement_prix_extanded']
    right = df['action_synthetise'][['intervention_synthetise_id']]
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='action_id', right_index=True, how='inner')


    left = df['recolte_rendement_prix_extanded'].reset_index()
    right = merge
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, on = ['composant_culture_id', 'intervention_synthetise_id'], how='left').set_index('id')

    # on remplace les données manquantes
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']].fillna('t')
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']].fillna('t')


    left = df['recolte_rendement_prix_extanded']
    right = merge.groupby('intervention_synthetise_id')['surface_relative_corrigee'].sum().rename('surface_relative_corrigee_totale')
    final_synthetise = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True, how='left')

    # attention, il y a un problème dans les données historique (juste 2 actions qui posent problème...)
    final_synthetise = final_synthetise.reset_index().drop_duplicates(subset='id').set_index('id')

    # Attention, on ne doit corriger que si ce n'est pas un mélange de variété / ou d'espèce !
    final_synthetise_1 = final_synthetise.loc[(final_synthetise['melange_especes']=='f') & (final_synthetise['melange_varietes'] == 'f')]
    final_synthetise_2 = final_synthetise.loc[(final_synthetise['melange_especes']=='t') | (final_synthetise['melange_varietes'] == 't')]

    final_synthetise.loc[final_synthetise_1.index, 'rendement_moy_corr'] = final_synthetise_1['rendement_moy'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'rendement_median_corr'] = final_synthetise_1['rendement_median'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'rendement_max_corr'] = final_synthetise_1['rendement_max'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index,'rendement_min_corr'] = final_synthetise_1['rendement_min'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'commercialisation_pct_corr'] = final_synthetise_1['commercialisation_pct'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'autoconsommation_pct_corr'] = final_synthetise_1['autoconsommation_pct'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'nonvalorisation_pct_corr'] = final_synthetise_1['nonvalorisation_pct'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']

    final_synthetise.loc[final_synthetise_2.index, 'rendement_moy_corr'] = final_synthetise_2['rendement_moy']
    final_synthetise.loc[final_synthetise_2.index, 'rendement_median_corr'] = final_synthetise_2['rendement_median']
    final_synthetise.loc[final_synthetise_2.index, 'rendement_max_corr'] = final_synthetise_2['rendement_max']
    final_synthetise.loc[final_synthetise_2.index,'rendement_min_corr'] = final_synthetise_2['rendement_min']
    final_synthetise.loc[final_synthetise_2.index, 'commercialisation_pct_corr'] = final_synthetise_2['commercialisation_pct']
    final_synthetise.loc[final_synthetise_2.index, 'autoconsommation_pct_corr'] = final_synthetise_2['autoconsommation_pct']
    final_synthetise.loc[final_synthetise_2.index, 'nonvalorisation_pct_corr'] = final_synthetise_2['nonvalorisation_pct']

    final_synthetise = final_synthetise.groupby(['destination', 'rendement_unite', 'action_id']).agg({
        'rendement_moy_corr' : 'sum',
        'rendement_median_corr' : 'sum',
        'rendement_max_corr' : 'sum',
        'rendement_min_corr' : 'sum', 
        'commercialisation_pct_corr' : 'sum',
        'autoconsommation_pct_corr' :'sum',
        'nonvalorisation_pct_corr' : 'sum'
    }).reset_index().replace(0, np.nan).round(2)

    return final_synthetise

# FONCTION POUR LES RECOLTES
def get_recolte_outils_can(
    donnees
):
    """ 
    Permet d'obtenir les informations sur les récoltes réalisées. La fonction récupère et fusionne 
    les données relatives aux récoltes effectuées à partir de deux fonctions : 
    `get_recolte_realise_outils_can` pour les récoltes réelles et `get_recolte_synthetise_outils_can` 
    pour les récoltes synthétisées. Ensuite, elle fusionne ces résultats pour produire un seul tableau final.

    Args:
        donnees (dict): Un dictionnaire contenant plusieurs DataFrames nécessaires: 
            - Les autres tables utilisées dans `get_intervention_synthetise_outils_can_context`,
                `get_recolte_realise_outils_can`, `get_recolte_synthetise_outils_can`
    
    Returns:
        pd.DataFrame: Un DataFrame consolidé avec les informations sur les récoltes réalisées et synthétisées. 
                      Le résultat contient les colonnes 
                        `destination_id`, 
                        `rendement_unite`,
                        `action_id` 
                      ainsi que des informations agrégées sur les rendements, en tenant compte des ajustements 
                      et des corrections historiques.

    Exemple d'utilisation :
        donnees = {
            'composant_culture': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'action_synthetise': pd.DataFrame(...),
            ...
        }
        result = get_recolte_outils_can(donnees)

    Notes:
        - La fonction fait appel à deux sous-fonctions (`get_recolte_realise_outils_can` et 
          `get_recolte_synthetise_outils_can`) pour récupérer et combiner les résultats des récoltes réalisées.
        - La gestion des mélanges d'espèces et des problèmes historiques dans les données doit être prise en compte 
          pour assurer l'exactitude des résultats.
    """
    resultat_realise = get_recolte_realise_outils_can(donnees)
    resultat_synthetise = get_recolte_synthetise_outils_can(donnees)
    final = pd.concat([resultat_realise, resultat_synthetise])

    return final

# FONCTION LES ZONES
def get_zone_realise_outils_can(
    donnees
):
    """
    Permet d'obtenir les informations liées aux zones. La fonction combine les données de deux sous-fonctions 
    pour fournir des informations sur les cultures, les variétés, et les rendements associés à chaque zone.

    Args:
        donnees (dict): 
                - Les autres tables utilisées dans `get_zone_realise_culture_outils_can`, 
                `get_zone_realise_rendement_outils_can`
    
    Returns:
        pd.DataFrame: Un DataFrame contenant les informations sur les zones, avec les colonnes suivantes :
                        - `id` : Identifiant de la zone.
                        - `variete_nom` : Concaténation des variétés sur la zone.
                        - `culture_especes_edi` : Concaténation des espèces sur la zone.
                        - `rendement_culture` : Concaténation des rendements de culture sur la zone.

    Exemple d'utilisation :
        donnees = {
            'zone': pd.DataFrame(...),
            ...
        }
        result = get_zone_realise_outils_can(donnees)
    """
    df_zone= donnees['zone']

    left = df_zone
    right = get_zone_realise_culture_outils_can(donnees)
    merge = pd.merge(left, right, on='id', how='left')

    left = merge
    right = get_zone_realise_rendement_outils_can(donnees)
    merge = pd.merge(left, right, on='id', how='left')
    
    return merge[['id', 'variete_nom', 'culture_especes_edi', 'rendement_culture']]

def get_zone_realise_rendement_outils_can(
    donnees
):
    """
    Permet d'obtenir les informations de rendement des cultures liées aux zones. La fonction calcule la somme des rendements 
    moyens pour chaque zone et les regroupe sous une forme concaténée pour chaque zone.

    À la fin, la fonction retourne un DataFrame où chaque zone est associée à un rendement total sous forme de chaîne concaténée.


    Args:
        donnees (dict): 
            - Les autres tables utilisées dans `get_recolte_realise_outils_can`, 
            - 'action_realise_agrege' : Données des actions en réalisé.

    Returns:
        pd.DataFrame: Un DataFrame contenant les rendements totaux par zone, avec les colonnes suivantes :
                        - `id` : Identifiant de la zone.
                        - `rendement_culture` : Rendement total concaténé sous forme de chaîne.

    Exemple d'utilisation :
        donnees = {
            'zone': pd.DataFrame(...),
            'action_realise_agrege': pd.DataFrame(...),
            ...
        }
        result = get_zone_realise_rendement_outils_can(donnees)

    Notes:
        - Les rendements sont regroupés par zone et concaténés pour former une chaîne de caractères qui inclut 
          la destination, le rendement moyen corrigé, et l'unité de rendement.
        - La fonction utilise les données des récoltes réalisées et les actions agrégées pour obtenir les informations de rendement.
    """
    # on ajoute les informations sur les action
    left = get_recolte_realise_outils_can(donnees)
    right = donnees['action_realise_agrege'].set_index('id')[['zone_id']]
    recolte_rendement_prix_extanded = pd.merge(left, right, left_on='action_id', right_index=True, how='left')

    unite_rendement = pd.DataFrame.from_records([UNITE_RENDEMENT]).melt().rename(
        columns={'variable' : 'unite_agrosyst', 'value' : 'unite_utilisateur'}
    )

    left = recolte_rendement_prix_extanded
    right = unite_rendement
    recolte_rendement_prix_extanded = pd.merge(left, right, left_on='rendement_unite', right_on='unite_agrosyst', how='left')

    # on effectue la somme pour ceux où n'y a que le rendement_moy qui diffère :  
    recolte_rendement_prix_extanded = recolte_rendement_prix_extanded.groupby(['zone_id', 'destination', 'unite_utilisateur']).agg({
        'rendement_moy_corr' : 'sum'
    }).reset_index()

    recolte_rendement_prix_extanded['rendement_total'] = '['+recolte_rendement_prix_extanded['destination'].astype('str')+']'+'|'+\
        recolte_rendement_prix_extanded['rendement_moy_corr'].astype('str')+'|'+\
            recolte_rendement_prix_extanded['unite_utilisateur'].astype('str')


    res = recolte_rendement_prix_extanded.groupby('zone_id').agg({
        'rendement_total' : lambda x: '#'.join(dict.fromkeys([item for item in x if item.strip()])),
    }).rename(columns={'rendement_total' : 'rendement_culture'})
    
    return res.reset_index().rename(columns={'zone_id' : 'id'})


def get_zone_realise_culture_outils_can(
        donnees
):
    """
    Permet d'obtenir les informations des cultures liées aux zones, notamment les espèces cultivées et les variétés. 

    La sortie contient les colonnes suivantes :
        - `id` : Identifiant de la zone.
        - `culture_especes_edi` : Liste des espèces cultivées dans la zone, concaténées sous forme de chaîne.
        - `variete_nom` : Liste des variétés cultivées dans la zone, concaténées sous forme de chaîne.

    Args:
        donnees (dict): 
                - 'culture' : Données des cultures.
                - 'composant_culture' : Composants de cultures. 
                - 'espece' : Espèces.
                - 'variete' : Variétés.
                - 'noeuds_realise' : Noeuds en réalisé.
                - 'plantation_perenne_realise' : Plantation perenne en réalisé.

    Returns:
        pd.DataFrame: Un DataFrame contenant les informations sur les cultures par zone, avec les colonnes suivantes :
                        - `id` : Identifiant de la zone.
                        - `culture_especes_edi` : Liste concaténée des espèces cultivées dans la zone.
                        - `variete_nom` : Liste concaténée des variétés cultivées dans la zone.

    Exemple d'utilisation :
        donnees = {
            'culture': pd.DataFrame(...),
            'composant_culture': pd.DataFrame(...),
            'espece': pd.DataFrame(...),
            'variete': pd.DataFrame(...),
            'noeuds_realise': pd.DataFrame(...),
            'plantation_perenne_realise': pd.DataFrame(...),
            ...
        }
        result = get_zone_realise_culture_outils_can(donnees)

    Notes:
        - Les valeurs manquantes sont remplacées par des chaînes vides pour éviter les erreurs lors de la concaténation.
    """
    df_culture = donnees['culture']
    df_composant_culture = donnees['composant_culture']
    df_espece = donnees['espece'].set_index('id')
    df_variete = donnees['variete'].set_index('id')
    df_noeuds_realise = donnees['noeuds_realise']
    df_plantation_perenne_realise = donnees['plantation_perenne_realise']
    df_connection_realise = donnees['connection_realise']

    # on rajoute au composant de culture les informations sur les variétés et les espèces
    left = df_composant_culture
    right = df_espece[
        ['libelle_espece_botanique', 'libelle_qualifiant_aee', 
         'libelle_type_saisonnier_aee', 'libelle_destination_aee']
    ]

    df_composant_culture_extanded = pd.merge(left, right, left_on='espece_id', right_index=True, how='left')

    left = df_composant_culture_extanded
    right = df_variete[['denomination']]
    df_composant_culture_extanded = pd.merge(left, right, left_on='variete_id', right_index=True, how='left')

    # On fill les NaN avec ''
    df_composant_culture_extanded= df_composant_culture_extanded.fillna('')

    # On crée la description succinte de l'espèce 
    df_composant_culture_extanded.loc[:, 'esp'] = df_composant_culture_extanded[['libelle_espece_botanique']]
    df_composant_culture_extanded.loc[:, 'var'] = df_composant_culture_extanded[['denomination']]


    # On créé la chaîne correspondant à la description complète du composant de culture
    df_composant_culture_extanded.loc[:, 'esp_complet'] = df_composant_culture_extanded[[
        'libelle_espece_botanique', 
        'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 
        'libelle_destination_aee'
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    # On ajoute l'information de la variété
    df_composant_culture_extanded.loc[
        df_composant_culture_extanded['var'] !=  '', 'var'
    ] = df_composant_culture_extanded.loc[df_composant_culture_extanded['var'] !=  '']['var']

    df_composant_culture_extanded['var'] = df_composant_culture_extanded['var'].fillna('')
    
    df_composant_cutlure_with_var = df_composant_culture_extanded.loc[df_composant_culture_extanded['var'] != '']
    df_composant_culture_extanded.loc[:,'esp_complet_var'] = df_composant_culture_extanded['esp_complet']
    df_composant_culture_extanded.loc[df_composant_cutlure_with_var.index,'esp_complet_var'] = df_composant_culture_extanded['esp_complet'] + \
        ' - '+ df_composant_culture_extanded['var']

    # on rajoute à la culture l'information de la zone pour les assolées
    left = df_culture.rename(columns={'id' : 'culture_id'})
    right = df_noeuds_realise.rename(columns={'id' : 'noeuds_realise_id'})
    merge_assolee = pd.merge(left, right, on='culture_id', how='inner')

    # on rajoute aussi la culture intermediaire
    left = df_connection_realise.rename(columns={'id' : 'connection_id'})
    right = df_noeuds_realise.rename(columns={'id' : 'noeuds_realise_id'})
    noeuds_connection = pd.merge(left, right, left_on='source_noeuds_realise_id', right_on = 'noeuds_realise_id', how='inner')

    left = df_culture.rename(columns={'id' : 'culture_id'})
    right = noeuds_connection[['culture_intermediaire_id','noeuds_realise_id','rang','zone_id']]
    merge_ci = pd.merge(left, right, left_on='culture_id', right_on = 'culture_intermediaire_id', how='inner')
    
    # on rajoute à la culture l'information de la zone pour les perennes
    left = df_culture.rename(columns={'id' : 'culture_id'})
    right = df_plantation_perenne_realise.rename(columns={'id' : 'plantation_perenne_realise_id'})
    merge_perenne = pd.merge(left, right, on='culture_id', how='inner')

    merge = pd.concat([merge_assolee, merge_ci, merge_perenne])

    # on rajoute aux composants de culture les informations sur les zones :
    left = df_composant_culture_extanded[['esp', 'var', 'esp_complet', 'esp_complet_var', 'culture_id']]
    right = merge[['zone_id', 'noeuds_realise_id', 'plantation_perenne_realise_id', 'culture_id']]
    merge = pd.merge(left, right, on='culture_id', how='inner')

    df_final = merge.groupby([
        'zone_id'
    ]).agg({
        'esp_complet_var' : ' ; '.join, 
        'esp_complet' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'esp': lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()])),
        'var' : lambda x: ', '.join(dict.fromkeys([item for item in x if item.strip()]))
    })

    df_final = df_final.rename(
        columns = {
            'esp' : 'culture_especes_edi', 
            'var' : 'variete_nom'
        }
    )

    return df_final.reset_index().rename(columns={'zone_id' : 'id'})


def get_sdc_realise_outils_can(
    donnees
):
    """
    Permet d'obtenir les informations des cultures liées aux SDC (Systèmes de Culture), notamment les espèces et les variétés cultivées dans chaque SDC.

    La sortie contient les colonnes suivantes :
        - `id` : Identifiant du SDC.
        - `especes` : Liste concaténée des espèces cultivées dans le SDC.
        - `varietes` : Liste concaténée des variétés cultivées dans le SDC.

    Args:
        donnees (dict): Un dictionnaire contenant les DataFrames nécessaires,
            - 'zone' : Zones.
            - 'parcelle' : Parcelles.
            - Les autres tables utilisées dans `get_zone_realise_culture_outils_can`, 

    Returns:
        pd.DataFrame: Un DataFrame contenant les informations sur les espèces et variétés cultivées dans chaque SDC, avec les colonnes suivantes :
                        - `id` : Identifiant du SDC.
                        - `especes` : Concaténation des espèces cultivées dans le SDC.
                        - `varietes` : Concaténation des variétés cultivées dans le SDC.

    Exemple d'utilisation :
        donnees = {
            'zone': pd.DataFrame(...),
            'parcelle': pd.DataFrame(...),
            ...
        }
        result = get_sdc_realise_outils_can(donnees)

    """
    # Fonction pour fusionner les valeurs d'une colonne sépare par une virgule, en évitant les doublons
    def merge_concat(values):
        # Split les valeurs par ", ", puis enlever les doublons avec set, enfin rejoindre avec ", "
        clean_values = [val.strip() for val in ', '.join(values).split(', ') if val.strip()]
        return ', '.join(sorted(set(clean_values)))
    
    zone = donnees['zone']
    parcelle = donnees['parcelle'].set_index('id')
    
    # on obtient pour chaque zone la concaténation des cultures présentes en mobilisant 
    # la fonction get_zone_realise_culture_outils_can
    left = zone
    right = get_zone_realise_culture_outils_can(donnees)
    zone_extanded = pd.merge(left, right, on='id', how='left')

    # on ajoute l'information du sdc_id à travers la parcelle
    left = zone_extanded
    right = parcelle
    zone_extanded = pd.merge(left, right, left_on='parcelle_id', right_index=True, how='left')

    # on fill les nan avec la chaine de caractère vide : 
    zone_extanded.loc[:, 'culture_especes_edi'] = zone_extanded['culture_especes_edi'].fillna('')
    zone_extanded.loc[:, 'variete_nom'] = zone_extanded['variete_nom'].fillna('')

    # on groupe par sdc_id :
    sdc_extanded = zone_extanded.groupby('sdc_id').agg({
        'culture_especes_edi': merge_concat, 
        'variete_nom' : merge_concat
    })

    return sdc_extanded.reset_index().rename(columns={
        'sdc_id' : 'id', 
        'culture_especes_edi' : 'especes', 
        'variete_nom': 'varietes'
    })


# def get_noeuds_realise_outils_can(
#     donnees
# ):
#     """
#         Permet d'obtenir le culture_id du noeuds précédent
#                 - precedent_id (culture_id du précédent)
#     """
#     print(donnees)



def get_parcelle_realise_outils_can(
    donnees
):
    """
    Permet d'obtenir les informations des cultures liées aux parcelles, notamment les espèces, les variétés et les rendements des cultures dans chaque parcelle.

    Args:
        donnees (dict): Un dictionnaire contenant les DataFrames nécessaires,
            - 'zone' : Zones.
            - 'parcelle' : Parcelles.
            - Les autres tables utilisées dans `get_zone_realise_culture_outils_can`, 

    Returns:
        pd.DataFrame: Un DataFrame contenant les informations sur les espèces, variétés et rendements cultivés dans chaque parcelle, avec les colonnes suivantes :
                        - `id` : Identifiant de la parcelle.
                    - `especes` : Concaténation des espèces cultivées dans la parcelle.
                    - `varietes` : Concaténation des variétés cultivées dans la parcelle.
                    - `rendement` : Concaténation des rendements des cultures dans la parcelle.

    Exemple d'utilisation :
        donnees = {
            'zone': pd.DataFrame(...),
            'parcelle': pd.DataFrame(...),
            ...
        }
        result = get_parcelle_realise_outils_can(donnees)

    Notes:
        - Les valeurs manquantes pour les espèces, variétés et rendements sont remplacées par des chaînes vides avant d'effectuer les agrégations.
    """

    # Fonction pour fusionner les valeurs d'une colonne sépare par une virgule, en évitant les doublons
    def merge_concat(values):
        # Split les valeurs par ", ", puis enlever les doublons avec set, enfin rejoindre avec ", "
        clean_values = [val.strip() for val in ', '.join(values).split(', ') if val.strip()]
        return ', '.join(sorted(set(clean_values)))
    
    zone = donnees['zone']
    parcelle = donnees['parcelle'].set_index('id')
    
    # on obtient pour chaque zone la concaténation des cultures présentes en mobilisant 
    # la fonction get_zone_realise_culture_outils_can
    left = zone
    right = get_zone_realise_outils_can(donnees)
    zone_extanded = pd.merge(left, right, on='id', how='left')

    left = zone_extanded
    right = parcelle
    zone_extanded = pd.merge(left, right, left_on='parcelle_id', right_index=True, how='left')

    # on fill les nan avec la chaine de caractère vide : 
    zone_extanded.loc[:, 'culture_especes_edi'] = zone_extanded['culture_especes_edi'].fillna('')
    zone_extanded.loc[:, 'variete_nom'] = zone_extanded['variete_nom'].fillna('')
    zone_extanded.loc[:, 'rendement_culture'] = zone_extanded['rendement_culture'].fillna('')


    # on groupe par sdc_id :
    sdc_extanded = zone_extanded.groupby('parcelle_id').agg({
        'culture_especes_edi': merge_concat, 
        'variete_nom' : merge_concat,
        'rendement_culture' : merge_concat
    })

    return sdc_extanded.reset_index().rename(columns={
        'parcelle_id' : 'id', 
        'culture_especes_edi' : 'especes', 
        'variete_nom' : 'varietes',
        'rendement_culture' : 'rendement'
    })


# FONCTION POUR ASSOLEES_SYNTHETISE 
def get_culture_indicateur_branche(
    donnees
):
    """
        Permet d'obtenir L'information (d'après moi inexploitable) de culture_indicateur_branche telle
        qu'on la trouve dans les exports en masse
    """
    df_noeuds_synthetise = donnees['noeuds_synthetise'].set_index('id')
    

    return 0