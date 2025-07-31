"""
	Regroupe les fonctions qui consistent à faire un pont entre une échelle de donnnées Agrosyst et un référentiel (externe préférentiellement)
"""

import pandas as pd
import numpy as np
import geopandas as gpd

def make_spatial_interoperation_btw_codeinsee_and_spatial_id(donnees):
    """
    Permet d'obtenir la correspondance spatiale entre une commune et une maille safran
    Pour le bind la règle est la suivante : 
        1 - le centroide de la commune est inclu dans la maille safran
        2 - si le centroide n'est inclu dans aucune maille, on va chercher la maille la plus proche (1er essai la distance max de rattachement était de 46km)
    QUE POUR LA METROPOLE FRANçAISE

    Permet aussi d'obtenir la correspondance spatiale entre une commune et un site du projet RMQS (GIS Sol)
    Pour le bind la règle est la suivante : 
        le site RMQS (point) le plus proche du centroide de la commune
    QUE POUR LA METROPOLE FRANçAISE

    Arguments:
        donnees (dict): 
            Contenant les fichiers suivants provenant des external_data :
                - geoVec_com2024.json : fichier des contour de communes 2024 en epsg 4326
                - safran.gpkg : geopackage safran télécharger sur le site de SICLIMA
                - geoVec_rmqs.json : geojson des identifiants des sites du projet RMQS (2 campagnes distinctes)

    Retourne:
        pd.DataFrame:
            - 'codeinsee' : le code insee de la commune
            - 'safran_cell_id' : l'identifiant de la cellule safran où se situe la commune
            - 'rmqs_site_id' = identifiant du site RMS le plus proche du centroide de la commune métropolitaine
            - 'rmqs_date_sampl' = date d'échantillonnage sur le site RMQS en question (attention 2 campagnes distinctes)
            - 'rmqs_dist_site' = distances entre le centroide de la commune métropolitaine la plus proche du site RMQS indiqué et le point du site RMQS indiqué

    Notes:
        Cette fonction n'est qu'un intermédiaire pour arrivé à une sortie attendue principalement pour
        la fonction get_donnees_spatiales_from_domain_township. Un futur dévellopement à penser pour stocker ces fichiers intermédiaires qui ne seront à refaire 
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
    gdf_commune = donnees['geoVec_com2024'][['code','geometry','departement']].\
        rename(columns={"code": "codeinsee",
                        'departement': 'dep'})

    #Verification de l'unicité des code insee
    if gdf_commune.codeinsee.is_unique : print('index gdf_commune OK') 
    else : print('ATTENTION codeinsee ne doit pas servir d\'index à gdf_commune !')


    # Geopackage safran dont la citation est dans le READ ME.txt
    gdf_safran = donnees['safran'][['cell','geometry']].rename(columns={"cell": "safran_cell_id"})

    # Verification de l'unicité des cellules safran
    if gdf_safran.safran_cell_id.is_unique : print('index gdf_safran OK') 
    else : print('ATTENTION safran_cell_id ne doit pas servir d\'index à gdf_safran !')
    
    # geojson des sites RMQS (GIS Sol : https://entrepot.recherche.data.gouv.fr/dataverse/info_et_sols?q=&types=dataverses%3Adatasets&sort=dateSort&order=desc&page=3)
    gdf_rmqs = donnees['geoVec_rmqs']

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
    join = df_spatial.loc[df_spatial.safran_cell_id.isna(), ['geometry','centroid']]
    join = gpd.sjoin_nearest(join.to_crs(3857).set_geometry('centroid'), gdf_safran.to_crs(3857), how = 'left', distance_col = "safran_dist").to_crs(4326)
    print('La distance max de jointure par la maille la plus proche est de '+str(np.ceil(join['safran_dist'].max() / 1000).astype(int))+' km')
    # On joint les communes rattachées par nearest avec celles rattachés par within
    df_spatial = df_spatial.combine_first(join[['safran_cell_id','safran_dist']])
    df_spatial['safran_dist'] = round(df_spatial['safran_dist']/1000, 0)

    df_spatial = gpd.sjoin_nearest(df_spatial.to_crs(3857), gdf_rmqs.set_index('id').to_crs(3857), distance_col="distances_rmqs", how='left').set_index('codeinsee')

    df_spatial['id_site'] = np.where(pd.isna(df_spatial['id_site']),df_spatial['id_site'],df_spatial['id_site'].astype(str))

    df_spatial['distances_rmqs'] = np.where(pd.isna(df_spatial['distances_rmqs']),df_spatial['distances_rmqs'],round(df_spatial['distances_rmqs']/1000,0).astype('Int64'))

    df_spatial = df_spatial.rename(columns={
        'id_site' : 'rmqs_site_id',
        'sampling_date' : 'rmqs_date_sampl',
        'distances_rmqs' : 'rmqs_dist_site'
    })


    # Check et changement cellules safran en int puis de nouveau en str
    if df_spatial['safran_cell_id'].isnull().values.any() : 
        print('!!! ATTENTION des communes ne sont pas rattachées à une maille !!!')
    else :
        df_spatial['safran_cell_id'] = df_spatial['safran_cell_id'].astype('Int64').astype('str')
    
    # On ne check pas les sites RMQS car on a pas mis de max distances et surtout certains site n'ont pas de coordonnées !
    
    # # Map explore() permettant de voir les communes non rattachés par within pour comprendre leur distances par rapport aux mailles
    # m2 = df_spatial.loc[df_spatial.distances.notnull()].set_geometry('geometry').explore(name="Polygons")
    # m2 = df_spatial.loc[df_spatial.distances.notnull()].set_geometry('centroid').explore(m=m2, color="red", name="Points", marker_type = 'circle')
    # m2 = gdf_safran.explore(m=m2, name="Polygons safran", color="grey")

    df_spatial = df_spatial[['safran_cell_id','safran_dist','rmqs_site_id','rmqs_date_sampl','rmqs_dist_site']].reset_index()

    # return m
    # return m2
    return df_spatial


def get_donnees_spatiales_commune_du_domaine(donnees):
    
    """
    Permet d'obtenir des informations spatiales pour chaque domaines.
    
    Echelle : 
        domaine_id : 
            On préfère cette échelle à domain_code pour la simplicité de la structure de l'entrepot, la facilitation aux utilisateur. 
            Et, point important, il est possible de changer de commune au cours du temps, la spatialisation est rattaché à l'id pas au code !
    
    Arguments:
        donnees (dict): 
            Contenant les tables suivantes de l'entrepot
                - domaine : (entrepot.Contexte => commune_id)
                - commune : (entrepot.Référentiel => codeinsee)
            Contient aussi les données dont a besoin la fonction make_spatial_interoperation_btw_codeinsee_and_spatial_id()
                - geoVec_com2024 : fichier des contour de communes 2024 en epsg 4326. JSON
                - safran : geopackage safran téléchargé sur le site de SICLIMA. GPKG
                - geoVec_rmqs : geojson des identifiants des sites du projet RMQS (2 campagnes distinctes). JSON
                - geofla : référentiel avec un code insee (2024) et une liste d'identifiant geofla (2015)
                - ruralite : référentiel avec un code insee (2024) et une typologie de ruralité (0 à 9). Si le codeinsee date de 2024, le dvlpmt des typologies de ruralité a été mené par le DATAR en 2003 et 2011.

    Retourne:
        pd.DataFrame:
            - 'domaine_id' : Identifiant du domaine
            - 'domaine_code' : Code du domaine
            - 'commune_id' : Identifiant du référentiel de localisation des communes
            - 'codeinsee' : le code insee
            - 'safran_cell_id' : l'identifiant de la cellule safran où se situe le centroide de la commune ; ou la cellule la plus proche. Que pour métropole
            - 'rmqs_site_id' = identifiant du site RMS le plus proche du centroide de la commune métropolitaine
            - 'rmqs_date_sampl' = date d'échantillonnage sur le site RMQS en question (attention 2 campagnes distinctes)
            - 'rmqs_dist_site' = distances entre le centroide de la commune métropolitaine la plus proche du site RMQS indiqué et le point du site RMQS indiqué
            - 'geofla_2015_id' = liste d'identifiant geofla pour chaque code insee. Attention geofla est obsolete !
            - 'typo_ruralite" = typologie de ruralité de la commune (0 à 9)

    Notes:
        make_spatial_interoperation_btw_codeinsee_and_spatial_id() est une fonction permettant de générer un Dataframe qui donne le rattachement commune/maille safran/site RMQS
        on la fait tourner pour obtenir la maille safran en mergeant par le code insee. Possible qu'un jour on ne lui fasse plus appel mais qu'on
        importe sa sortie comme n'importe quel Df
    """

    # import et renommage
    df_domaine = donnees['domaine'][['id','code','commune_id']].rename(columns={
        'id' : 'domaine_id',
        'code' : 'domaine_code'
        }).copy()
    df_commune = donnees['commune'][['id','codeinsee']].rename(columns={
        'id' : 'commune_id'
        }).copy()
    df_geofla = donnees['geofla'].copy()
    df_typoruralite = donnees['ruralite'][['codeinsee','typo_ruralite']].copy()

    df_spatial = make_spatial_interoperation_btw_codeinsee_and_spatial_id(
        donnees
    )

    # Passer les codeinsee en str pour toutes les tables, surtout à cause des None lors du mode DEBUG
    df_commune['codeinsee'] = df_commune['codeinsee'].astype(str)
    df_spatial['codeinsee'] = df_spatial['codeinsee'].astype(str)
    df_geofla['codeinsee'] = df_geofla['codeinsee'].astype(str)
    df_typoruralite['codeinsee'] = df_typoruralite['codeinsee'].astype(str)

    # Merge
    df = df_domaine.merge(df_commune, on = 'commune_id', how='left')
    df = df.merge(df_spatial, on = 'codeinsee', how='left')
    df = df.merge(df_geofla, on = 'codeinsee', how='left')
    df = df.merge(df_typoruralite, on = 'codeinsee', how='left')
    # 0 ==> Hors champ : DOM ou commune urbaine
    # 1 ==> Les petites polarités industrielles et artisanales
    # 2 ==> Les petites polarités mixtes
    # 3 ==> Les ruralités productives agricoles
    # 4 ==> Les ruralités productives ouvrières
    # 5 ==> Les ruralités résidentielles aisées
    # 6 ==> Les ruralités résidentielles mixtes
    # 7 ==> Les ruralités touristiques à dominante résidentielles
    # 8 ==> Les ruralités touristiques spécialisées
    # 9 ==> Communes ayant changé de périmètre depuis la réalisation de la typologie


    # On drop les duplicats d'identiafiants de points GPS car il peut arriver qu'un point GPS matches avec plusieurs site RMQS par exemple lorsque deux points RMQS sont à même distance du centre du point GPS. Il est possible que ce soit 2 fois le même site RMQS (donc les même coordonnées GPS) mais avec un identifiant différent et des dates de sampling différentes.
    # Du coup on drop les duplicats en gardant le premier
    df = df.drop_duplicates(subset=['domaine_id'], keep='first')

    df = df.set_index('domaine_id')

    return df



def get_donnees_spatiales_coord_gps_du_domaine(donnees):
    
    """
    Permet d'obtenir des informations spatiales pour chaque coordonnées gps saisies au niveau du domaine
    
    Echelle : 
        geopoint_id : 
            Au niveau du domaine on peut saisir plusieurs points gps et les nommés (par exemple 'Siege', 'Hangar', ...).
            Les points gps des parcelles seront saisie plutot au niveau de la zone en réalisé.
    
    Arguments:
        donnees (dict) : Contenant les tables suivantes provenant de l'netrepot mais aussi des données externes geospatiales
            - coordonnees_gps_domaine (entrepot.Contexte => domain_id, latitude, longitude)
            - geoVec_com2024 : fichier des contour de communes 2024 en epsg 4326. JSON
            - safran : geopackage safran téléchargé sur le site de SICLIMA. GPKG
            - geoVec_rmqs : geojson des identifiants des sites du projet RMQS (2 campagnes distinctes). JSON

    Retourne:
        pd.DataFrame:
            - 'geopoint_id' : Identifiant du point gps
            - 'domaine_id' : Identifiant du domaine
            - 'safran_cell_id' : l'identifiant de la cellule safran où se situe le point GPS. Que pour métropole
            - 'rmqs_site_id' = identifiant du site RMS le plus proche du cpoint GPS. Que pour métropole
            - 'rmqs_date_sampl' = date d'échantillonnage sur le site RMQS en question (attention 2 campagnes distinctes)
            - 'rmqs_dist_site' = distances entre le point GPS le plus proche du site RMQS indiqué et le point du site RMQS indiqué
     """
    
    # import et renommage
    gdf_gps = donnees['coordonnees_gps_domaine'][['id','domaine_id','latitude','longitude']].rename(columns={"id": "geopoint_id"}).copy()
    gdf_gps = gpd.GeoDataFrame(gdf_gps,
                               geometry = gpd.points_from_xy(
                                   x = gdf_gps.longitude,
                                   y = gdf_gps.latitude,
                                   crs = 'EPSG:4326')
                                ).drop(columns=['latitude', 'longitude'])
    
    gdf_safran = donnees['safran'][['cell','geometry']].rename(columns={"cell": "safran_cell_id"}).copy()
    gdf_safran['safran_cell_id'] = gdf_safran['safran_cell_id'].astype(str)
    gdf_rmqs = donnees['geoVec_rmqs'].copy()
    gdf_rmqs['id_site'] = gdf_rmqs['id_site'].astype(str)

    # On joint la cellule safran si les coord gps du domaine sont à l'intérieur de la cell
    df_coord_gps = gpd.sjoin(gdf_gps.set_geometry('geometry'), gdf_safran, how='left', predicate='within').drop(columns='index_right')
    
    # Si pas le cas on va chercher la cell la plus proche.
    # On pose un distance pax d'appariement de 80km (au jugé, = x10 mailles)
    join = df_coord_gps.loc[df_coord_gps.safran_cell_id.isna(), ['geopoint_id','geometry']]
    join = gpd.sjoin_nearest(join.to_crs(3857).set_geometry('geometry'), gdf_safran.to_crs(3857).set_geometry('geometry'), how = 'left', max_distance = 80000).to_crs(4326).drop(columns='index_right')
    # On joint les communes rattachées par nearest avec celles rattachés par within
    df_coord_gps = df_coord_gps.combine_first(join[['safran_cell_id']])

    # RMQS
    df_coord_gps = gpd.sjoin_nearest(df_coord_gps.to_crs(3857), gdf_rmqs.to_crs(3857), distance_col="distances_rmqs", how='left', max_distance = 80000).drop(columns = ['id','index_right'])

    df_coord_gps['id_site'] = np.where(pd.isna(df_coord_gps['id_site']),df_coord_gps['id_site'],df_coord_gps['id_site'].astype(str))

    df_coord_gps['distances_rmqs'] = np.where(pd.isna(df_coord_gps['distances_rmqs']), np.nan, round(df_coord_gps['distances_rmqs']/1000,0).astype(int, errors='ignore'))

    df_coord_gps = df_coord_gps.rename(columns={
        'id_site' : 'rmqs_site_id',
        'sampling_date' : 'rmqs_date_sampl',
        'distances_rmqs' : 'rmqs_dist_site'
    })
    df_coord_gps = df_coord_gps.to_crs(4326)

    # GEOFLA
    # df_coord_gps = df_coord_gps.merge(df_geofla, on = 'codeinsee', how='left')
    # imposssible de faire Geofla car reviendrai à faire ce qui est fait pour commune, en effet on a qu'un référentiel codeinsee-geofla_id. Alors que pour faire selon un point GPS on devrait avoir un fichier geojson (ou vectorisé) qui pointe vers un geofla-id.


    df = df_coord_gps[['geopoint_id','domaine_id','geometry','safran_cell_id','rmqs_site_id','rmqs_date_sampl','rmqs_dist_site']]\
        .rename(columns={"geometry": "coord_gps"})
    
    df.loc[df['coord_gps'].apply(lambda p: np.isinf(p.x) or np.isinf(p.y)), 'coord_gps'] = np.nan
    df['coord_gps'] = df['coord_gps'].apply(lambda geom: geom.wkt if geom else np.nan)
    df = pd.DataFrame(df)


    # On drop les duplicats d'identiafiants de points GPS car il peut arriver qu'un point GPS matches avec plusieurs site RMQS par exemple lorsque deux points RMQS sont à même distance du centre du point GPS. Il est possible que ce soit 2 fois le même site RMQS (donc les même coordonnées GPS) mais avec un identifiant différent et des dates de sampling différentes.
    # Du coup on drop les duplicats en gardant le premier
    df = df.drop_duplicates(subset=['geopoint_id'], keep='first')

    df = df.set_index('geopoint_id')

    return df