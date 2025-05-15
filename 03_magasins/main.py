"""
Ce script effectue les tâches suivantes  :
    1) Exécution des scripts de génération des magasins (en se basant sur une copie locale des données)
    2) Enregistrement des résultats dans la base entrepôt (si TYPE == "DISTANT")
"""
import os
import re
import json
import configparser
import pandas as pd
import duckdb
from tqdm import tqdm
from colorama import Fore, Style
from version import __version__

#Obtenir les paramètres de connexion pour psycopg2
config = configparser.ConfigParser()
config.read(r'../00_config/config.ini')

DATA_PATH = config.get('metadata', 'data_path') 
TYPE = config.get('metadata', 'type')
DEBUG = bool(int(config.get('metadata', 'debug')))
VERBOSE = DEBUG
VERSION = __version__
with open('../00_config/specs.json', encoding='utf8') as json_file:
    SOURCE_SPECS = json.load(json_file)

if(DEBUG):
    NROWS = int(config.get('debug', 'nrows'))
    DATA_PATH = config.get('debug', 'data_test_path')

df = {}


def check_existing_files(file_names):
    """vérifie que les fichiers sont présent et les créé au besoin."""
    code_error = 0
    for file_name in file_names : 
        file_path = DATA_PATH+file_name+'.txt'
        if(not os.path.isfile(file_path)):
            with open(file_path,'w', encoding='utf-8') as version_file:
                json.dump({}, version_file)
            return 0 
    return code_error

check_existing_files(['version'])

def update_local_version_table(table_name):
    """
        Met à jour la version de la table table_name dans le version.txt des données
    """
    # lecture du fichier
    with open(DATA_PATH+'version.txt', encoding='utf-8') as version_file:
        version_control = json.load(version_file)
        version_control[table_name] = VERSION

    # ecriture du fichier
    with open(DATA_PATH+'version.txt','w', encoding='utf-8') as version_file:
        print("UPDATE")
        json.dump(version_control, version_file)
    return 0

def import_df(df_name, path_data, sep, index_col=None):
    """ importe un dataframe df_name dans le dictionnaire global df"""
    if('entrepot_'+df_name not in df):
        if(DEBUG):
            df['entrepot_'+df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep, index_col=index_col, low_memory=False,  nrows=NROWS).replace({'\r\n': '\n'}, regex=True)
        else:
            df['entrepot_'+df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep, index_col=index_col, low_memory=False).replace({'\r\n': '\n'}, regex=True)

def import_dfs(df_names, path_data, sep = ',', index_col=None, verbose=False):
    """ importe un ensemble de dataframes dans une liste et dont la copie locale se situe au chemin path_data"""
    for df_name in tqdm(df_names) : 
        if(verbose) :
            print(" - ", df_name)
        import_df(df_name, path_data, sep, index_col=index_col)

def check_existing_tables(desired_tables):
    """vérifie que toutes les tables sont présentes"""
    code_error = 0
    for desired_table in desired_tables : 
        file_path = DATA_PATH+desired_table+'.csv'
        if(not os.path.isfile(file_path)):
            print(f"- fichier {Fore.RED}"+file_path+f"{Style.RESET_ALL} manquant") 
            code_error = 1
    return code_error

def import_sql_file(file):
    """
        importe un fichier file et retourne la chaîne de caractère resultante
    """
    with open(file, 'r',  encoding="utf-8") as f:
        data = f.read()
    return data

def import_sql_files(desired_tables, path):
    """
        importe tous les scripts SQL au chemin path+table où table est un élément de tables.
        retourne une liste de chaîne de caractère contenant le script à exécuter
    """
    res = []
    for desired_table in desired_tables : 
        res.append(import_sql_file(path+desired_table+'.sql'))
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

    # 2. Replace `to_char(..., 'DD/MM')` with `strftime(..., '%d/%m')`
    query = re.sub(
        r'to_char\s*\(\s*([a-zA-Z0-9_.]+)\s*,\s*\'DD/MM\'\s*\)', 
        r"strftime(CAST(\1 AS DATE), '%d/%m')", 
        query, flags=re.IGNORECASE
    )

    # 2. Replace `to_char(..., 'DD/MM/YYYY')` with `strftime(..., '%d/%m/%Y')`
    query = re.sub(
        r'to_char\s*\(\s*([a-zA-Z0-9_.]+)\s*,\s*\'DD/MM/YYYY\'\s*\)', 
        r"strftime(CAST(\1 AS DATE), '%d/%m/%Y')", 
        query, flags=re.IGNORECASE
    )

    

    # 3. Remove lines containing alter table
    query = re.sub(r'(?i)^.*alter table.*$', '', query, flags=re.MULTILINE)
    return query

def preprocess_postgresql_queries(queries):
    """transforme une liste de requêtes PostgreSQL compatibles vers des fonctions SQLITE compatibles"""
    res = []
    for query in queries:
        res.append(preprocess_postgresql_query(query))
    return res


