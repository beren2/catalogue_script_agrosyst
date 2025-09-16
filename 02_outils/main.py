"""
    Fichier principal d'obtention des données.
    À exécuter lors d'une mise à jour des données sur Datagrosyst ou lors de la conception d'outils
    
    Ce script effectue les tâches suivantes  :
    1) Import des données : téléchargement des données de l'entrepôt en utilisant la connexion POSTGRESQL (si TYPE == "DISTANT")
    2) Exécution des scripts de génération des outils (en se basant sur une copie locale des données)
    3) Enregistrement des résultats dans la base entrepôt (si TYPE == "DISTANT")
"""
import os
import json
import configparser
import urllib
import importlib
import time
import psycopg2 as psycopg
from scripts import nettoyage
from scripts import restructuration 
from scripts import indicateur
from scripts import agregation
from scripts import interoperabilite
from scripts import outils_can
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
from colorama import Fore, Style
from tqdm import tqdm
from version import __version__

# obtenir les paramètres de connexion pour psycopg2
config = configparser.ConfigParser()
config.read(r'../00_config/config.ini')

DATA_PATH = config.get('metadata', 'data_path') 
TYPE = config.get('metadata', 'type')
DEBUG = bool(int(config.get('metadata', 'debug')))
BDD_ENTREPOT=config.get('metadata', 'bdd_entrepot')
VERSION = __version__
with open('../00_config/specs.json', encoding='utf8') as json_file:
    SOURCE_SPECS = json.load(json_file)

if(DEBUG):
    NROWS = int(config.get('debug', 'nrows'))
    DATA_PATH = config.get('debug', 'data_test_path')

path_metadata = 'data/metadonnees_tests.csv'
df_metadata = pd.read_csv(path_metadata)

DATABASE_URI_entrepot=None
if(TYPE == 'distant'):
    # On se connecte à la BDD seulement si l'utilisateur veut déclarer à distance
    DB_HOST = config.get(BDD_ENTREPOT, 'host')
    DB_PORT = config.get(BDD_ENTREPOT, 'port')
    DB_NAME_ENTREPOT = config.get(BDD_ENTREPOT, 'database')
    DB_USER = config.get(BDD_ENTREPOT, 'user')
    DB_PASSWORD = urllib.parse.quote(config.get(BDD_ENTREPOT, 'password'))
    DATABASE_URI_entrepot = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_ENTREPOT}'

    #Créer la connexion pour sqlalchemy (pour executer des requetes : uniquement pour l entrepot)
    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_ENTREPOT}')

    # Establish a connection to PostgreSQL
    conn = engine.raw_connection()
    cur = conn.cursor()

def check_existing_files(file_names):
    """vérifie que toutes les tables sont présentes"""
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
        json.dump(version_control, version_file)

    return 0

def export_to_db(df, name):
    """ permet d'exporter un dataframe dans une table de l'entrepôt avec """
    if(TYPE == 'local'):
        if('entrepot_' in name):
            name = name[9:]
        if(DEBUG):
            df.iloc[0:NROWS].to_csv(DATA_PATH+name+'.csv')
            update_local_version_table(name)
        else:
            df.to_csv(DATA_PATH+name+'.csv')
            update_local_version_table(name)
    else :
        df.to_sql(name=name, con=engine, if_exists='replace')
        engine.dispose()
    print("* CRÉATION TABLE ",name, " TERMINEE *")

def add_primary_key(table_name, pk_column):
    """Ajoute une clé primaire avec reconnexion forcée"""

    if TYPE != "distant":
        print(f"ℹ️ Type {TYPE} : clé primaire ignorée pour {table_name}")
        return

    conn = None
    cur = None
    try:
        # ⚠️ On force la reconnexion à chaque appel (pas besoin de global)
        engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_ENTREPOT}')
        conn = engine.raw_connection()
        cur = conn.cursor()

        cur.execute("SET statement_timeout = 0;")
        sql = f'ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column});'
        cur.execute(sql)
        conn.commit()
        # print(f"✅ Clé primaire {pk_column} ajoutée à {table_name}")

    except Exception as e:
        print(f"⚠️ Impossible d'ajouter la clé primaire sur {table_name} : {e}")

    finally:
        if cur is not None and not cur.closed:
            cur.close()
        if conn is not None and not conn.closed:
            conn.close()



def convert_to_serializable(obj):
    """ Permet de convertir un objet pandas en list ou dictionnaire """
    if isinstance(obj, pd.Index):
        return obj.tolist()
    if isinstance(obj, pd.Series):
        return obj.tolist()
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def export_dict_to_catalogue(dic, name):
    """ permet d'exporter un dictionnaire dans le catalgoue data/export_from_functions"""
    pathway_for_data_to_export = 'data/export_from_functions/'
    if('entrepot_' in name):
        name = name[9:]
    if(TYPE == 'local'):
        with open(DATA_PATH + name + '.json', 'w', encoding="utf-8") as f:
            json.dump(dic, f, default=convert_to_serializable, indent=4)
    else :
        with open(pathway_for_data_to_export + name + '.json', 'w', encoding="utf-8") as f:
            json.dump(dic, f, default=convert_to_serializable, indent=4)
    print("* CRÉATION DANS LE CATALOGUE DU DICTIONNAIRE ",name, " TERMINEE *")


donnees = {}

def import_df(df_name, path_data, sep, file_format='csv') :
    """
        importe un dataframe au chemin path_data+df_name+'.csv' et le stock dans le dictionnaire 'df' à la clé df_name
    """
    global donnees
    if file_format == 'csv' :
        if(DEBUG):
            donnees[df_name] = pd.read_csv(path_data+df_name+'.'+file_format, sep = sep, low_memory=False, nrows=NROWS).replace({'\r\n': '\n'}, regex=True)
        else:
            donnees[df_name] = pd.read_csv(path_data+df_name+'.'+file_format, sep = sep, low_memory=False).replace({'\r\n': '\n'}, regex=True)
    if file_format == 'json' and df_name.startswith('geoVec') :
        # Utilise geopandas pour les json formater en geojson. Le nom du fichier json doit alors commencer par geoVec
        donnees[df_name] = gpd.read_file(path_data+df_name+'.'+file_format)
    if file_format == 'gpkg' :
        donnees[df_name] = gpd.read_file(path_data+df_name+'.'+file_format)


