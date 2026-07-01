"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "Tableau_de_bord_can".
"""
import pandas as pd
import numpy as np


def get_reseaux_rattachement_sdc_outils_tableau_de_bord_can(
    donnees
):
    """
    Permet d'obtenir les informations du réseau de rattachement d'un système de culture.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'reseau' : Données des réseaux associés aux dispositifs.
            - 'liaison_reseaux' : Liaison des réseaux et autres données associées.
            - 'liaison_sdc_reseau' : Affectation des systèmes de cultures à un ou plusieurs réseaux.
            - 'sdc' : Données des systèmes de cutlures.
            
    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations agrégées sur les sdc avec les colonnes suivantes :
            - `id` : Identifiant du sdc.
            - `reseaux_ir` : Concaténation des réseaux associés au domaine (séparés par un pipe `|`).
            - `reseaux_it` : Concaténation des réseaux parents associés au domaine (séparés par une pipe `|`).

    Exemple d'utilisation :
        donnees = {
            'reseau': pd.DataFrame(...),
            'liaison_reseaux': pd.DataFrame(...),
            'liaison_sdc_reseau': pd.DataFrame(...),
            'sdc': pd.DataFrame(...),
        }
        result = get_reseaux_rattachement_sdc(donnees)
    """
    df = donnees.copy()
    df['reseau'] = donnees['reseau'].set_index('id')
    df['liaison_reseaux'] = donnees['liaison_reseaux']
    df['liaison_sdc_reseau'] = donnees['liaison_sdc_reseau']
    df['sdc'] = donnees['sdc'].set_index('id')

    # pour chaque liaison de réseau, on obtient l'information complète
    left = df['liaison_sdc_reseau']
    right = df['sdc'][['dispositif_id']]
    df['liaison_sdc_reseau_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    # pour chaque laison, on ajoute les informations sur le réseau
    left = df['liaison_sdc_reseau_extanded'] 
    right = df['reseau'][['nom', 'code_convention_dephy']]
    df['liaison_sdc_reseau_extanded']  = pd.merge(left, right, left_on='reseau_id', right_index=True, how='left')

    # on obtient aussi le lien vers le parent du réseau
    left = df['liaison_sdc_reseau_extanded']
    right = df['liaison_reseaux']
    df['liaison_sdc_reseau_extanded']  = pd.merge(left, right, on='reseau_id', how='left')

    # on ajoute les informations sur le réseau parent
    left = df['liaison_sdc_reseau_extanded'] 
    right = df['reseau'].rename(columns={
            'nom' : 'nom_reseau_parent', 
            'code_convention_dephy' : 'code_convention_dephy_reseau_parent'
            }
    )
    df['liaison_sdc_reseau_extanded']  = pd.merge(left, right, left_on='reseau_parent_id', right_index=True).dropna(subset=['nom', 'nom_reseau_parent']).fillna('')

    res = df['liaison_sdc_reseau_extanded'] .groupby('sdc_id').agg({
        'nom' : lambda x: '|'.join(x.unique()),
        'nom_reseau_parent' : lambda x: '|'.join(x.unique()),
        'code_convention_dephy' : lambda x: '|'.join(x.unique())
    }).rename(columns={
        'nom' : 'reseaux_ir',
        'nom_reseau_parent' : 'reseaux_it',
        'code_convention_dephy' : 'codes_convention_dephy'
    })
    return res.reset_index().rename(columns={'sdc_id' : 'id'})



def get_surface_sdc_realise_outils_tableau_de_bord_can(
    donnees
):
    """
    Permet d'obtenir la SAU des sdc en réalisé en sommant les surfaces des parcelles contenues dans le sdc
    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'parcelle' : Données des parcelles
            
    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations agrégées sur les sdc avec les colonnes suivantes :
            - `id` : Identifiant du sdc.
            - `surface_sdc` : Surface du système de culture 

    Exemple d'utilisation :
        donnees = {
            'parcelle': pd.DataFrame(...),
        }
        result = get_surface_sdc_realise_outils_tableau_de_bord_can(donnees)
    """
    df = donnees.copy()
    df['parcelle'] = df['parcelle'].set_index('id')

    # pour chaque parcelle
    res = df['parcelle'].groupby('sdc_id').agg({'surface' : 'sum'}).rename(columns={'surface' : 'surface_sdc'})

    return res.reset_index().rename(columns={'sdc_id' : 'id'})
