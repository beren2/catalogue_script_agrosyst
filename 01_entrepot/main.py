"""
    Script permettant la génération de l'entrepôt de données
"""
#!/usr/bin/python
import configparser
import urllib
import datetime
import subprocess 
import os
import json
import psycopg2 as psycopg
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import inspect
from colorama import Fore, Style
from version import __version__
from tqdm import tqdm

#Fetch the sql files 
path_sql_files = 'scripts/'

#Obtenir les paramètres de configuration
config = configparser.ConfigParser()
config.read(r'../00_config/config.ini')

TYPE = config.get('metadata', 'type')
BDD_ENTREPOT = config.get('metadata', 'bdd_entrepot')
VERSION = __version__
DEBUG = bool(int(config.get('metadata', 'debug')))
DATA_PATH = config.get('metadata', 'data_path') 

if(DEBUG):
    NROWS = int(config.get('debug', 'nrows'))
    DATA_PATH = config.get('debug', 'data_test_path')

# La db de l'entrepot
DB_HOST_ENTREPOT = config.get(BDD_ENTREPOT, 'host')
DB_PORT = config.get(BDD_ENTREPOT, 'port')
DB_NAME_ENTREPOT = config.get(BDD_ENTREPOT, 'database')
DB_USER = config.get(BDD_ENTREPOT, 'user')
DB_PASSWORD = urllib.parse.quote(config.get(BDD_ENTREPOT, 'password'))
DATABASE_URI_entrepot = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_ENTREPOT}:{DB_PORT}/{DB_NAME_ENTREPOT}'

#Créer la connexion pour sqlalchemy (pour executer des requetes : uniquement pour l entrepot)
conn = psycopg.connect(user = DB_USER,
                password = config.get(BDD_ENTREPOT, 'password'),
                host = DB_HOST_ENTREPOT,
                port = DB_PORT,
                database = DB_NAME_ENTREPOT)

cur = conn.cursor()

# La db de datagrosyst
DB_HOST = config.get('datagrosyst', 'host')
DB_PORT = config.get('datagrosyst', 'port')
DB_NAME = config.get('datagrosyst', 'database')
DB_USER = config.get('datagrosyst', 'user')
DB_PASSWORD = urllib.parse.quote(config.get('datagrosyst', 'password'))
DATABASE_URI_datagrosyst = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# On vérifie que le fichier de versionning est initialisé
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