# FAIRE UN IMPORT DF POUR EXTERNAL DATA !

def import_dfs(df_names, data_path, sep = ',', verbose=False, file_format='csv'):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans la liste df_names
    """
    global donnees
    pbar = tqdm(df_names)
    for df_name in pbar:
        pbar.set_description(f"Import de {df_name}")
        import_df(df_name, data_path, sep, file_format=file_format)


def copy_table_to_csv(table_name, csv_path, csv_name):
    """
        Permet de copier une table depuis la base de donnée distance dans un fichier local csv_path+csv_name.csv
    """
    with psycopg.connect(DATABASE_URI_entrepot) as connection:
        cursor = connection.cursor()

        with open(csv_path+csv_name+".csv", "wb") as f:
            if(DEBUG):
                cursor.copy_expert("COPY (SELECT * from "+table_name+" LIMIT "+str(NROWS)+") TO STDOUT WITH CSV DELIMITER ',' HEADER", file=f)
            else:
                cursor.copy_expert("COPY "+table_name+" TO STDOUT WITH CSV DELIMITER ',' HEADER", file=f)
    update_local_version_table(table_name)

def copy_tables_to_csv(table_names, csv_path, verbose=False):
    """
        permet de copier un ensemble de tables depuis la base de données distance dans des fichiers local au csv_path
    """
    pbar = tqdm(table_names)
    for table_name in pbar : 
        if(verbose) :
            print("- ", table_name)
        pbar.set_description(f"Téléchargement de {table_name}")
        copy_table_to_csv('entrepot_'+table_name, csv_path, table_name)

def download_datas(desired_tables, verbose=False):
    """
        Télécharge toutes les données dans la liste tables en local
    """
    copy_tables_to_csv(desired_tables, DATA_PATH, verbose=verbose)

def load_datas(desired_tables, verbose=True, path_data=DATA_PATH, file_format='csv'):
    """ permet de charger les tables dans la variable globale donnees"""
    global donnees
    import_dfs(desired_tables, path_data, verbose=verbose, file_format=file_format)

def load_datas_entrepot(desired_tables, verbose=True, path_data=DATA_PATH, file_format='csv', need_perf=False):
    """permet de charger les tables de l'entrepôt dans la variable globale donnée"""
    filtered_tables = []
    for desired_table in desired_tables:
        if(not need_perf) :
            # si on a pas besoin des performances, alors on enlève les tables de cette catégorie
            if(SOURCE_SPECS['entrepot']['tables'][desired_table]['category'] != "performance"):
                filtered_tables.append(desired_table)
        else :
            filtered_tables.append(desired_table)
    load_datas(filtered_tables, verbose=verbose, path_data=DATA_PATH, file_format=file_format)


def check_files_exist(tables, path_data=DATA_PATH, verbose=False):
    """
        Vérifie que toutes les tables sont accessible au chemin path_data.
        - tables : liste de nom auquel on rajoutera ".csv" pour checker l'existence dans le répertoire.

        retourne une liste des tables manquantes
    """
    leaking_tables = []
    for table in tables :
        file_name = table+'.csv'
        file = path_data+file_name
        if(not os.path.isfile(file)):
            leaking_tables.append(table)
            if(verbose):
                print(f"- fichier {Fore.RED}"+file+f"{Style.RESET_ALL} manquant")
    return leaking_tables
    

def get_leaking_tables_for_category(category, verbose=False):
    """
        Vérifier si toutes les tables nécessaires à la génération de l'outil sont accessibles 
        - Tables de l'entrepôt
        - Tables outils dépendances
        - Tables externes
    """
    entrepot_spec = SOURCE_SPECS['entrepot']
    category_spec = SOURCE_SPECS['outils']['categories'][category]
    external_data_spec = SOURCE_SPECS['outils']['external_data']
    outils_dependances = category_spec['dependances']

    # constitution de la liste des tables de l'entrepôt (toujours supposées nécessaires, sauf pour la catégorie test)
    entrepot_tables = []
    for _, table_name in enumerate(entrepot_spec['tables']):
        entrepot_tables.append(table_name)

    # constitution de la liste des tables dépendantes pour la catégorie :
    dependance_tables = []
    for _, outil_dependance in enumerate(outils_dependances):
        if(verbose):
            print("dependance : ", outil_dependance['category'])
        print(outil_dependance)
        category = outil_dependance['category']
        dependance_tables += SOURCE_SPECS['outils']['categories'][category]['generated']


    # check que toutes les tables de l'entrepôt sont présentes
    leaking_tables_entrepot = check_files_exist(entrepot_tables)

    # check que toutes les tables outils nécessaires sont présentes
    leaking_tables_outils = check_files_exist(dependance_tables)

    # check que toutes les tables externes nécessaires sont présentes
    leaking_tables_external = check_files_exist(
        external_data_spec['tables'], 
        path_data=external_data_spec['path'])

    if(verbose):
        print('Tables manquantes entrepôt : ', leaking_tables_entrepot)
        print('Tables manquantes outils : ', leaking_tables_outils)
        print('Tables manquantes externes : ', leaking_tables_external)
    
    return {
        'entrepot' : leaking_tables_entrepot, 
        'outils' : leaking_tables_outils,
        'external' : leaking_tables_external
    }


