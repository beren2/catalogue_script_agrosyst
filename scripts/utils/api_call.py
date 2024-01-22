"""
    Ce script contient les fonctions utiles pour l'appel à l'api Datagrosyst : 
    (obtention des métadonnées de l'entrepôt, mise à jour des données...)
"""
import json
from datetime import datetime, date
from io import StringIO
import os
import configparser
from requests.auth import HTTPBasicAuth
import requests
import pandas as pd


# Obtention des données de configurations pour l'API et la mise à jour des données
config = configparser.ConfigParser()
config.read(r'config/datagrosyst.ini')

# Informations générales pour l'API 
URL = config.get('api_info', 'url')
LAST_UPDATE_DATE_FILE = config.get('api_info', 'last_update_date_file')

# Informations d'authentification pour l'API
DATAGROSYST_MAIL = config.get('api_info', 'mail')
DATAGROSYST_PASSWORD = config.get('api_info', 'password')
BASIC = HTTPBasicAuth(DATAGROSYST_MAIL, DATAGROSYST_PASSWORD)
TIMEOUT = 100

def get_metadata(metadata_name):
    """ 
        Chargement de la dernière date d'actualisation des exports personnalisés
    """
    end_point = URL+'metadata/'+metadata_name
    r = requests.get(end_point, timeout=TIMEOUT)  
    return json.loads(r.content)

def get_table_names():
    """
        Obtenir le nom de toutes les tables de l'entrepôt de données
    """
    end_point = URL+'table_name/'
    r = requests.get(end_point, timeout=TIMEOUT)  
    return json.loads(r.content)

def download_df(df_name, verbose=False):
    """ 
        Chargement d'une table dans un dataframe par appel à l'api
    """
    if(verbose):
        print("- "+df_name)
    end_point = URL+'table_zip/'+df_name
    r = requests.get(end_point, auth=BASIC, timeout=TIMEOUT)  
    return pd.read_csv(StringIO(r.text), sep=',')

def download_dfs(df_names, data_path_out='./data/', verbose=False):
    """ 
        Chargement d'un ensemble de tables par appel à l'api 
    """
    for df_name in df_names :
        df = download_df(df_name, verbose=verbose)
        df.to_csv(data_path_out+df_name+".csv")

def load_df(df_name, data_path_in, verbose=False):
    """ 
        Chargement d'une table locale dans un dataframe 
    """
    if(verbose):
        print("- "+df_name)
    return pd.read_csv(data_path_in+df_name+'.csv', sep=',', index_col=0)

def loads_dfs(df_names, data_path_in='./data/', verbose=False):
    """ 
        Chargement d'un ensemble de tables locales dans un dictionnaire
    """
    dfs = {}
    for df_name in df_names :
        dfs[df_name] = load_df(df_name, data_path_in, verbose=verbose)
    return dfs


def refresh_last_data(data_path):
    """
        Permet de mettre à jour les données du répertoire si un export + récent s'y trouve
    """
    # récupération de la date des exports disponibles sur Datagrosyst
    current_export_date = datetime.strptime(get_metadata('date_current_export')['value'], "%Y-%m-%d")
    need_refresh = True
    if os.path.isfile(LAST_UPDATE_DATE_FILE):
        # le fichier de dernier import existe
        with open(LAST_UPDATE_DATE_FILE, "r", encoding="utf8") as file:
            last_import_date = datetime.strptime(file.read().splitlines()[0], "%Y-%m-%d")
    
        if(last_import_date >= current_export_date):
            # il y a eu une nouvelle version d'exports depuis la dernière mise à jour des données locales
            need_refresh = False

    if(need_refresh) : 
        print("Nouvelle version des données disponibles sur Datagrosyst !")
        
        # téléchargement des données
        print("Téléchargement [peut prendre plusieurs dizaines de minutes]...")
        df_names = get_table_names()
        download_dfs(df_names, data_path_out=data_path, verbose=True)
        print("Téléchargement terminé !")

        # mise à jour des données locales : aujourd'hui
        with open(LAST_UPDATE_DATE_FILE, "w+", encoding="utf8") as file:
            file.write(str(date.today()))
    else :
        print("Vos données sont à jour !")
