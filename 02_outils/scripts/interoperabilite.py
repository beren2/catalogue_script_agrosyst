"""
	Regroupe les fonctions qui consistent à faire un pont entre une échelle de donnnées Agrosyst et un référentiel (externe préférentiellement)
"""

import pandas as pd
import numpy as np
import geopandas as gpd

def get_safran_cell_for_each_township (
        external_data
):
    # /!\ Attention geoVec_com2022.json est le fichier geojson utiliser pour DEPHYGraph, trouvé sur datagouv.fr :
    # https://www.data.gouv.fr/fr/datasets/r/fb3580f6-e875-408d-809a-ad22fc418581
    # Contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches
    # epsg : 4326
    # annee : 2022
    gdf_commune = external_data['geoVec_com2022'][['codgeo','geometry','dep']].rename(columns={"codgeo": "code_insee"})
    
    #Verification de l'unicité des code insee
    if gdf_commune.code_insee.is_unique : print('index gdf_commune OK') 
    else : print('ATTENTION code_insee ne doit pas servir d\'index à gdf_commune !')


    # Geopackage safran dont la citation est dans le READ ME.txt
    gdf_safran = external_data['safran'][['cell','geometry']].rename(columns={"cell": "cellule_safran"})

    # Verification de l'unicité des cellules safran
    if gdf_safran.cellule_safran.is_unique : print('index gdf_safran OK') 
    else : print('ATTENTION cellule_safran ne doit pas servir d\'index à gdf_safran !')
    

    # Les communes des Droms sont rapprochées de la métropole
    # Les géopositions de leur Polygones ne peuvent pas donc pas être considérées pour les mailles Safran
    # De toute manière les données Safran ne concernent que la métropole !
    gdf_commune = gdf_commune[~(gdf_commune['dep'].str.match(r'97+') | gdf_commune['dep'].str.match(r'98+'))]
    # Créer les centroid des communes. On passe par l'epsg de projection, puis on remet en epsg classique
    gdf_commune = gdf_commune.assign(centroid = gdf_commune.to_crs(3857).centroid.to_crs(4326))


    # Possibilité de check avec la map 'm' si les centroid sont bien centroidés 
    # m = gdf_commune.set_geometry('geometry').explore(name="Polygons")
    # m = gdf_commune.set_geometry('centroid').explore(m=m, color="red", name="Points", marker_type = 'circle')
    # m


    # On joint les données safran aux commune quand le centroid de la commune est à l'intérieur de la maille
    df_spatial = gpd.sjoin(gdf_commune.set_geometry('centroid'), gdf_safran, how='left', predicate='within')
    df_spatial = df_spatial[df_spatial.columns.difference(['dep','index_right'])]
    # 357 communes sans maille rattaché par un within, on fait donc à la maille la plus proche. Besoin de passer en projection
    join = df_spatial.loc[df_spatial.cellule_safran.isna(), ['geometry','centroid']]
    join = gpd.sjoin_nearest(join.to_crs(3857).set_geometry('centroid'), gdf_safran.to_crs(3857), how = 'left', distance_col = "distances").to_crs(4326)
    print('La distance max de jointure par la maille la plus proche est de '+str(np.ceil(join['distances'].max() / 1000).astype(int))+' km')
    # On joint les communes rattachées par nearest avec celles rattachés par within
    df_spatial = df_spatial.combine_first(join[['cellule_safran','distances']])

    # Check et changement cellules safran en int
    if df_spatial['cellule_safran'].isnull().values.any() : 
        print('/!\ ATTENTION des communes ne sont pas rattachées à une maille !')
    else :
        df_spatial['cellule_safran'] = df_spatial['cellule_safran'].astype('Int64')
    
    df_spatial = df_spatial[['code_insee','cellule_safran']]

    return df_spatial


# def create_donnees_spatiales(
#         donnees, 
#         external_data
#         ):
    
#     """
#     Permet d'obtenir beaucoup d'informations spatiales pour chaque domaines. 
    
#     Echelle : 
#         domaine_id 
#         On préfère cette échelle à domain_code pour la simplicité de la structure de l'entrepot, la facilitation aux utilisateur. 
#         Et, point important, il est possible de changer de commune au cours du temps, la spatialisation est rattaché à l'id pas au code !
    
#     Arguments:
#         donnees (dict): Contenant les tables suivantes
#             - domaine (Contexte, commune_id)
#             - commune (Référentiel)
#     Retourne:
#         pd.DataFrame:
#             - 'domaine_id' : Identifiant du domaine
#             - 'commune_id' : Identifiant du référentiel de localisation des communes
#             - 'code_insee' : le code insee
#             - 'safran_cell' : l'identifiant de la cellule safran où se situe le centroide de la commune ; ou la cellule la plus proche. Que pour métropole
#             - 'bassin_viticole' : le nom du bassin viticole (création pour DEPHYGraph)
#             - + ?

#     Notes:
#         - 
#     """

#     # Possible de faire une fonction qui crée qui fait le pont commune safran
#     df_domaine = donnees['domaine'][['id','commune_id']]
#     df_refgeo = external_data['reflocation']

#     df = df_refgeo

#     return df