def test_all_findable_for_category(category, verbose=False):
    """
        retourne un message et un code d'erreur si certaines tables ne sont pas trouvées
    """
    
    leaking_tables = get_leaking_tables_for_category(category)
    error_message = """Vous disposez de toutes les tables nécessaires."""
    error_code = 0

    # si au moins l'une des listes est non-vide, on doit retourner une erreur
    if(len(leaking_tables['entrepot']) > 0 or len(leaking_tables['outils'])>0 or len(leaking_tables['external']) >0):
        error_message = f"""{Fore.RED}Attention, il manque les tables suivantes :{Style.RESET_ALL}
entrepot : """+str(leaking_tables['entrepot'])+ """ ("""+DATA_PATH+""")
outils : """+str(leaking_tables['outils'])+""" ("""+DATA_PATH+""")
external : """+str(leaking_tables['external'])+""" ("""+SOURCE_SPECS['outils']['external_data']['path']+""")
        """
        error_code = 1

    return error_code, error_message

def test_check_external_data(leaking_tables):
    """
        Print les résultats des tests effectués dans le fichier défini 
        dans la spec : outils.external_data.validation.path
        Retourne 0 si tout s'est bien passé, 1 sinon

        leaking_tables : list, fichiers non présents en local
    """
    external_tables = SOURCE_SPECS['outils']['external_data']['tables']
    external_tables_existing = [t for t in external_tables if t not in leaking_tables]

    external_data_validation = SOURCE_SPECS['outils']['external_data']['validation']
    external_data_validation_path = external_data_validation['path']
    external_data_validation_checks = [check for check in external_data_validation['checks'] if check['table'] not in leaking_tables]

    # load des données externes
    load_datas(
        external_tables_existing, 
        verbose=True, 
        path_data=SOURCE_SPECS['outils']['external_data']['path']
    )
    
    all_passed = True
    for check in external_data_validation_checks:
        external_data_test_module = importlib.import_module(external_data_validation_path)
        check_function = getattr(external_data_test_module, check['function_name'])
        message_error = check_function(donnees)
        
        if len(message_error) == 0:
            print(f"{Fore.GREEN}", check['name'], ":", f"validé {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}", check['name'], ":", f"échoué {Style.RESET_ALL}")
            print(message_error)
            print("\n")
            all_passed = False

    if all_passed:
        error_code = 0
        error_message = f"{Fore.GREEN}Les données externes testées sont conformes{Style.RESET_ALL}"
    else :
        error_code = 0
        error_message = f"{Fore.RED}Certaines des données externes ne sont pas conformes{Style.RESET_ALL}"
    
    return error_code, error_message

def generate_leaking_df(df1, df2, id_name, columns_difference):
    """
        retourne un dataframe qui contient les lignes entre les df1 et df2 où les colonnes contenues
        dans columns_difference diffèrent
    """
    df1 = df1[df1.columns.difference(columns_difference)].drop_duplicates().rename(
        columns={id_name: 'id'}
    ).set_index('id')
    df2 = df2.set_index('id')
    return pd.concat([df1, df2], axis=0)

def generate_data_agreged(verbose=False):
    """
        génère l'ensemble des données agrégées
        utile car on ne stocke pas en base les jeux de données agrégés
        on ne stock que les différences à chaque étape pour limiter 
        la redondance d'informations
    """
    global donnees

    # Génération de action_realise_agrege
    df1 = donnees['utilisation_intrant_realise_agrege'].copy()
    df2 = donnees['action_realise_manquant_agrege'].copy()
    donnees['action_realise_agrege'] = generate_leaking_df(df1, df2, 'action_realise_id', columns_difference = ['id'])
    donnees['action_realise_agrege'] = donnees['action_realise_agrege'].reset_index()

    # Génération de action_synthétisé_agrege
    df1 = donnees['utilisation_intrant_synthetise_agrege'].copy()
    df2 = donnees['action_synthetise_manquant_agrege'].copy()
    donnees['action_synthetise_agrege'] = generate_leaking_df(df1, df2, 'action_synthetise_id', columns_difference = ['id'])
    donnees['action_synthetise_agrege'] = donnees['action_synthetise_agrege'].reset_index()

    # Génération de intervention_realise_agrege
    df1 = donnees['utilisation_intrant_realise_agrege'].copy()
    df2 = donnees['intervention_realise_manquant_agrege'].copy()
    donnees['intervention_realise_agrege'] = generate_leaking_df(df1, df2, 'intervention_realise_id', columns_difference = ['id', 'action_realise_id'])
    donnees['intervention_realise_agrege'] = donnees['intervention_realise_agrege'].reset_index()

    # Génération de intervention_synthetise_agrege
    df1 = donnees['utilisation_intrant_synthetise_agrege'].copy()
    df2 = donnees['intervention_synthetise_manquant_agrege'].copy()
    donnees['intervention_synthetise_agrege'] = generate_leaking_df(df1, df2, 'intervention_synthetise_id', columns_difference = ['id', 'action_synthetise_id'])
    donnees['intervention_synthetise_agrege'] = donnees['intervention_synthetise_agrege'].reset_index()

def download_data_agreged(verbose=False):
    """
        permet de télécharger en csv les jeux de données agrégés complets
    """
    global donnees
    donnees['action_realise_agrege'].to_csv(DATA_PATH+'action_realise_agrege.csv')
    donnees['action_synthetise_agrege'].to_csv(DATA_PATH+'action_synthetise_agrege.csv')
    donnees['intervention_realise_agrege'].to_csv(DATA_PATH+'intervention_realise_agrege.csv')
    donnees['intervention_synthetise_agrege'].to_csv(DATA_PATH+'intervention_synthetise_agrege.csv')


