"""
	Regroupe les fonctions qui constituent en des restructuration des fichiers initiaux afin de faciliter leur utilisation
"""
import pandas as pd
import numpy as np


def restructuration_noeuds_synthetise(donnees):
    """ 
        fonction permettant d'obtenir pour chaque noeuds_synthetise, le bon culture_id plutôt que le culture_code
    """
    donnees = donnees.copy()
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')

    # obtention de la campagne pour le noeuds synthétisé
    left = donnees['noeuds_synthetise'][['id', 'culture_code', 'synthetise_id']]
    right = donnees['synthetise'][['sdc_id']]
    merge = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    left = merge
    right = donnees['sdc'][['campagne']]
    donnees['noeuds_synthetise_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    # obtention de la campagne pour la cutlure
    left = donnees['culture'].set_index('id')
    right = donnees['domaine'].set_index('id')[['campagne']]
    donnees['culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['noeuds_synthetise_extanded']
    right = donnees['culture_extanded'].reset_index()[['id', 'code', 'campagne']].rename(columns={'id' : 'culture_id'})
    donnees['noeuds_synthetise_restructured'] = pd.merge(left, right, left_on=['culture_code', 'campagne'], right_on=['code', 'campagne'])

    return donnees['noeuds_synthetise_restructured'].set_index('id')[['culture_id']]


def restructuration_connection_synthetise(donnees):
    """
        fonction permettant d'obtenir, pour chaque connection_synthetise, un culture_intermediaire_id plutôt qu'un culture_intermediaire_code
    """
    donnees = donnees.copy()
    donnees['noeuds_synthetise'] = donnees['noeuds_synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    # obtention de la campagne pour la connexion en synthétisé
    left = donnees['connection_synthetise'][['id', 'cible_noeuds_synthetise_id', 'culture_intermediaire_code']]
    right = donnees['noeuds_synthetise'][['culture_code', 'synthetise_id']].rename(columns={'id' : 'noeuds_synthetise_id'})
    merge = pd.merge(left, right, left_on='cible_noeuds_synthetise_id', right_index=True, how='left').set_index('id')

    left = merge
    right = donnees['synthetise'][['sdc_id']]
    merge = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    left = merge
    right = donnees['sdc'][['campagne']]
    donnees['connection_synthetise_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')[['culture_intermediaire_code', 'campagne']].dropna()

    # obtention de la campagne pour la culture
    left = donnees['culture'].set_index('id')
    right = donnees['domaine'].set_index('id')[['campagne']]
    donnees['culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['connection_synthetise_extanded'].reset_index()
    right = donnees['culture_extanded'].reset_index()[['id', 'code', 'campagne']].rename(columns={'id' : 'culture_intermediaire_id'})
    donnees['connection_synthetise_restructured'] = pd.merge(left, right, left_on=['culture_intermediaire_code', 'campagne'], right_on=['code', 'campagne'])

    return donnees['connection_synthetise_restructured'].set_index('id')[['culture_intermediaire_id']]

def restructuration_intervention_synthetise(donnees):
    """
        fonction permettant de remplacer le combinaison_outil_code par un combinaison_outil_id dans les intervention en synthétisé
    """
    donnees = donnees.copy()

    donnees['intervention_synthetise'] = donnees['intervention_synthetise'].set_index('id')
    donnees['connection_synthetise'] = donnees['connection_synthetise'].set_index('id')
    donnees['noeuds_synthetise'] = donnees['noeuds_synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')
    donnees['synthetise'] = donnees['synthetise'].set_index('id')

    # obtention de la campagne pour l'intervention en synthétisé --> à cette échelle, on peut utiliser les fichier d'agrégation