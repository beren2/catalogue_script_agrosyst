"""
	Regroupe les fonctions qui consistent à faire un pont entre une échelle de donnnées Agrosyst et un référentiel (externe préférentiellement)
"""

import pandas as pd
import numpy as np
import geopandas as gpd

def get_safran_cell_for_each_township (
        external_data
):
    gdf_safran = external_data['safran.gpkg']
    gdf_commune = external_data['geoVec_com2022.json'][['codgeo','geometry']]

    # /!\ Attention geoVec_com2022.json est le fichier geojson utiliser pour DEPHYGraph, trouvé sur datagouv.fr :
    # https://www.data.gouv.fr/fr/datasets/r/fb3580f6-e875-408d-809a-ad22fc418581
    # Contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches
    # epsg : 4326
    # annee : 2022

    # les communes des Droms sont rapprochées de la métropole
    # Les géopositions de leur Polygones ne peuvent pas donc pas être considérées pour les mailles Safran
    # De toute manière les données Safran ne concernent que la métropole !

    df_fin = []

    return gdf_safran

path = '02_outils/data/external_data/geospatial_data/'
get_safran_cell_for_each_township(external_data = (path + 'safran.gpkg'))


def create_donnees_spatiales(
        donnees, 
        external_data
        ):
    
    """
    Permet d'obtenir beaucoup d'informations spatiales pour chaque domaines. 
    
    Echelle : 
        domaine_id 
        On préfère cette échelle à domain_code pour la simplicité de la structure de l'entrepot, la facilitation aux utilisateur. 
        Et, point important, il est possible de changer de commune au cours du temps, la spatialisation est rattaché à l'id pas au code !
    
    Arguments:
        donnees (dict): Contenant les tables suivantes
            - domaine (Contexte, commune_id)
            - commune (Référentiel)
    Retourne:
        pd.DataFrame:
            - 'domaine_id' : Identifiant du domaine
            - 'commune_id' : Identifiant du référentiel de localisation des communes
            - 'code_insee' : le code insee
            - 'safran_cell' : l'identifiant de la cellule safran où se situe le centroide de la commune ; ou la cellule la plus proche. Que pour métropole
            - 'bassin_viticole' : le nom du bassin viticole (création pour DEPHYGraph)
            - + ?

    Notes:
        - 
    """

    # Possible de faire une fonction qui crée qui fait le pont commune safran
    df_domaine = donnees['domaine'][['id','commune_id']]
    df_refgeo = external_data['reflocation']

    df = df_refgeo

    return df