def generate_table(current_magasin, current_table, current_dependances=None, verbose=False):
    """
        permet de générer et de sauvegarder la table "choosen_table" du magasin "choosen_magasin".
    """
    # récupération des tables utiles pour la génération 
    tables_utiles = magasin_specs[current_magasin]['tables'][current_table]['tables']
    
    # récupération des scripts à exécuter préalablement
    dependances = magasin_specs[current_magasin]['tables'][current_table]['dependances']

    if(verbose):
        print("- tables_utiles :", tables_utiles)
        print("- dependances :", dependances)
        print("- current_dependances :", current_dependances)

    dependances_filtered = []
    tables_dependance = []
    for dependance in dependances:
        if(current_dependances is not None):
            if(dependance not in current_dependances):
                tables_dependance += dependance_specs[dependance]['tables']
                # on retire les dépendances qui ont déjà été exexutées
                dependances_filtered.append(dependance)
        else :
            tables_dependance += dependance_specs[dependance]['tables']
            dependances_filtered.append(dependance)
    
    if(verbose):
        print("- dependances_filtered :", dependances_filtered)

    # récapitulatif des tables à importer
    tables_to_import = list(set(tables_dependance+tables_utiles))
    
    # vérification que l'utilisateur a bien tous les dataframes indiqués
    error = check_existing_tables(tables_to_import)
    if(error == 1):
        # pas la peine d'aller plus loin 
        return 1

    # récupération des scripts SQL
    queries = import_sql_files([current_table], magasin_specs[current_magasin]['path'])   
    dependance_queries = import_sql_files(dependances_filtered, magasin_specs[current_magasin]['path']+'dependances/')

    # preprocess des scripts SQL : 
    queries = preprocess_postgresql_queries(queries)
    dependance_queries = preprocess_postgresql_queries(dependance_queries)

    # import de toutes les données utiles dans le dictionnaire
    print("DÉBUT DE L'IMPORT DES DONNÉES POUR LA TABLE "+current_table)
    import_dfs(tables_to_import, DATA_PATH, sep = ',', verbose=False) 

    # conversion du dictionnaire en variable pour duckdb
    for key, df_value in df.items():
        globals()[key] = df_value  # Assign each dataframe to a variable with the name of the key  
        # chargement des dataframes en tant que table dans duckdb : 
        query = f"CREATE TABLE IF NOT EXISTS {key} AS SELECT * FROM {key};".format(key)
        duckdb.sql(query)
    print("DÉBUT DE GÉNÉRATION DE LA TABLE "+current_table)

    # Requêtes de dépendance à exécuter préalablement
    for _, dependance_query in enumerate(dependance_queries):  
        duckdb.sql(dependance_query)

    # Requêtes principales
    for _, query in enumerate(queries):  
        file_name = DATA_PATH+""+current_table+"_"+current_magasin+".csv"
        res = duckdb.sql(query)
    
        if(verbose):
            print(res)
        res.to_csv(file_name)
        print(f"- fichier {Fore.GREEN}"+file_name+f"{Style.RESET_ALL} exporté")
        # mise à jour du fichier local
        update_local_version_table(current_table+"_"+current_magasin)
    return dependances


dependance_specs = {
    'context_performance_sdc' : {
        'tables' : [
            'action_realise', 
            'utilisation_intrant_realise_agrege', 
            'action_realise_manquant_agrege',
            'sdc', 'dispositif', 'liaison_sdc_reseau',
            'liaison_reseaux', 'reseau', 'domaine'
        ]
    },
    'action_realise_agrege' : {
        'tables' : [
            'action_realise', 'utilisation_intrant_realise_agrege', 
            'action_realise_manquant_agrege'     
        ]
    },
    'action_synthetise_agrege' : {
        'tables' : [
            'action_synthetise', 'utilisation_intrant_synthetise_agrege',
            'action_synthetise_manquant_agrege'
        ]
    },
    'intervention_realise_agrege' : {
        'tables' : [
            'intervention_realise', 'utilisation_intrant_realise_agrege',
            'intervention_realise_manquant_agrege'
        ]
    }, 
    'intervention_synthetise_agrege' : {
        'tables' : [
            'intervention_synthetise', 'utilisation_intrant_synthetise_agrege', 
            'intervention_synthetise_manquant_agrege', 'intervention_synthetise_agrege',
            'noeuds_synthetise_restructure', 'connection_synthetise_restructure', 
            'plantation_perenne_synthetise_restructure' 
        ]
    }
}




magasin_specs  = SOURCE_SPECS['magasins']

options = {
    "Tout générer" : [],
    "Générer un magasin" : [],
    "Quitter" : []
}

donnees = {}
executed_dependances = []
while True:
    print("")
    print("")
    print("**************** Interface de gestion des magasins ****************")
    print("")
    print("      version :      ("+VERSION+")            ")
    print("      type :         ("+TYPE+")               ")
    print("      debug :        ("+str(DEBUG)+")         ")
    print("      repertoire :   ("+DATA_PATH+")         ")
    print("")
    print("*******************************************************************")
    print("")
    print("Veuillez choisir une option parmi les suivantes :")
    print("")
    for i, option in enumerate(options.keys()):
        print(f"{i + 1}. {option}")
    
    choice = int(input("Entrez votre choix (1, 2 ...) : "))
    choice_key = list(options.keys())[choice - 1]
    print(choice_key)

    if choice_key == "Quitter":
        print("Au revoir !")
        break

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
            for i, table in enumerate(magasin_specs[choosen_magasin]['tables']):
                print("- " +table)
                executed_dependances += generate_table(choosen_magasin, table, current_dependances=executed_dependances)
        else :
            executed_dependances += generate_table(choosen_magasin, choosen_table, current_dependances=executed_dependances, verbose=VERBOSE)
            



            
            
            
