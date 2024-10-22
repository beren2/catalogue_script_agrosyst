"""
Ce script effectue les tâches suivantes  :
    1) Exécution des scripts de génération des magasins (en se basant sur une copie locale des données)
    2) Enregistrement des résultats dans la base entrepôt (si TYPE == "DISTANT")
"""

import configparser
import pandas as pd
import duckdb
from tqdm import tqdm
import os
from colorama import Fore, Style
import re


#Obtenir les paramètres de connexion pour psycopg2
config = configparser.ConfigParser()
config.read(r'../00_config/config.ini')

DATA_PATH = config.get('metadata', 'data_path') 
TYPE = config.get('metadata', 'type')
df = {}


if(TYPE == 'local'):
    welcome_message = """
        Bienvenue sur l'interface de génération des magasins de données
    """
else :
    welcome_message = """
        Attention, votre configuration est en mode """+TYPE+""" ce qui indique que votre
        copie locale des données pourrait ne pas être à jour (ce script utilise exclusivement 
        les données locales).
    """

def import_df(df_name, path_data, sep, index_col=None):
    """ importe un dataframe df_name dans le dictionnaire global df"""
    if('entrepot_'+df_name not in df.keys()):
        df['entrepot_'+df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep, index_col=index_col, low_memory=False)#,  nrows=LIMIT)

def import_dfs(df_names, path_data, sep = ',', index_col=None, verbose=False):
    """ importe un ensemble de dataframes dans une liste et dont la copie locale se situe au chemin path_data"""
    for df_name in tqdm(df_names) : 
        if(verbose) :
            print(" - ", df_name)
        import_df(df_name, path_data, sep, index_col=index_col)

def check_existing_tables(tables):
    """vérifie que toutes les tables sont présentes"""
    code_error = 0
    for table in tables : 
        file_path = DATA_PATH+table+'.csv'
        if(not os.path.isfile(file_path)):
            print(f"- fichier {Fore.RED}"+file_path+f"{Style.RESET_ALL} manquant") 
            code_error = 1
    return code_error

def import_sql_file(file):
    """
        importe un fichier file et retourne la chaîne de caractère resultante
    """
    with open(file, 'r') as file:
        data = file.read()
    return data

def import_sql_files(tables, path):
    """
        importe tous les scripts SQL au chemin path+table où table est un élément de tables.
        retourne une liste de chaîne de caractère contenant le script à exécuter
    """
    res = []
    for table in tables : 
        res.append(import_sql_file(path+table+'.sql'))
    return res

def preprocess_postgresql_query(query):
    """
    Preprocesses a PostgreSQL query string to replace PostgreSQL-specific functions
    with DuckDB-compatible functions.
    - string_agg(distinct er2.nom, ', ') -> group_concat(distinct er2.nom, ', ')
    - to_char(eis.date_debut, 'DD/MM/YYYY') -> strftime(eis.date_debut, '%d/%m/%Y')
    
    Parameters:
    query (str): Original PostgreSQL query string
    
    Returns:
    str: Preprocessed query string compatible with DuckDB
    """
    # 1. Replace `string_agg(distinct ...)` with `group_concat(distinct ...)`
    query = re.sub(
        r'string_agg\s*\(\s*distinct\s+([a-zA-Z0-9_.]+)\s*,\s*\'([^\']+)\'\s*\)', 
        r"group_concat(distinct \1, '\2')", 
        query, flags=re.IGNORECASE
    )
    
    # 2. Replace `to_char(..., 'DD/MM/YYYY')` with `strftime(..., '%d/%m/%Y')`
    query = re.sub(
        r'to_char\s*\(\s*([a-zA-Z0-9_.]+)\s*,\s*\'DD/MM/YYYY\'\s*\)', 
        r"strftime(CAST(\1 AS DATE), '%d/%m/%Y')", 
        query, flags=re.IGNORECASE
    )
    return query

def preprocess_postgresql_queries(queries):
    """transforme une liste de requêtes PostgreSQL compatibles vers des fonctions SQLITE compatibles"""
    res = []
    for query in queries:
        res.append(preprocess_postgresql_query(query))
    return res

dependance_specs = {
    'context_performance_sdc' : {
        'tables' : [
            'action_realise', 
            'utilisation_intrant_realise_agrege', 
            'action_realise_manquant_agrege',
            'sdc', 'dispositif', 'liaison_sdc_reseau',
            'liaison_reseaux', 'reseau'
        ]
    }
}




