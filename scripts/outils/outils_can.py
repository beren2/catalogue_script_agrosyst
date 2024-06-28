"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "CAN".
"""

import pandas as pd

def get_intervention_realise_outils_can(
    donnees
):
    """
        Permet d'obtenir un dataframe qui fait directement le bilan sur les espèces concernées par une intervention. 
    """
    df_composant_culture_concerne_intervention_realise = donnees['composant_culture_concerne_intervention_realise']
    df_espece = donnees['espece']
    df_variete = donnees['variete']
    df_culture = donnees['culture']
    df_composant_culture = donnees['composant_culture']

    # Ajout des informations "espèces / variétés" au composant de culture
    left = df_composant_culture
    right = df_espece[[
        'id', 'libelle_espece_botanique', 'libelle_qualifiant_aee',
        'libelle_type_saisonnier_aee', 'libelle_destination_aee'
    ]].rename(columns={'id' : 'espece_id'})
    df_composant_culture_extanded = pd.merge(left, right, on='espece_id', how='left')

    left = df_composant_culture_extanded
    right = df_variete[[
        'id', 'denomination'
    ]].rename(columns={'id' : 'variete_id'})
    df_composant_culture_extanded = pd.merge(left, right, on='variete_id', how='left')

    # Ajout des informations dans le dataframe principal 
    left = df_composant_culture_concerne_intervention_realise[['id', 'composant_culture_id']]
    right = df_composant_culture_extanded.rename(columns={'id' : 'composant_culutre_id'})
    df_studied = pd.merge(left, right, on='composant_culture_id', how='left')

    df_studied = df_studied.fillna('')
    df_studied['description'] = df_studied[[
        'libelle_espece_botanique', 'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 'libelle_destination_aee', 
        'denomination'
    ]]

    return df_studied
