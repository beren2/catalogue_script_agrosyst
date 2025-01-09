"""
	Regroupe les fonctions qui consistent à faire un pont entre une échelle de donnnées Agrosyst et un référentiel (externe préférentiellement)
"""

import pandas as pd
import numpy as np
import geopandas as gpd

def get_safran_cell_for_each_township(donnees):
    """
    Permet d'obtenir la correspondance spatiale entre une commune et une maille safran
    Pour le bind la règle est la suivante : 
        1 - le centroide de la commune est inclu dans la maille safran
        2 - si le centroide n'est inclu dans aucune maille, on va chercher la maille la plus proche (1er essai la distance max de rattachement était de 46km)
    QUE POUR LA METROPOLE FRANçAISE

    Arguments:
        donnees (dict): 
            Contenant les fichiers suivants provenant des external_data :
                - geoVec_com2024.json : fichier des contour de communes 2024 en epsg 4326
                - safran.gpkg : geopackage safran télécharger sur le site de SICLIMA

    Retourne:
        pd.DataFrame:
            - 'codeinsee' : le code insee de la commune
            - 'cellule_safran' : l'identifiant de la cellule safran où se situe la commune (voir règles plus haut)

    Notes:
        Cette fonction met environ 3 secondes à tourner. Elle n'est qu'un intermédiaire pour arrivé à une sortie attendue principalement pour
        la fonction create_donnees_spatiales. Un futur dévellopement à penser pour stocker ces fichiers intermédiaires qui ne seront à refaire 
        tourner qu'une fois tout les an, voire plus (au changement des contour de communes, chgt de codeinsee, chgt d'id maille safran)
        Pour l'instant on choisit de faire tourner cette fonction à chaque fois (que 3s !)
    """

    # /!\ Attention geoVec_com2022.json est le fichier geojson utiliser pour DEPHYGraph, trouvé sur datagouv.fr :
    # https://www.data.gouv.fr/fr/datasets/r/fb3580f6-e875-408d-809a-ad22fc418581
    # Contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches
    # epsg : 4326
    # annee : 2022

    # Celui utilisé ici est celui de 2024 avec DROMS NON RAPPORCHES trouvé sur BAN Open data !!
    # https://adresse.data.gouv.fr/data/contours-administratifs/2024/geojson
    gdf_commune = donnees['geoVec_com2024'][['codgeo','geometry','dep']].rename(columns={"codgeo": "codeinsee"})

    #Verification de l'unicité des code insee
    if gdf_commune.codeinsee.is_unique : print('index gdf_commune OK') 
    else : print('ATTENTION codeinsee ne doit pas servir d\'index à gdf_commune !')


    # Geopackage safran dont la citation est dans le READ ME.txt
    gdf_safran = donnees['safran'][['cell','geometry']].rename(columns={"cell": "cellule_safran"})

    # Verification de l'unicité des cellules safran
    if gdf_safran.cellule_safran.is_unique : print('index gdf_safran OK') 
    else : print('ATTENTION cellule_safran ne doit pas servir d\'index à gdf_safran !')
    

    # Les géopositions des communes d'outre mer (DROMs) ne sont pas à considérés car pas dans SAFRAN
    gdf_commune = gdf_commune[~(gdf_commune['dep'].str.match(r'97+') | gdf_commune['dep'].str.match(r'98+'))]
    # Créer les centroid des communes. On passe par l'epsg de projection, puis on remet en epsg classique
    gdf_commune = gdf_commune.assign(centroid = gdf_commune.to_crs(3857).centroid.to_crs(4326))

    # # Possibilité de check avec la map 'm' si les centroid des communes sont bien centroidés 
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
    
    # # Map explore() permettant de voir les communes non rattachés par within pour comprendre leur distances par rapport aux mailles
    # m2 = df_spatial.loc[df_spatial.distances.notnull()].set_geometry('geometry').explore(name="Polygons")
    # m2 = df_spatial.loc[df_spatial.distances.notnull()].set_geometry('centroid').explore(m=m2, color="red", name="Points", marker_type = 'circle')
    # m2 = gdf_safran.explore(m=m2, name="Polygons safran", color="grey")

    df_spatial = df_spatial[['codeinsee','cellule_safran']]

    # return m
    # return m2
    return df_spatial