magasin_specs  = {
    'magasin_can' : {
        'tables' : {
            'assolee_synthetise' : {
                'dependances' : [
                ],
                'tables' : [
                ]
            },
            'atelier_elevage' : {
                'dependances' : [
                    'context_performance_sdc'
                ],
                'tables' : [
                    'atelier_elevage', 'domaine', 
                    'domaine_filtres_outils_can'
                ]
            },
            'intervention_realise_performance' : {
                'tables' : [
                     'intervention_realise_performance', 
                     'intervention_realise', 'intervention_realise_performance', 
                     'intervention_realise_outils_can', 
                     'intervention_realise_agrege', 
                     'zone', 
                     'parcelle', 
                     'noeuds_realise', 
                     'culture',
                     'culture_outils_can',
                     'plantation_perenne_phases_realise',
                     'plantation_perenne_realise', 
                     'domaine',
                     
                ],
                'dependances':[
                    'context_performance_sdc'
                ]
            }
        }, 
        'path' : 'can/scripts/'
    },
    'means' : {

    }
}

options = {
    "Tout générer" : [],
    "Générer un magasin" : [],
    "Quitter" : []
}

donnees = {}
while True:
    print("")
    print("")
    print(welcome_message)
    print("")
    print("")
    print("Veuillez choisir une option parmi les suivantes :")
    print("")
    for i, option in enumerate(options.keys()):
        print(f"{i + 1}. {option}")
    
    choice = int(input("Entrez votre choix (1, 2 ...) : "))
    choice_key = list(options.keys())[choice - 1]
    print(choice_key)

    if(choice_key == "Générer un magasin"):

        # On demande le magasin à générer
        magasins = list(magasin_specs.keys())
        print("")
        print("Veuillez choisir le magasin à générer")
        print("")
        for i, option_magasin in enumerate(magasins):
                    print(f"{i + 1}. {option_magasin}")
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_magasin = magasins[choice - 1]
        #print("magasin choisi : ", choosen_magasin)

        # On demande la table dans ce magasin à générer (ou toutes)
        tables = ['tout']
        tables += list(magasin_specs[choosen_magasin]['tables'].keys())
        print("")
        print("Veuillez choisir la table à générer")
        print("")
        for i, option_table in enumerate(tables):
                    print(f"{i + 1}. {option_table}")
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_table = tables[choice - 1]
        if(choosen_table == 'tout') :
            print("Début génération de toute les tables du magasin "+choosen_magasin)
            print("Cette action n'est pas encore disponible...")
        else :
            # récupération des tables utiles pour la génération 
            tables_utiles = magasin_specs[choosen_magasin]['tables'][choosen_table]['tables']
            
            # récupération des scripts à exécuter préalablement
            dependances = magasin_specs[choosen_magasin]['tables'][choosen_table]['dependances']
            tables_dependance = []
            for dependance in dependances:
                tables_dependance += dependance_specs[dependance]['tables']
            
            # récapitulatif des tables à importer
            tables_to_import = list(set(tables_dependance+tables_utiles))
            
            # vérification que l'utilisateur a bien tous les dataframes indiqués
            error = check_existing_tables(tables_to_import)
            if(error == 1):
                # pas la peine d'aller plus loin 
                break

            # récupération des scripts SQL
            queries = import_sql_files([choosen_table], magasin_specs[choosen_magasin]['path'])   
            dependance_queries = import_sql_files(dependances, magasin_specs[choosen_magasin]['path']+'dependances/')

            # preprocess des scripts SQL : 
            queries = preprocess_postgresql_queries(queries)
            dependance_queries = preprocess_postgresql_queries(dependance_queries)

            # import de toutes les données utiles dans le dictionnaire
            print("Début de l'import des données nécessaires")
            import_dfs(tables_to_import, DATA_PATH, sep = ',', verbose=False) 
            print("Fin de l'import des données nécessaires")

            # conversion du dictionnaire en variable pour duckdb
            for key, df_value in df.items():
                globals()[key] = df_value  # Assign each dataframe to a variable with the name of the key  
            
            print("Début de l'exécution des scripts SQL")

            # Requêtes de dépendance à exécuter préalablement
            for i, dependance_query in enumerate(dependance_queries):  
                res1 = duckdb.sql(dependance_query)

            # Requêtes principales
            for i, query in enumerate(queries):  
                file_name = DATA_PATH+""+choosen_table+"_"+choosen_magasin+".csv"
                res = duckdb.sql(query)
                res.to_csv(file_name)
                print(f"- fichier {Fore.GREEN}"+file_name+f"{Style.RESET_ALL} exporté") 
            print("Fin de l'exécution des scripts SQL")





            
            
            