def load_ref(verbose=False):
    """
        permet de charger les référentiels
        ATTENTION : cette fonction est ammenée à disparaître car à terme, 
        tous les référentiels devront être accessibles sur Datagrosyst.
    """
    global donnees
    path = 'data/referentiels/'
    refs = [
        'ref_nuisible_edi', 
        'ref_correspondance_groupe_cible',
        'ref_adventice', 
        'dose_ref_cible',
        'ref_acta_traitement_produit',
        'conversion_utilisation_intrant',
        'ref_culture_maa'
    ]
    import_dfs(refs, path, verbose=True)




def create_category_nettoyage():
    """
        Execute les requêtes pour créer les outils de nettoyage
    """
    # nettoyage_intervention_realise
    name_table = 'intervention_realise'
    df_nettoyage_intervention_realise = nettoyage.nettoyage_intervention(donnees, path_metadata='data/')

    export_to_db(df_nettoyage_intervention_realise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_intervention_realise.to_csv('entrepot_'+name_table+'_nettoyage.csv')
    add_primary_key('entrepot_'+name_table+'_nettoyage', 'id')

    # nettoyage_utilisation_intrant_realise
    name_table = 'utilisation_intrant_realise'
    df_nettoyage_utilisation_intrant_realise = nettoyage.nettoyage_utilisation_intrant(donnees, saisie='realise', verbose=False, path_metadata='data/')

    export_to_db(df_nettoyage_utilisation_intrant_realise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_utilisation_intrant_realise.to_csv(prefixe_source+suffixe_table+'_realise.csv')
    add_primary_key('entrepot_'+name_table+'_nettoyage', 'id')

    # nettoyage_utilisation_intrant_synthetise
    name_table = 'utilisation_intrant_synthetise'
    df_nettoyage_utilisation_intrant_synthetise = nettoyage.nettoyage_utilisation_intrant(donnees, saisie='synthetise', verbose=False, path_metadata='data/')

    export_to_db(df_nettoyage_utilisation_intrant_synthetise, 'entrepot_'+name_table+'_nettoyage')
    add_primary_key('entrepot_'+name_table+'_nettoyage', 'id')
    #df_nettoyage_utilisation_intrant_synthetise.to_csv(prefixe_source+suffixe_table+'_synthetise.csv')

def create_category_agregation():
    """
        Execute les requêtes pour créer les outils d'agregation
    """

    # permet d'obtenir des tables agrégées pour avoir les niveaux supérieurs depuis les niveaux fins (raccourcis)
    aggreged_utilisation_intrant_synthetise = agregation.get_aggreged_from_utilisation_intrant_synthetise(
        donnees
    )
    export_to_db(aggreged_utilisation_intrant_synthetise, 'entrepot_utilisation_intrant_synthetise_agrege')
    add_primary_key('entrepot_utilisation_intrant_synthetise_agrege', 'id')

    # permet d'obtenir des tables agrégées pour avoir les niveaux supérieurs depuis les niveaux fins (raccourcis)
    aggreged_utilisation_intrant_realise = agregation.get_aggreged_from_utilisation_intrant_realise(
        donnees
    )
    export_to_db(aggreged_utilisation_intrant_realise, 'entrepot_utilisation_intrant_realise_agrege')
    add_primary_key('entrepot_utilisation_intrant_realise_agrege', 'id')
    
    # toutes les infos manquantes agrégées depuis l'action
    aggreged_leaking_action_realise = agregation.get_leaking_aggreged_from_action_realise(
        aggreged_utilisation_intrant_realise, donnees
    )
    export_to_db(aggreged_leaking_action_realise, 'entrepot_action_realise_manquant_agrege')
    add_primary_key('entrepot_action_realise_manquant_agrege', 'id')

    aggreged_leaking_action_synthetise = agregation.get_leaking_aggreged_from_action_synthetise(
        aggreged_utilisation_intrant_synthetise, donnees
    )
    export_to_db(aggreged_leaking_action_synthetise, 'entrepot_action_synthetise_manquant_agrege')
    add_primary_key('entrepot_action_synthetise_manquant_agrege', 'id')
    

    # toutes les infos manquantes agrégées depuis l'intervention 
    aggreged_leaking_intervention_realise = agregation.get_leaking_aggreged_from_intervention_realise(
        aggreged_utilisation_intrant_realise, donnees
    )
    export_to_db(aggreged_leaking_intervention_realise, 'entrepot_intervention_realise_manquant_agrege')
    add_primary_key('entrepot_intervention_realise_manquant_agrege', 'id')
    
    aggreged_leaking_intervention_synthetise = agregation.get_leaking_aggreged_from_intervention_synthetise(
        aggreged_utilisation_intrant_synthetise, donnees
    )
    export_to_db(aggreged_leaking_intervention_synthetise, 'entrepot_intervention_synthetise_manquant_agrege')
    add_primary_key('entrepot_intervention_synthetise_manquant_agrege', 'id')
    
def create_category_restructuration():
    """
        Execute les requêtes pour créer les outils de restructuration
    """
    df_noeuds_synthetise_restructured = restructuration.restructuration_noeuds_synthetise(donnees)
    export_to_db(df_noeuds_synthetise_restructured, 'entrepot_noeuds_synthetise_restructure')
    add_primary_key('entrepot_noeuds_synthetise_restructure', 'id')

    df_connection_synthetise_restructured = restructuration.restructuration_connection_synthetise(donnees)
    export_to_db(df_connection_synthetise_restructured, 'entrepot_connection_synthetise_restructure')
    add_primary_key('entrepot_connection_synthetise_restructure', 'id')

    df_noeuds_realise_restructured = restructuration.restructuration_noeuds_realise(donnees)
    export_to_db(df_noeuds_realise_restructured, 'entrepot_noeuds_realise_restructure')
    add_primary_key('entrepot_noeuds_realise_restructure', 'id')
    
    df_noeuds_realise_restructured = restructuration.restructuration_recolte_rendement_prix(donnees)
    export_to_db(df_noeuds_realise_restructured, 'entrepot_recolte_rendement_prix_restructure')
    add_primary_key('entrepot_recolte_rendement_prix_restructure', 'id')

    df_plantation_perenne_synthetise_restructured = restructuration.restructuration_plantation_perenne_synthetise(donnees)
    export_to_db(df_plantation_perenne_synthetise_restructured, 'entrepot_plantation_perenne_synthetise_restructure')
    add_primary_key('entrepot_plantation_perenne_synthetise_restructure', 'id')

    # Attention, en suivant parfaitement la convention de nommage, on aboutit à des noms de tables trop longs pour être pris en charge
    # par Postgres en tant que nom de table (taille maximum : 63), on raccourci donc : "composant_culture_concerne" en "ccc"
    df_composant_culture_concerne_intervention_synthetise_restructured = \
        restructuration.restructuration_composant_culture_concerne_intervention_synthetise(donnees)
    export_to_db(
        df_composant_culture_concerne_intervention_synthetise_restructured,
        'entrepot_ccc_intervention_synthetise_restructure'
    )
    add_primary_key('entrepot_ccc_intervention_synthetise_restructure', 'id')

    df_intervention_synthetise_restructure = restructuration.restructuration_intervention_synthetise(donnees)
    export_to_db(df_intervention_synthetise_restructure, 'entrepot_intervention_synthetise_restructure')
    add_primary_key('entrepot_intervention_synthetise_restructure', 'id')

def create_category_indicateur_0():
    """
        Execute les requêtes pour créer les outils des indicateurs uniquement pour les fonctions de poids de connexions !
        A faire passer avant indicateur_1 qui a besoin de la génération des poids de connexions et de la typologie_can_culture
    """
    _, csv_of_bad_synth = indicateur.extract_good_rotation_diagram(donnees)
    export_to_db(csv_of_bad_synth, 'entrepot_mauvaise_structure_de_rotation')
    add_primary_key('entrepot_mauvaise_structure_de_rotation', 'index')

    df_get_connexion_weight_in_synth_rotation, df_get_couple_connexion_paths, list_synthe_somme_pas_a_un = indicateur.get_connexion_weight_in_synth_rotation(donnees)
    export_dict_to_catalogue(list_synthe_somme_pas_a_un, 'list_synthe_somme_pas_a_un')

    export_to_db(df_get_couple_connexion_paths, 'entrepot_couple_connexions_chemins_synthetise_rotation')
    add_primary_key('entrepot_couple_connexions_chemins_synthetise_rotation', 'connexion_id, chemin_id')

    export_to_db(df_get_connexion_weight_in_synth_rotation, 'entrepot_poids_connexions_synthetise_rotation')
    add_primary_key('entrepot_poids_connexions_synthetise_rotation', 'connexion_id')

def create_category_indicateur_1():
    """
        Crée les typologies de culture de base pour les autres indicateurs. 
        N'a pas besoin des poids de connexions !
        A faire passer avant indicateur_2 qui a besoin de la génération des poids de connexions et de la typologie_can_culture
    """
    df_typologie_culture_CAN= indicateur.get_typologie_culture_CAN(donnees)
    export_to_db(df_typologie_culture_CAN, 'entrepot_typologie_can_culture')
    add_primary_key('entrepot_typologie_can_culture', 'index')

def create_category_indicateur_2():
    """
        Execute les requêtes pour créer les outils des indicateurs (sauf poids de conenxions et typo_can_culture, voir create_category_indicateur_0)
    """
    # df_surface_connexion_synthetise = indicateur.get_surface_connexion_synthetise(donnees)
    # export_to_db(df_surface_connexion_synthetise, 'entrepot_surface_connection_synthetise')
    
    df_utilsation_intrant_indicateur = indicateur.indicateur_utilisation_intrant(donnees)
    export_to_db(df_utilsation_intrant_indicateur, 'entrepot_utilisation_intrant_indicateur')
    add_primary_key('entrepot_utilisation_intrant_indicateur', 'id')

    df_identification_pz0 = indicateur.identification_pz0(donnees)
    export_to_db(df_identification_pz0, 'entrepot_identification_pz0')
    add_primary_key('entrepot_identification_pz0', 'entite_id')

    df_typologie_rotation_CAN_synthetise= indicateur.get_typologie_rotation_CAN_synthetise(donnees)
    export_to_db(df_typologie_rotation_CAN_synthetise, 'entrepot_typologie_can_rotation_synthetise')
    add_primary_key('entrepot_typologie_can_rotation_synthetise', 'synthetise_id')

    df_typologie_assol_CAN_realise= indicateur.get_typologie_assol_CAN_realise(donnees)
    export_to_db(df_typologie_assol_CAN_realise, 'entrepot_typologie_assol_can_realise')
    add_primary_key('entrepot_typologie_assol_can_realise', 'sdc_id')

    # TODO : on fait appel à une fonction "get_recolte_realise_outils_can" car l'importance pour tout le monde de bénéficier de cet outil a été identifié à posteriori.
    # Ce n'est pas idéal, il vaudrait mieux créer une fonction qui créer cette outil et faire appel à cet outil dans les outils can / le magasin can
    df_action_realise_rendement_total = outils_can.get_recolte_realise_outils_can(donnees)
    df_action_realise_rendement_total = df_action_realise_rendement_total.rename(columns={'action_id' : 'action_realise_id'})
    export_to_db(df_action_realise_rendement_total, 'entrepot_action_realise_rendement_total')
    add_primary_key('entrepot_action_realise_rendement_total', 'index')

    # TODO : cf commentaire plus haut : idem pour "get_recolte_synthetise_outils_can"
    df_action_synthetise_rendement_total = outils_can.get_recolte_synthetise_outils_can(donnees)
    df_action_synthetise_rendement_total = df_action_synthetise_rendement_total.rename(columns={'action_id' : 'action_synthetise_id'})
    export_to_db(df_action_synthetise_rendement_total, 'entrepot_action_synthetise_rendement_total')
    add_primary_key('entrepot_action_synthetise_rendement_total', 'index')


def create_category_interoperabilite():
    """
        Execute les requêtes pour créer les outils d'interopérabilité
    """
    df_donnees_spatiales_commune_du_domaine = interoperabilite.get_donnees_spatiales_commune_du_domaine(donnees)
    export_to_db(df_donnees_spatiales_commune_du_domaine, 'entrepot_donnees_spatiales_commune_du_domaine')
    add_primary_key('entrepot_donnees_spatiales_commune_du_domaine', 'domaine_id')

    df_donnees_spatiales_coord_gps_du_domaine = interoperabilite.get_donnees_spatiales_coord_gps_du_domaine(donnees)
    export_to_db(df_donnees_spatiales_coord_gps_du_domaine, 'entrepot_donnees_spatiales_coord_gps_du_domaine')
    add_primary_key('entrepot_donnees_spatiales_coord_gps_du_domaine', 'geopoint_id')

def create_category_outils_can():
    """
        Execute les requêtes pour créer le source des outils utiles pour la génération des csv CAN
    """
    # création de l'outil permettant de filtrer les entités (dispositifs)
    df_dispositif_filtres_outils_can = outils_can.dispositif_filtres_outils_can(donnees)
    df_dispositif_filtres_outils_can.set_index('id', inplace=True)
    export_to_db(df_dispositif_filtres_outils_can, 'entrepot_dispositif_filtres_outils_can')
    add_primary_key('entrepot_dispositif_filtres_outils_can', 'id')

    # création de l'outil permettant de filtrer les entités (domaine)
    df_domaine_filtres_outils_can = outils_can.domaine_filtres_outils_can(donnees)
    df_domaine_filtres_outils_can.set_index('id', inplace=True)
    export_to_db(df_domaine_filtres_outils_can, 'entrepot_domaine_filtres_outils_can')
    add_primary_key('entrepot_domaine_filtres_outils_can', 'id')

    df_parcelle_non_ratachee_outils_can = outils_can.get_parcelles_non_rattachees_outils_can(donnees)
    df_parcelle_non_ratachee_outils_can.set_index('id', inplace=True)
    export_to_db(df_parcelle_non_ratachee_outils_can, 'entrepot_parcelle_non_rattachee_outils_can')
    add_primary_key('entrepot_parcelle_non_rattachee_outils_can', 'id')

    df_culture_outils_can = outils_can.get_culture_outils_can(donnees)
    df_culture_outils_can.set_index('id', inplace=True)
    export_to_db(df_culture_outils_can, 'entrepot_culture_outils_can')
    add_primary_key('entrepot_culture_outils_can', 'id')

    df_intervention_realise_outils_can = outils_can.get_intervention_realise_outils_can(donnees)
    df_intervention_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_intervention_realise_outils_can, 'entrepot_intervention_realise_outils_can')
    add_primary_key('entrepot_intervention_realise_outils_can', 'id')

    df_intervention_synthetise_outils_can = outils_can.get_intervention_synthetise_outils_can(donnees)
    df_intervention_synthetise_outils_can.set_index('id', inplace=True)
    export_to_db(df_intervention_synthetise_outils_can, 'entrepot_intervention_synthetise_outils_can')
    add_primary_key('entrepot_intervention_synthetise_outils_can', 'id')

    df_recolte_outils_can = outils_can.get_recolte_outils_can(donnees)
    export_to_db(df_recolte_outils_can, 'entrepot_recolte_outils_can')
    add_primary_key('entrepot_recolte_outils_can', 'action_id, rendement_unite, destination')

    df_zone_outils_can = outils_can.get_zone_realise_outils_can(donnees)
    df_zone_outils_can.set_index('id', inplace=True)
    export_to_db(df_zone_outils_can, 'entrepot_zone_realise_outils_can')
    add_primary_key('entrepot_zone_realise_outils_can', 'id')

    df_sdc_realise_outils_can = outils_can.get_sdc_realise_outils_can(donnees)
    df_sdc_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_sdc_realise_outils_can, 'entrepot_sdc_realise_outils_can')
    add_primary_key('entrepot_sdc_realise_outils_can', 'id')

    df_parcelle_realise_outils_can = outils_can.get_parcelle_realise_outils_can(donnees)
    df_parcelle_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_parcelle_realise_outils_can, 'entrepot_parcelle_realise_outils_can')
    add_primary_key('entrepot_parcelle_realise_outils_can', 'id')