def create_donnees_spatiales(donnees, get_safran_cell_for_each_township_data):
    
    """
    Permet d'obtenir des informations spatiales pour chaque domaines.
    
    Echelle : 
        domaine_id : 
            On préfère cette échelle à domain_code pour la simplicité de la structure de l'entrepot, la facilitation aux utilisateur. 
            Et, point important, il est possible de changer de commune au cours du temps, la spatialisation est rattaché à l'id pas au code !
    
    Arguments:
        donnees (dict): Contenant les tables suivantes
            - domaine (entrepot.Contexte => commune_id)
            - commune (entrepot.Référentiel => codeinsee)
            - coordonnees_gps_domaine (entrepot.Contexte => latitude, longitude)
        external_data (dict): Contient les données dont a besoin la fonction get_safran_cell_for_each_township()
            - geoVec_com2024.json : fichier des contour de communes 2024 en epsg 4326
            - safran.gpkg : geopackage safran télécharger sur le site de SICLIMA

    Retourne:
        pd.DataFrame:
            - 'domaine_id' : Identifiant du domaine
            - 'commune_id' : Identifiant du référentiel de localisation des communes
            - 'codeinsee' : le code insee
            - 'cellule_safran' : l'identifiant de la cellule safran où se situe le centroide de la commune ; ou la cellule la plus proche. Que pour métropole

    Notes:
        get_safran_cell_for_each_township() est une fonction permettant de générer un Dataframe qui donne le rattachement commune/maille safran
        on la fait tourner pour obtenir la maille safran en mergeant par le code insee. Possible qu'un jour on ne lui fasse plus appel mais qu'on
        importe sa sortie comme n'importe quel Df
    """
    # import et renommage
    df_domaine = donnees['domaine'][['id','code','commune_id']].rename(columns={
        'id' : 'domaine_id',
        'code' : 'domaine_code'
        })
    df_commune = donnees['commune'][['id','codeinsee']].rename(columns={
        'id' : 'commune_id'
        })
    # On crée deux geodf un avec safran et un avec les coord gps des domaines
    gdf_gps = donnees['coordonnees_gps_domaine'][['domaine_id','latitude','longitude']]
    gdf_gps = gpd.GeoDataFrame(gdf_gps,
                               geometry = gpd.points_from_xy(
                                   x = gdf_gps.longitude,
                                   y = gdf_gps.latitude,
                                   crs = 'EPSG:4326')
                                ).drop(columns=['latitude', 'longitude'])
    gdf_safran = get_safran_cell_for_each_township_data['safran'][['cell','geometry']].rename(columns={"cell": "cellule_safran"})

    # On joint la cellule safran si les coord gps du domaine sont à l'intérieur de la cell
    df_coord_gps = gpd.sjoin(gdf_gps.set_geometry('geometry'), gdf_safran, how='left', predicate='within')
    # Si pas le cas on va chercher la cell la plus proche.
    # On pose un distance pax d'appariement de 70km (au jugé)
    join = df_coord_gps.loc[df_coord_gps.cellule_safran.isna(), ['geometry']]
    join = gpd.sjoin_nearest(join.to_crs(3857).set_geometry('geometry'), gdf_safran.to_crs(3857).set_geometry('geometry'), how = 'left', max_distance = 70000).to_crs(4326)
    # On joint les communes rattachées par nearest avec celles rattachés par within
    df_coord_gps = df_coord_gps.combine_first(join[['cellule_safran']])
    df_coord_gps = df_coord_gps[['domaine_id','cellule_safran']]

    if df_coord_gps.duplicated('domaine_id').shape[0] != 0:
        return print('/!\ ATTENTION pluseiurs coordonnées gps renseignés pour un même domaine !'), df_coord_gps.duplicated('domaine_id', keep=False)

    df_spatial = get_safran_cell_for_each_township(get_safran_cell_for_each_township_data)

    # merge
    df = df_domaine.merge(df_commune, on = 'commune_id', how='left')
    df = df.merge(df_coord_gps, on = 'domaine_id', how='left')
    df = df.merge(df_spatial, on = 'codeinsee', how='left')

    df['cellule_safran'] = df['cellule_safran_x'].fillna(df['cellule_safran_y'])
    df = df.drop(['cellule_safran_x', 'cellule_safran_y'], axis=1)

    return df