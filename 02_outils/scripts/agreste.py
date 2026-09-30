"""
	Regroupe les fonctions qui enregistrent et restructurent les données issues d'Agreste
"""

import pandas as pd
import numpy as np
import geopandas as gpd


def get_agreste_ift_gcpe_reference_region(donnees):
    
    """
        Cet outil sert juste à rendre disponiblesur Datagrosyst les donnée obtenues dans 02_outils/data/external_data/agreste
        Ici on fait le choix de stocker en base car : 
        - les données traitées sont extrêmement petites 
        - les données sont très utiles pour les utilisateurs
        - les données sont mobilisées dans certains magasins (tdb_magasin_can)

        On fusionne les dataframes pk pour n'en faire qu'un seul avec les colonnes suivantes : 
        - campagne
        - nom_ancienne_region
        - ift_moyen_gcpe_can

        > ATTENTION, en cas de mise à jour des données PK (exemple : nouvelle campagne) on doit bien penser à mettre à jour
        > cet outil ou la nouvelle campagne ne sera pas disponible sous Datagrosyst.
    """
    df = donnees.copy()

    agreste_2017 = df['agreste_ift_culture_gcpe_reference_region_2017']
    agreste_2017.loc[:, 'campagne'] = 2017

    agreste_2021 = df['agreste_ift_culture_gcpe_reference_region_2021']
    agreste_2021.loc[:, 'campagne'] = 2021

    res = pd.concat([
        agreste_2017, 
        agreste_2021
    ])

    return res


def get_agreste_ift_arboriculture_reference_region(donnees):
    
    """
        Cet outil sert juste à rendre disponiblesur Datagrosyst les donnée obtenues dans 02_outils/data/external_data/agreste
        Ici on fait le choix de stocker en base car : 
        - les données traitées sont extrêmement petites 
        - les données sont très utiles pour les utilisateurs
        - les données sont mobilisées dans certains magasins (tdb_magasin_can)

        On fusionne les dataframes pk pour n'en faire qu'un seul avec les colonnes suivantes : 
        - campagne
        - nom_ancienne_region
        - ift_moyen_gcpe_can

        > ATTENTION, en cas de mise à jour des données PK (exemple : nouvelle campagne) on doit bien penser à mettre à jour
        > cet outil ou la nouvelle campagne ne sera pas disponible sous Datagrosyst.
    """
    df = donnees.copy()

    agreste_2018 = df['agreste_ift_culture_arboriculture_reference_region_2018']
    agreste_2018.loc[:, 'campagne'] = 2018

    agreste_2024 = df['agreste_ift_culture_arboriculture_reference_region_2024']
    agreste_2024.loc[:, 'campagne'] = 2024

    res = pd.concat([
        agreste_2018, 
        agreste_2024
    ])

    return res


def get_ift_agreste_viticulture(donnees):
    
    """
        Cet outil sert juste à rendre disponiblesur Datagrosyst les donnée obtenues dans 02_outils/data/external_data/agreste/ift/viticulture
        Ici on fait le choix de stocker en base car : 
        - les données traitées sont extrêmement petites 
        - les données sont très utiles pour les utilisateurs
        - les données sont mobilisées dans certains magasins (tdb_magasin_can)
    """
    df = donnees.copy()

    agreste_ift_viticulture_departement = df['agreste_ift_viticulture_departement']

    return agreste_ift_viticulture_departement