def create_category_test():
    """ 
            Execute les requêtes pour tester la génération d'outils spécifiques
    """
    # df_identification_pz0 = indicateur.identification_pz0(donnees)
    # export_to_db(df_identification_pz0, 'entrepot_identification_pz0')
    # add_primary_key('entrepot_identification_pz0', 'entite_id')

    # print('Fin du test de entrepot_identification_pz0')

# à terme, cet ordre devra être généré automatiquement à partir des dépendances --> mais pour l'instant plus simple comme ça
steps = [
    {'source' : 'outils', 'category' : 'nettoyage'},
    {'source' : 'outils', 'category' : 'agregation'},
    {'source' : 'outils', 'category' : 'agregation_complet'},
    {'source' : 'outils', 'category' : 'restructuration'},
    {'source' : 'outils', 'category' : 'indicateur_0'},
    {'source' : 'outils', 'category' : 'indicateur_1'},
    {'source' : 'outils', 'category' : 'indicateur_2'},
    {'source' : 'outils', 'category' : 'interoperabilite'},
    {'source' : 'outils', 'category' : 'outils_can'}
]

options_categories = {}

for source_key, source in SOURCE_SPECS.items():
    if(source_key == 'outils'):
        for categorie_key in source['categories']:
            options_categories[categorie_key +' ('+ source_key+')'] = {'source' : source_key, 'category' : categorie_key}
            categorie = source['categories'][categorie_key]
            dependances = categorie['dependances']