def copy_table_to_csv(table_name, csv_path, csv_name):
    """
        Permet de copier une table depuis la base de donnée distance dans un fichier local csv_path+csv_name.csv
        + Parse le fichier local de contrôle de versions de fichiers et le met à jour en fonction de la version local
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

def check_existing_table_database(tables_to_check,schema):
    """
        Vérifie si les tables en argument sont bien présentes dans la base de données de l'entrepot
    """
    list_table = ['entrepot_' + t for t in tables_to_check]
    tables_not_exists = [t.replace("entrepot_","") for t in list_table if t not in schema]
    
    if len(tables_not_exists) > 0:
        print(f"{Fore.RED} ATTENTION DES TABLES SONT NON EXISTANTES EN BASE : "f"{Style.RESET_ALL}") 
    for current_table in tables_not_exists:
        print(f"{Fore.RED} - " + current_table + f"{Style.RESET_ALL}") 

    return(tables_not_exists)


ordered_files = [
    "commune",
    "espece",
    "intervention_travail_edi",
    "criteres_selection",
    "domaine",
    "coordonees_gps_domaine",
    "dispositif",
    "sdc",
    "parcelle",
    "zone",
    "parcelle_type",
    "synthetise",
    "culture",
    "materiel",
    "combinaison_outil",
    "composant_culture",
    "atelier_elevage",
    "bilan_campagne_regional",
    "modele_decisionnel",
    "sole_realise",
    "cycle_culture_realise",
    "cycle_culture_synthetise",
    "plantation_perenne_realise",
    "plantation_perenne_synthetise",
    "intervention_realise",
    "composant_culture_concerne_intervention",
    "intervention_synthetise",
    "action_realise",
    "action_synthetise",
    "intrant",
    "semence",
    "utilisation_intrant_realise",
    "utilisation_intrant_synthetise",
    "utilisation_intrant_cible",
    "precision_espece_semis",
    "variete",
    "utilisation_intrant_performance",
    "intervention_realise_performance",
    "zone_realise_performance",
    "parcelle_realise_performance",
    "sdc_realise_performance",
    "itk_realise_performance",
    "intervention_synthetise_performance",
    "synthetise_synthetise_performance",
    "recolte",
    "acta_groupe_culture",
    "acta_substance_active",
    "acta_traitement_produit",
    "acta_dosage_spc",
    "bilan_campagne_sdc",
    'composition_substance_active_numero_amm',
    'composant_action_semis',
    'reseau',
    'liaison_reseaux',
    'liaison_sdc_reseau',
    "critere_qualite_valorisation",
    "destination_valorisation",
    "dose_ref_par_groupe_cible",
    "groupe_cible",
    "nuisible_edi",
    "substances_actives_europeennes",
    "phrases_de_risque_numero_amm",
    "composition_substance_active_numero_amm",
    "prix_intrant_produit_phyto_sanitaire",
    "prix_carburant",
    "otex",
    "variete_plante_grappe",
    "station_meteo",
    "levier",
    "texture_sol",
    "fertilisation_organique",
    "fertilisation_minerale",
    "groupe_cible",
    "adventice"
]


options = {
        "Génération de toutes les données de l'entrepôt" : [],
        "Génération de certaines données de l'entrepôt" : [],  
        "Vérification cohérence colonnes existantes tables et documentation" : [],  
        "Création d'une nouvelle base de données entrepôt nettoyée" : [],
        "Mettre à jour les métadonnées de Datagrosyst" : [],
        "Téléchargement de l'entrepôt" : [],
        "Quitter" : []
}


while True:
    print("")
    print("")
    print("**************** Interface de gestion de l'entrepôt ****************")
    print("")
    print("      version :      ("+VERSION+")            ")
    print("      type :         ("+TYPE+")               ")
    print("      debug :        ("+str(DEBUG)+")         ")
    print("      repertoire :   ("+DATA_PATH+")         ")
    print("      nom BDD :      ("+DB_NAME_ENTREPOT+")         ") 
    print("      serveur BDD :  ("+DB_HOST_ENTREPOT+")         ") 
    print("")
    print("********************************************************************")
    print("")
    print("Veuillez choisir une option parmi les suivantes :")
    print("")
    for i, option in enumerate(options.keys()):
        print(f"{i + 1}. {option}")
    
    try:
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
    except ValueError:
        choice = 6

    choice_key = list(options.keys())[choice - 1]
    
    if choice_key == "Quitter":
        print("Au revoir !")
        break
    if(choice_key == "Génération de toutes les données de l'entrepôt"):

        #Nettoyage de l'environnement de travail (suppression de toutes les tables commençant par entrepot_)
        
        # Récupération des informations sur les tables existantes
        engine_entrepot = create_engine(DATABASE_URI_entrepot)
        #metadata = MetaData(bind=engine_entrepot)
        inspector = inspect(engine_entrepot)
        schemas = inspector.get_schema_names()

        print("")
        print("NETTOYAGE DE LA BASE DE DONNÉES ("+DB_NAME_ENTREPOT+", "+DB_HOST_ENTREPOT+")")
        print("--")
        for current_table_name in inspector.get_table_names(schema='public'):
            associated_file_name = "_".join(current_table_name.split('_')[1:])
            if(current_table_name.startswith('entrepot_')):
                print(f"- Suppression de la table : {Fore.RED}"+current_table_name+f"{Style.RESET_ALL}")           
                drop_request = "DROP TABLE IF EXISTS "+current_table_name+" CASCADE"
                cur.execute(drop_request)
        print("")
        print("GÉNÉRATION DES TABLES DE L'ENTREPÔT :")
        print("--")
        #Obtention des fichiers sql
        for i, ordered_file in enumerate(ordered_files):
            current_file = ordered_file+'.sql'

            print(f"- Maj entrepôt à partir du fichier: {Fore.YELLOW}"+current_file+f"{Style.RESET_ALL}")           
            print(datetime.datetime.now())
            
            extract_file = path_sql_files+current_file  

            if('sql' in extract_file):
                #Get the sql extract file
                with open(extract_file, "r", encoding="utf8") as file:
                    sql_extract = file.read()
                cur.execute(sql_extract)    
            conn.commit()
            print(f"{Fore.GREEN} Ok.{Style.RESET_ALL}")
            print(datetime.datetime.now())

    elif(choice_key == "Génération de certaines données de l'entrepôt"):
        print("")
        print("Veuillez table particulière à mettre à jour :")
        print("")

        for i, option in enumerate(ordered_files):
            print(f"{i + 1}. {option}")
        
        choice = int(input("Entrez le rang de votre choix : "))
        choice_key = list(ordered_files)[choice - 1]
        print("choice_key : ", choice_key)
        print(datetime.datetime.now())


         # Récupération des informations sur les tables existantes
        engine_entrepot = create_engine(DATABASE_URI_entrepot)
        #metadata = MetaData(bind=engine_entrepot)
        inspector = inspect(engine_entrepot)
        schemas = inspector.get_schema_names()

        print("")
        print("NETTOYAGE DE LA BASE DE DONNÉES ("+DB_NAME_ENTREPOT+", "+DB_HOST_ENTREPOT+")")
        print("--")
        print(f"- Suppression de la table : {Fore.RED}entrepot_"+choice_key+f"{Style.RESET_ALL}")           
        drop_request = "DROP TABLE IF EXISTS entrepot_"+choice_key+" CASCADE"
        cur.execute(drop_request)
        print("")
        print("GÉNÉRATION DES TABLES DE L'ENTREPÔT :")
        print("--")
        #Obtention des fichiers sql
        current_file = choice_key+'.sql'

        print(f"- Maj entrepôt à partir du fichier: {Fore.YELLOW}"+current_file+f"{Style.RESET_ALL}")           
        
        extract_file = path_sql_files+current_file  

        if('sql' in extract_file):
            #Get the sql extract file
            with open(extract_file, "r", encoding="utf8") as file:
                sql_extract = file.read()
            cur.execute(sql_extract)    
        conn.commit()
        print(f"{Fore.GREEN} Ok.{Style.RESET_ALL}")
        print(datetime.datetime.now())



    elif(choice_key == "Vérification cohérence colonnes existantes tables et documentation"):

        engine_datagrosyst = create_engine(DATABASE_URI_datagrosyst)
        postgreSQLConnection_datagrosyst = engine_datagrosyst.connect()

        engine_entrepot = create_engine(DATABASE_URI_entrepot)
        postgreSQLConnection_entrepot = engine_entrepot.connect()

        schema_tables = pd.read_sql( text("""select table_name from information_schema.tables where table_schema = 'public' and table_name like '%entrepot%'"""), postgreSQLConnection_entrepot) 
        entrepot_table = pd.read_sql("select id,label,explication,category_id,is_active from entrepot_table", postgreSQLConnection_datagrosyst) 

        schema_columns = pd.read_sql( text("""select table_name, column_name from information_schema.columns where table_schema = 'public' and table_name like '%entrepot%'"""), postgreSQLConnection_entrepot) 
        entrepot_columns = pd.read_sql("select id,label,explication,sensible_column,table_id,is_active,foreign_key_table from entrepot_column", postgreSQLConnection_datagrosyst) 

        # mettre en minuscule les labels des tables de description
        entrepot_columns['label'] = entrepot_columns['label'].str.lower()

        # Lignes obsoletes de description des tables dans "entrepot_table"
        table_not_exist = pd.DataFrame(columns=['id','label','explication','category_id','is_active'])
        for t in range(0,entrepot_table.shape[0]):
            if "entrepot_"+entrepot_table.loc[t,'id'] not in schema_tables['table_name'].tolist():
                table_not_exist = pd.concat([table_not_exist,entrepot_table.loc[[t,]]], ignore_index=True)

        if table_not_exist.shape[0] > 0 :
            print(f"{Fore.RED} Erreur tables non existantes dans l'entrepot {Style.RESET_ALL}")
            print(table_not_exist)
        else :
            print(f"{Fore.GREEN} Ok : toutes les tables documentées existent {Style.RESET_ALL}")

        # Lignes obsoletes où la foreign key n'a pas de correspondance
        foreignkey_not_exist = pd.DataFrame(columns=['id','label','explication','sensible_column','table_id','is_active','foreign_key_table'])
        entrepot_columns_fk = entrepot_columns.dropna(subset=['foreign_key_table'], ignore_index=True)

        for t in range(0,entrepot_columns_fk.shape[0]):
            fk_list = entrepot_columns_fk.loc[t,'foreign_key_table'].split(', ')
            for i, fk in enumerate(fk_list) :
                if "entrepot_"+fk not in schema_tables['table_name'].tolist():
                    foreignkey_not_exist = pd.concat([foreignkey_not_exist,entrepot_columns_fk.loc[[t,]]], ignore_index=True)
                
        if foreignkey_not_exist.shape[0] > 0 :
            print(f"{Fore.RED} Erreur tables foreign_key non existantes dans l'entrepot {Style.RESET_ALL}")
            print(f"{Fore.RED} Attention, si il n'y a pas de fk, il faut que la valeur soit NULL pour la visualisation de l'entrepot :  Update entrepot_column set foreign_key_table = null where id = '' {Style.RESET_ALL}")
            print(foreignkey_not_exist[['id','foreign_key_table']])
        else :
            print(f"{Fore.GREEN} Ok : toutes foreign_key renseignées existent {Style.RESET_ALL}")

        # Lignes obsoletes de description des colonnes : "entrepot_columns"
        column_not_exist = pd.DataFrame(columns=['id','label','explication','sensible_column','table_id','is_active','foreign_key_table'])
        dict_table_columns = schema_columns.groupby("table_name")['column_name'].apply(list).to_dict()

        for t in list(dict_table_columns.keys()):
            entrepot_columns_onetable = entrepot_columns[entrepot_columns['table_id'] == t.split('entrepot_')[1]]          
            entrepot_columns_not_exist_subset = entrepot_columns_onetable[~entrepot_columns_onetable.label.isin(dict_table_columns.get(t))]
            
            column_not_exist = pd.concat([column_not_exist,entrepot_columns_not_exist_subset], ignore_index=True)
            
        if column_not_exist.shape[0] > 0 :
            print(f"{Fore.RED} Erreur documentation obsolete : colonnes non existantes dans l'entrepot {Style.RESET_ALL}")
            if column_not_exist.shape[0] > 20:
                print(f"{Fore.RED} Le nombre de lignes est supérieur à 20. Elles sont compilées dans ./documentation_obsolete.csv {Style.RESET_ALL}")
                column_not_exist.to_csv('./documentation_obsolete.csv') 
            else :
                print(column_not_exist[['id','label','explication','sensible_column','table_id','is_active','foreign_key_table']])
        else :
            print(f"{Fore.GREEN} Ok : toutes les colonnes documentées existent {Style.RESET_ALL}")

        
        # Lignes de description des colonnes manquantes
        descrip_col_not_exist = pd.DataFrame(columns=['table_name', 'column_name'])
        dict_table_columns = entrepot_columns.groupby("table_id")['label'].apply(list).to_dict()

        for t in list(dict_table_columns.keys()):
            sel = schema_columns[schema_columns['table_name'] == "entrepot_"+t]       
        
            descrip_col_not_exist = pd.concat([descrip_col_not_exist,sel[~sel.column_name.isin(dict_table_columns.get(t))]], ignore_index=True)
        
        if descrip_col_not_exist.shape[0] > 0 :
            print(f"{Fore.RED} Attention ! Documentation MANQUANTE pour certaines colonnes {Style.RESET_ALL}")
            if descrip_col_not_exist.shape[0] > 20:
                print(f"{Fore.RED} Le nombre de lignes manquantes est supérieur à 20. Elles sont compilées dans ./documentation_manquante.csv {Style.RESET_ALL}")
                descrip_col_not_exist.to_csv('./documentation_manquante.csv') 
            else :
                print(descrip_col_not_exist)
        else :
            print(f"{Fore.GREEN} Ok : toutes les colonnes sont documentées {Style.RESET_ALL}")
    elif (choice_key == "Création d'une nouvelle base de données entrepôt nettoyée"):
        print("Nom de la base de données originale (ex : export_perf...)")
        nom_origine = input()
        print("Nom de la base de données destination (ex : entrepot_20231115)")
        nom_final = input()
        os.environ['PGPASSWORD'] = config.get('datagrosyst', 'password')
        subprocess.run("""pg_dump -vFc --dbname="""+str(nom_origine)+""" --host=147.100.179.208 --no-blobs --port=5438  --username=dephygraph_admin --file="""+str(nom_origine)+""".dump""", shell=True, check=True)
        subprocess.run("""createdb """+str(nom_final)+""" -Udephygraph_admin -h147.100.179.208 -p5438""", shell=True, check=True)
        subprocess.run("""pg_restore -v -Udephygraph_admin -d"""+str(nom_final)+""" -h147.100.179.208 -p5438 """+str(nom_origine)+""".dump""", shell=True, check=True)
        #os.environ['PGPASSWORD'] = 'postgres'
        #subprocess.run("""pg_restore -v -Upostgres -d"""+str(nom_final)+""" -h127.0.0.1 -p5432 """+str(nom_origine)+""".dump""", shell=True, check=True)
        subprocess.run("""rm """+str(nom_origine)+""".dump""",  check=False)

        print("La nouvelle BDD est générée, pensez à mettre à jour le fichier config_files/connection/database_source.ini")
    
    elif(choice_key == "Mettre à jour les métadonnées de Datagrosyst"):
        # on met à jour les métadonnées de Datagrosyst sur de l'export courant.
        print("Date des exports courants (ex : 15/01/2024)")
        date = input()
        engine_datagrosyst = create_engine(DATABASE_URI_datagrosyst)
        postgreSQLConnection_datagrosyst = engine_datagrosyst.connect()
        transaction = postgreSQLConnection_datagrosyst.begin()
        try:
            postgreSQLConnection_datagrosyst.execute(text("UPDATE metadatas SET value = '"+str(date)+"' WHERE name='date_current_export_perso'"))
            transaction.commit()
        except Exception:
            transaction.rollback()
            raise
        
        print("Les métas-données de", DB_NAME, "sont à jour, pensez à mettre à jour le fichier de configuration du serveur (database.ini)")

    elif choice_key == "Téléchargement de l'entrepôt":
        engine_entrepot = create_engine(DATABASE_URI_entrepot) 
        postgreSQLConnection_entrepot = engine_entrepot.connect()
    
        schema_tables = pd.read_sql( text("""select table_name from information_schema.tables where table_schema = 'public' and table_name like '%entrepot%'"""), postgreSQLConnection_entrepot) 
        schema_tables = schema_tables['table_name'].values.tolist()
    
        tables = ['tout']
        tables += list(ordered_files)
        print("")
        print("Veuillez choisir la table à générer")
        print("")
        for i, option_table in enumerate(tables):
                    print(f"{i + 1}. {option_table}")
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_table = tables[choice - 1]

        no_existing_table = check_existing_table_database(ordered_files,schema_tables)

        print("* DÉBUT DU TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        if(choosen_table == 'tout') :
            for table in no_existing_table:
                ordered_files.remove(table)
            
            download_datas(ordered_files, verbose=False)
        else :
            if choosen_table not in no_existing_table:
                download_datas([choosen_table], verbose=False)
        print("* FIN DU TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")


cur.close()
conn.close()