history = []


options = {
    'local' : {
        "Tout générer" : [],
        "Générer une catégorie" : [],  
        "Tester la cohérence des données externes": [],
        "Quitter" : []
    },
    'distant' : {
        "Tout générer" : [],
        "Générer une catégorie" : [],  
        "Tester la cohérence des données externes": [],
        "Télécharger une catégorie" : [],
        "Quitter" : []
    }
}

donnees = {}
while True:
    print("")
    print("")
    print("**************** Interface de gestion des outils ****************")
    print("")
    print("      version :      ("+VERSION+")            ")
    print("      type :         ("+TYPE+")               ")
    print("      debug :        ("+str(DEBUG)+")         ")
    print("      repertoire :   ("+DATA_PATH+")         ")
    if(TYPE == 'distant'):
        print("      BDD :          ("+DB_NAME_ENTREPOT+")         ")
    print("")
    print("*****************************************************************")
    print("")

    print("""Information(s) : le type local signifie qu'on supprime toutes les fonctionnalités liées aux BDD.
Par exemple, les outils générés sont téléchargés uniquement en csv et pas importés dans la base.
En revanche, dans tous les cas, il faut disposer des csv de l'entrepôt à jour en local.
          """, )

    print("Veuillez choisir une option parmi les suivantes :")
    print("")
    for i, option in enumerate(options[TYPE].keys()):
        print(f"{i + 1}. {option}")
    
    choice = int(input("Entrez votre choix (1, 2 ...) : "))
    choice_key = list(options[TYPE].keys())[choice - 1]
    
    if choice_key == "Quitter":
        print("Au revoir !")
        break

    if choice_key == 'Tout générer':

        # Téléchargement et chargement des données
        if(TYPE == 'distant'):
            print("* TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
            download_datas(list(SOURCE_SPECS['entrepot']['tables'].keys()), verbose=False)
        # Vérification que toutes les données sont présentes pour la première catégorie
        error_code_findable, error_message_findable = test_all_findable_for_category(steps[0]['category'])
        print(error_message_findable)

        
        # Si toutes les données nécessaires sont disponibles, on peut les charger
        if(error_code_findable == 0):
            # Vérification que les données externes vérifient le format attendu
            error_code_check, error_message_check = test_check_external_data(leaking_tables=[])
            print(error_message_check)
            if(error_code_check == 0):

                # Chargement des données
                print("* CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                load_datas_entrepot(list(SOURCE_SPECS['entrepot']['tables'].keys()), verbose=False, need_perf=False)
                print("* CHARGEMENT DES DONNÉES EXTERNES *")
                load_datas(SOURCE_SPECS['outils']['external_data']['tables'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['path'])
                print("* CHARGEMENT DES DONNÉES SPATIALES EXTERNES *")
                load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['geojson'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='json')
                load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['geopackage'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='gpkg')
                load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['csv_geo'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='csv')
                print("* CHARGEMENT DES RÉFÉRENTIELS *")
                print("Attention, penser à les mettre à jour manuellement.")
                load_ref()

                for step in steps :
                    CURRENT_SOURCE = step['source']
                    CURRENT_CATEGORY = step['category']

                    # Vérification que toutes les données sont présentes pour la catégorie courante
                    error_code_findable, error_message_findable = test_all_findable_for_category(step['category'])
                    print(error_message_findable)
                    if(error_code_findable == 0):
                        print("* GÉNÉRATION ", CURRENT_SOURCE, CURRENT_CATEGORY," *")
                        choosen_function = eval(str(SOURCE_SPECS[CURRENT_SOURCE]['categories'][CURRENT_CATEGORY]['function_name']))

                        if(CURRENT_CATEGORY == 'agregation_complet'):
                            # Lors de la génération de agregation_complet, il faut aussi créer les dataframes.
                            generate_data_agreged(verbose=False)
                            download_data_agreged(verbose=False)
                        else :
                            choosen_function()
                            if(TYPE == 'distant'):
                                download_datas(SOURCE_SPECS[CURRENT_SOURCE]['categories'][CURRENT_CATEGORY]['generated'])
                            load_datas(SOURCE_SPECS[CURRENT_SOURCE]['categories'][CURRENT_CATEGORY]['generated'])
        else:
            time.sleep(1)
    elif choice_key == 'Télécharger une catégorie':
        print("")
        print("Veuillez choisir la catégorie à télécharger")
        print("")
        for i, option_category in enumerate(options_categories.keys()):
                    print(f"{i + 1}. {option_category}")
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_value = list(options_categories.values())[choice - 1]
        choosen_source = choosen_value['source']
        choosen_category = choosen_value['category']
        choosen_function = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['function_name']
        choosen_generated = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['generated']

        if(choosen_category == 'agregation_complet'):
            # Attention, dans ce cas les données à télécharger ne sont pas celles stockées, il faut préalablement les reconstituer
            # Chargement de toutes les données incomplètes
            print("* DÉBUT DU CHARGEMENT DES DONNÉES AGREGATION PARTIELLES *")             
            choosen_dependances = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['dependances']
            for choosen_dependance in choosen_dependances:
                categorie_dependance = SOURCE_SPECS[choosen_dependance['source']]['categories'][choosen_dependance['category']]
                if(len(categorie_dependance['generated']) != 0):
                    if(categorie_dependance['generated'][0] not in donnees):
                        print("* DÉBUT DU CHARGEMENT DES DONNÉES DES OUTILS NÉCESSAIRES *")
                        load_datas(categorie_dependance['generated'], verbose=False)
                        print("* FIN DU CHARGEMENT DES DONNÉES DES OUTILS NÉCESSAIRES *")
                            
                print("* FIN DU CHARGEMENT DES DONNÉES AGREGATION PARTIELLES*")
                print("* DÉBUT GÉNÉRATION DES DONNÉES AGREGATION PARTIELLES *")
                generate_data_agreged(verbose=False)
                print("* FIN GÉNÉRATION DES DONNÉES AGREGATION PARTIELLES *")
                print("* DÉBUT DU TÉLÉCHARGEMENT DES DONNÉES AGREGATION TOTAL *")
                download_data_agreged(verbose=False)
                print("* FIN DU TÉLÉCHARGEMENT DES DONNÉES AGREGATION TOTAL *")

        else :
            download_datas(choosen_generated, verbose=False)
    elif choice_key == "Générer une catégorie":
        print("")
        print("Veuillez choisir la catégorie à générer")
        print("Note : le script se charge d'identifier les données à charger pour la génération de cette catégorie")
        print("")
        for i, option_category in enumerate(options_categories.keys()):
                    print(f"{i + 1}. {option_category}")

        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_value = list(options_categories.values())[choice - 1]
        choosen_source = choosen_value['source']
        choosen_category = choosen_value['category']
        choosen_function = eval(str(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['function_name']))
        choosen_dependances = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['dependances']

        # Vérification que toutes les données sont présentes pour la catégorie courante
        error_code_findable, error_message_findable = test_all_findable_for_category(choosen_category)
        print(error_message_findable)
        
        if(error_code_findable == 0):
            for choosen_dependance in choosen_dependances:
                categorie_dependance = SOURCE_SPECS[choosen_dependance['source']]['categories'][choosen_dependance['category']]
                if(len(categorie_dependance['generated']) != 0):

                    # on check si tous les fichiers requis sont bien présents, sinon on arrête et on fournis la liste des absents.
                    errors = check_existing_files(categorie_dependance['generated'])
                    if(errors == 1):
                        break
                    
                    if(categorie_dependance['generated'][0] not in donnees):
                        print("* DÉBUT DU CHARGEMENT DES OUTILS DE LA CATÉGORIE", choosen_dependance['category']," *")
                        load_datas(categorie_dependance['generated'], verbose=False)
                        print("* FIN DU CHARGEMENT DES OUTILS DE LA CATÉGORIE", choosen_dependance['category']," *")
            
            if(choosen_category == 'agregation_complet'):
                # Si on a choisi de générer agregation_complet, il faut aussi load les données agrégées complètes
                generate_data_agreged(verbose=False)
                download_data_agreged(verbose=False)
            elif(choosen_category == 'test'):
                print("* DÉBUT DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                load_datas(SOURCE_SPECS['outils']['categories'][choosen_category]['entrepot_dependances'], verbose=False)
                load_ref()
                print("* FIN DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                print("* DÉBUT DU CHARGEMENT DES DONNÉES EXTERNES *")
                load_datas(SOURCE_SPECS['outils']['external_data']['tables'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['path'])
                print("* CHARGEMENT DES DONNÉES SPATIALES EXTERNES *")
                load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['geojson'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='json')
                load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['geopackage'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='gpkg')
                load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['csv_geo'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='csv')
                print("* FIN DU CHARGEMENT DES DONNÉES EXTERNES*")

                print("* DÉBUT GÉNÉRATION ", choosen_source, choosen_category," *")
                choosen_function()
                if(TYPE == 'distant'):
                    download_datas(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['generated'])
                print("* FIN GÉNÉRATION ", choosen_source, choosen_category," *")
            else :
                # on vérifie que les données n'ont pas été déjà chargées
                if('domaine' not in donnees):
                    print("* DÉBUT DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                    load_datas_entrepot(
                        list(SOURCE_SPECS['entrepot']['tables'].keys()), 
                        verbose=False,
                        need_perf=(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['need_performance']=="True")
                    )
                    load_ref()
                    print("* FIN DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                    print("* DÉBUT DU CHARGEMENT DES DONNÉES EXTERNES *")
                    load_datas(SOURCE_SPECS['outils']['external_data']['tables'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['path'])
                    print("* CHARGEMENT DES DONNÉES SPATIALES EXTERNES *")
                    load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['geojson'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='json')
                    load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['geopackage'], verbose=False, path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='gpkg')
                    load_datas(SOURCE_SPECS['outils']['external_data']['geospatial_data']['csv_geo'], verbose=False,path_data=SOURCE_SPECS['outils']['external_data']['geospatial_data']['geodata_path'], file_format='csv')
                    print("* FIN DU CHARGEMENT DES DONNÉES EXTERNES*")
                    
                print("* DÉBUT GÉNÉRATION ", choosen_source, choosen_category," *")
                choosen_function()
                if(TYPE == 'distant'):
                    download_datas(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['generated'])
                print("* FIN GÉNÉRATION ", choosen_source, choosen_category," *")

    elif choice_key == 'Tester la cohérence des données externes':
        print("* DÉBUT DU TEST DE COHÉRENCE DES DONNÉES EXTERNES *")
        tables_to_check = SOURCE_SPECS['outils']['external_data']['tables']
        leaking_tables_ext = check_files_exist(
            tables_to_check, 
            path_data=SOURCE_SPECS['outils']['external_data']['path']
        )
        if len(leaking_tables_ext) != 0:
            print(f"{Fore.RED} Attention : certaines tables externes sont absentes. Elles NE SONT PAS vérifiées(",str(leaking_tables_ext),f"){Style.RESET_ALL}")
            
        if len(tables_to_check) > len(leaking_tables_ext):
            error_code_check, error_message_check = test_check_external_data(leaking_tables = leaking_tables_ext)
            print(error_message_check)

        print("* FIN DU TEST DE COHÉRENCE DES DONNÉES EXTERNES *")

    elif choice_key == "Test":
        print("* DÉBUT DE LA GÉNÉRATION TEST *")
        create_category_restructuration()
        print("* FIN DE LA GÉNÉRATION TEST *")





