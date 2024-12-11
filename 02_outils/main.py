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
import psycopg2 as psycopg
from scripts import nettoyage
from scripts import restructuration 
from scripts import indicateur
from scripts import agregation
from scripts import interoperabilite
from scripts import outils_can
from sqlalchemy import create_engine
import pandas as pd
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
EXTERNAL_DATA_PATH = 'data/external_data/'
VERSION = __version__
with open('../00_config/specs.json', encoding='utf8') as json_file:
    SOURCE_SPECS = json.load(json_file)

if(DEBUG):
    NROWS = int(config.get('debug', 'nrows'))
    DATA_PATH = config.get('debug', 'data_test_path')

path_metadata = 'data/metadonnees_tests.csv'
df_metadata = pd.read_csv(path_metadata)

if(TYPE == 'distant'):
    # On se connecte à la BDD seulement si l'utilisateur veut déclarer à distance
    DB_HOST = config.get(BDD_ENTREPOT, 'host')
    DB_PORT = config.get(BDD_ENTREPOT, 'port')
    DB_NAME_ENTREPOT = config.get(BDD_ENTREPOT, 'database')
    DB_USER = config.get(BDD_ENTREPOT, 'user')
    DB_PASSWORD = urllib.parse.quote(config.get(BDD_ENTREPOT, 'password'))
    DATABASE_URI_entrepot = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_ENTREPOT}'

    print(DB_USER, DB_PASSWORD, DATABASE_URI_entrepot)

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
    print("* CRÉATION TABLE ",name, " TERMINEE *")

donnees = {}
external_data = {}

def import_df(df_name, path_data, sep):
    """
        importe un dataframe au chemin path_data+df_name+'.csv' et le stock dans le dictionnaire 'df' à la clé df_name
    """
    global donnees
    if(DEBUG):
        donnees[df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep, low_memory=False, nrows=NROWS).replace({'\r\n': '\n'}, regex=True)
    else:
        donnees[df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep, low_memory=False).replace({'\r\n': '\n'}, regex=True)

# FAIRE UN IMPORT DF POUR EXTERNAL DATA !

def import_dfs(df_names, data_path, sep = ',', verbose=False):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans la liste df_names
    """
    global donnees
    pbar = tqdm(df_names)
    for df_name in pbar:
        pbar.set_description(f"Import de {df_name}")
        import_df(df_name, data_path, sep)


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

def load_datas(desired_tables, verbose=False, path_data=DATA_PATH):
    """ permet de chager les tables dans la variable globale donnees"""
    global donnees
    import_dfs(desired_tables, path_data, verbose=True)


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
    df1 = donnees['utilisation_intrant_realise_agrege']
    df2 = donnees['action_realise_manquant_agrege']
    donnees['action_realise_agrege'] = generate_leaking_df(df1, df2, 'action_realise_id', columns_difference = ['id'])
    donnees['action_realise_agrege'] = donnees['action_realise_agrege'].reset_index()

    # Génération de action_synthétisé_agrege
    df1 = donnees['utilisation_intrant_synthetise_agrege']
    df2 = donnees['action_synthetise_manquant_agrege']
    donnees['action_synthetise_agrege'] = generate_leaking_df(df1, df2, 'action_synthetise_id', columns_difference = ['id'])
    donnees['action_synthetise_agrege'] = donnees['action_synthetise_agrege'].reset_index()

    # Génération de intervention_realise_agrege
    df1 = donnees['utilisation_intrant_realise_agrege']
    df2 = donnees['intervention_realise_manquant_agrege']
    donnees['intervention_realise_agrege'] = generate_leaking_df(df1, df2, 'intervention_realise_id', columns_difference = ['id', 'action_realise_id'])
    donnees['intervention_realise_agrege'] = donnees['intervention_realise_agrege'].reset_index()

    # Génération de intervention_synthetise_agrege
    df1 = donnees['utilisation_intrant_synthetise_agrege']
    df2 = donnees['intervention_synthetise_manquant_agrege']
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


def check_existing_tables(desired_tables):
    """vérifie que toutes les tables sont présentes"""
    code_error = 0
    for table in desired_tables : 
        file_path = DATA_PATH+table+'.csv'
        if(not os.path.isfile(file_path)):
            print(f"- fichier {Fore.RED}"+file_path+f"{Style.RESET_ALL} manquant") 
            code_error = 1
    return code_error

def create_category_nettoyage():
    """
        Execute les requêtes pour créer les outils de nettoyage
    """
    # nettoyage_intervention_realise
    name_table = 'intervention_realise'
    df_nettoyage_intervention_realise = nettoyage.nettoyage_intervention(donnees, path_metadata='data/')

    export_to_db(df_nettoyage_intervention_realise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_intervention_realise.to_csv('entrepot_'+name_table+'_nettoyage.csv')

    # nettoyage_utilisation_intrant_realise
    name_table = 'utilisation_intrant_realise'
    df_nettoyage_utilisation_intrant_realise = nettoyage.nettoyage_utilisation_intrant(donnees, saisie='realise', verbose=False, path_metadata='data/')

    export_to_db(df_nettoyage_utilisation_intrant_realise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_utilisation_intrant_realise.to_csv(prefixe_source+suffixe_table+'_realise.csv')

    # nettoyage_utilisation_intrant_synthetise
    name_table = 'utilisation_intrant_synthetise'
    df_nettoyage_utilisation_intrant_synthetise = nettoyage.nettoyage_utilisation_intrant(donnees, saisie='synthetise', verbose=False, path_metadata='data/')

    export_to_db(df_nettoyage_utilisation_intrant_synthetise, 'entrepot_'+name_table+'_nettoyage')
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

    # permet d'obtenir des tables agrégées pour avoir les niveaux supérieurs depuis les niveaux fins (raccourcis)
    aggreged_utilisation_intrant_realise = agregation.get_aggreged_from_utilisation_intrant_realise(
        donnees
    )
    export_to_db(aggreged_utilisation_intrant_realise, 'entrepot_utilisation_intrant_realise_agrege')

    
    # toutes les infos manquantes agrégées depuis l'action
    aggreged_leaking_action_realise = agregation.get_leaking_aggreged_from_action_realise(
        aggreged_utilisation_intrant_realise, donnees
    )
    export_to_db(aggreged_leaking_action_realise, 'entrepot_action_realise_manquant_agrege')

    aggreged_leaking_action_synthetise = agregation.get_leaking_aggreged_from_action_synthetise(
        aggreged_utilisation_intrant_synthetise, donnees
    )
    export_to_db(aggreged_leaking_action_synthetise, 'entrepot_action_synthetise_manquant_agrege')


    # toutes les infos manquantes agrégées depuis l'intervention 
    aggreged_leaking_intervention_realise = agregation.get_leaking_aggreged_from_intervention_realise(
        aggreged_utilisation_intrant_realise, donnees
    )
    export_to_db(aggreged_leaking_intervention_realise, 'entrepot_intervention_realise_manquant_agrege')

    aggreged_leaking_intervention_synthetise = agregation.get_leaking_aggreged_from_intervention_synthetise(
        aggreged_utilisation_intrant_synthetise, donnees
    )
    export_to_db(aggreged_leaking_intervention_synthetise, 'entrepot_intervention_synthetise_manquant_agrege')

def create_category_restructuration():
    """
        Execute les requêtes pour créer les outils de restructuration
    """
    df_noeuds_synthetise_restructured = restructuration.restructuration_noeuds_synthetise(donnees)
    export_to_db(df_noeuds_synthetise_restructured, 'entrepot_noeuds_synthetise_restructure')

    df_connection_synthetise_restructured = restructuration.restructuration_connection_synthetise(donnees)
    export_to_db(df_connection_synthetise_restructured, 'entrepot_connection_synthetise_restructure')

    df_noeuds_realise_restructured = restructuration.restructuration_noeuds_realise(donnees)
    export_to_db(df_noeuds_realise_restructured, 'entrepot_noeuds_realise_restructure')
    
    df_noeuds_realise_restructured = restructuration.restructuration_recolte_rendement_prix(donnees)
    export_to_db(df_noeuds_realise_restructured, 'entrepot_recolte_rendement_prix_restructure')

    df_plantation_perenne_synthetise_restructured = restructuration.restructuration_plantation_perenne_synthetise(donnees)
    export_to_db(df_plantation_perenne_synthetise_restructured, 'entrepot_plantation_perenne_synthetise_restructure')

    # Attention, en suivant parfaitement la convention de nommage, on aboutit à des noms de tables trop longs pour être pris en charge
    # par Postgres en tant que nom de table (taille maximum : 63), on raccourci donc : "composant_culture_concerne" en "ccc"
    df_composant_culture_concerne_intervention_synthetise_restructured = \
        restructuration.restructuration_composant_culture_concerne_intervention_synthetise(donnees)
    export_to_db(
        df_composant_culture_concerne_intervention_synthetise_restructured,
        'entrepot_ccc_intervention_synthetise_restructure'
    )

    df_intervention_synthetise_restructure = restructuration.restructuration_intervention_synthetise(donnees)
    export_to_db(df_intervention_synthetise_restructure, 'entrepot_intervention_synthetise_restructure')

def create_category_indicateur():
    """
        Execute les requêtes pour créer les outils des indicateurs
    """
    df_utilsation_intrant_indicateur = indicateur.indicateur_utilisation_intrant(donnees)
    export_to_db(df_utilsation_intrant_indicateur, 'entrepot_utilisation_intrant_indicateur')
    
    df_sdc_donnee_attendue = indicateur.sdc_donnee_attendue(donnees)
    export_to_db(df_sdc_donnee_attendue, 'entrepot_sdc_donnee_attendue')

def create_category_interoperabilite():
    """
        Execute les requêtes pour créer les outils d'interopérabilité
    """
    df_donnees_spatiales = interoperabilite.create_donnees_spatiales(donnees, external_data)
    export_to_db(df_donnees_spatiales, 'entrepot_donnees_spatiales')


def create_category_outils_can():
    """
        Execute les requêtes pour créer le source des outils utiles pour la génération des csv CAN
    """
    # création de l'outil permettant de filtrer les entités (dispositifs)
    df_dispositif_filtres_outils_can = outils_can.dispositif_filtres_outils_can(donnees)
    df_dispositif_filtres_outils_can.set_index('id', inplace=True)
    export_to_db(df_dispositif_filtres_outils_can, 'entrepot_dispositif_filtres_outils_can')

    # création de l'outil permettant de filtrer les entités (domaine)
    df_domaine_filtres_outils_can = outils_can.domaine_filtres_outils_can(donnees)
    df_domaine_filtres_outils_can.set_index('id', inplace=True)
    export_to_db(df_domaine_filtres_outils_can, 'entrepot_domaine_filtres_outils_can')

    df_parcelle_non_ratachee_outils_can = outils_can.get_parcelles_non_rattachees_outils_can(donnees)
    df_parcelle_non_ratachee_outils_can.set_index('id', inplace=True)
    export_to_db(df_parcelle_non_ratachee_outils_can, 'entrepot_parcelle_non_rattachee_outils_can')

    df_culture_outils_can = outils_can.get_culture_outils_can(donnees)
    df_culture_outils_can.set_index('id', inplace=True)
    export_to_db(df_culture_outils_can, 'entrepot_culture_outils_can')

    df_intervention_realise_outils_can = outils_can.get_intervention_realise_outils_can(donnees)
    df_intervention_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_intervention_realise_outils_can, 'entrepot_intervention_realise_outils_can')

    df_intervention_synthetise_outils_can = outils_can.get_intervention_synthetise_outils_can(donnees)
    df_intervention_synthetise_outils_can.set_index('id', inplace=True)
    export_to_db(df_intervention_synthetise_outils_can, 'entrepot_intervention_synthetise_outils_can')

    df_recolte_outils_can = outils_can.get_recolte_outils_can(donnees)
    export_to_db(df_recolte_outils_can, 'entrepot_recolte_outils_can')

    df_zone_outils_can = outils_can.get_zone_realise_outils_can(donnees)
    df_zone_outils_can.set_index('id', inplace=True)
    export_to_db(df_zone_outils_can, 'entrepot_zone_realise_outils_can')

    df_sdc_realise_outils_can = outils_can.get_sdc_realise_outils_can(donnees)
    df_sdc_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_sdc_realise_outils_can, 'entrepot_sdc_realise_outils_can')

    df_parcelle_realise_outils_can = outils_can.get_parcelle_realise_outils_can(donnees)
    df_parcelle_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_parcelle_realise_outils_can, 'entrepot_parcelle_realise_outils_can')


def create_category_test():
    """ 
            Execute les requêtes pour tester la génération d'outils spécifiques
    """
    df_intervention_realise_outils_can = outils_can.get_intervention_realise_outils_can(donnees)
    df_intervention_realise_outils_can.set_index('id', inplace=True)
    export_to_db(df_intervention_realise_outils_can, 'entrepot_intervention_realise_outils_can')

entrepot_spec = {
    'tables' : [
        'semence', 'plantation_perenne_phases_realise', 'plantation_perenne_phases_synthetise', 'modele_decisionnel', 
        'composant_culture_concerne_intervention_synthetise', 'domaine', 'dispositif', 'modele_decisionnel_maitrise', 
        'modele_decisionnel_strategie', 'modele_decisionnel_strategie_culture', 'plantation_perenne_realise', 
        'intervention_realise_performance', 'intervention_synthetise_performance', 
        'bilan_campagne_regional_pressionbioagresseur', 'bilan_campagne_regional_generalites', 'coordonnees_gps_domaine', 
        'utilisation_intrant_performance', 'zone_realise_performance', 'intrant', 'composant_culture', 'culture', 
        'atelier_elevage', 'intervention_synthetise', 'commune', 'noeuds_realise', 'noeuds_synthetise', 
        'connection_synthetise', 'intervention_realise', 'combinaison_outil_action', 'domaine_sol', 
        'parcelle_type_voisinage', 'parcelle_type_zonage', 'parcelle_voisinage', 'parcelle_zonage', 'action_synthetise', 
        'action_realise', 'synthetise_synthetise_performance', 'sdc_realise_performance', 'parcelle_realise_performance', 
        'domaine_surface_especes_cultivees', 'sole_realise', 'connection_realise', 'composition_substance_active_numero_amm', 
        'utilisation_intrant_realise', 'parcelle', 'synthetise', 'zone', 'sdc', 'plantation_perenne_synthetise', 
        'utilisation_intrant_synthetise', 'materiel', 'combinaison_outil', 'combinaison_outil_materiel', 
        'utilisation_intrant_cible', 'parcelle_type', 'recolte_rendement_prix', 'itk_realise_performance', 
        'composant_culture_concerne_intervention_realise', 'bilan_campagne_sdc_generalites', 'espece', 
        'intervention_travail_edi', 'variete', 'acta_groupe_culture', 'acta_substance_active', 'acta_traitement_produit',
        'composant_action_semis', 'reseau', 'liaison_sdc_reseau', 'liaison_reseaux', 'nuisible_edi', 'adventice', 'groupe_cible'
    ]
}

external_data_spec = {
    'tables' : [
        'BDD_donnees_attendues_CAN'
    ]
}

# à terme, cet ordre devra être généré automatiquement à partir des dépendances --> mais pour l'instant plus simple comme ça
steps = [
    {'source' : 'outils', 'categorie' : 'nettoyage'},
    {'source' : 'outils', 'categorie' : 'agregation'},
    {'source' : 'outils', 'categorie' : 'agregation_complet'},
    {'source' : 'outils', 'categorie' : 'restructuration'},
    {'source' : 'outils', 'categorie' : 'indicateur'},
    {'source' : 'outils', 'categorie' : 'outils_can'}
]

options_categories = {}

for source_key, source in SOURCE_SPECS.items():
    if(source_key != 'entrepot'):
        for categorie_key in source['categories']:
            options_categories[categorie_key +' ('+ source_key+')'] = {'source' : source_key, 'categorie' : categorie_key}
            categorie = source['categories'][categorie_key]
            dependances = categorie['dependances']

history = []


options = {
    'local' : {
        "Tout générer" : [],
        "Générer une catégorie" : [],  
        "Quitter" : []
    },
    'distant' : {
        "Tout générer" : [],
        "Générer une catégorie" : [],  
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
        if(TYPE == 'distant'):
            print("* TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
            download_datas(list(SOURCE_SPECS['entrepot']['tables'].keys()), verbose=False)
        print("* CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        load_datas(list(SOURCE_SPECS['entrepot']['tables'].keys()), verbose=False)
        print("* CHARGEMENT DES DONNÉES EXTERNES *")
        load_datas(external_data_spec['tables'], verbose=False, path_data=EXTERNAL_DATA_PATH)
        print("* CHARGEMENT DES RÉFÉRENTIELS *")
        print("Attention, penser à les mettre à jour manuellement.")
        load_ref()

        for step in steps :
            current_source = step['source']
            current_category = step['categorie']
            print("* GÉNÉRATION ", current_source, current_category," *")
            choosen_function = eval(str(SOURCE_SPECS[current_source]['categories'][current_category]['function_name']))

            if(current_category == 'agregation_complet'):
                # Lors de la génération de agregation_complet, il faut aussi créer les dataframes.
                generate_data_agreged(verbose=False)
                download_data_agreged(verbose=False)
            else :
                choosen_function()
                if(TYPE == 'distant'):
                    download_datas(SOURCE_SPECS[current_source]['categories'][current_category]['generated'])
                load_datas(SOURCE_SPECS[current_source]['categories'][current_category]['generated'])

    elif choice_key == 'Télécharger une catégorie':
        print("")
        print("Veuillez choisir la catégorie à télécharger")
        print("")
        for i, option_category in enumerate(options_categories.keys()):
                    print(f"{i + 1}. {option_category}")
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_value = list(options_categories.values())[choice - 1]
        choosen_source = choosen_value['source']
        choosen_category = choosen_value['categorie']
        choosen_function = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['function_name']
        choosen_generated = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['generated']

        if(choosen_category == 'agregation_complet'):
            # Attention, dans ce cas les données à télécharger ne sont pas celles stockées, il faut préalablement les reconstituer
            # Chargement de toutes les données incomplètes
            print("* DÉBUT DU CHARGEMENT DES DONNÉES AGREGATION PARTIELLES *")             
            choosen_dependances = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['dependances']
            for choosen_dependance in choosen_dependances:
                categorie_dependance = SOURCE_SPECS[choosen_dependance['source']]['categories'][choosen_dependance['categorie']]
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
        choosen_category = choosen_value['categorie']
        print(str(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['function_name']))
        choosen_function = eval(str(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['function_name']))
        choosen_dependances = SOURCE_SPECS[choosen_source]['categories'][choosen_category]['dependances']
        for choosen_dependance in choosen_dependances:
            categorie_dependance = SOURCE_SPECS[choosen_dependance['source']]['categories'][choosen_dependance['categorie']]
            if(len(categorie_dependance['generated']) != 0):

                # on check si tous les fichiers requis sont bien présents, sinon on arrête et on fournis la liste des absents.
                errors = check_existing_tables(categorie_dependance['generated'])
                if(errors == 1):
                    break
                
                if(categorie_dependance['generated'][0] not in donnees):
                    print("* DÉBUT DU CHARGEMENT DES DONNÉES DES OUTILS NÉCESSAIRES *")
                    load_datas(categorie_dependance['generated'], verbose=False)
                    print("* FIN DU CHARGEMENT DES DONNÉES DES OUTILS NÉCESSAIRES *")
        
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
            load_datas(external_data_spec['tables'], verbose=False, path_data=EXTERNAL_DATA_PATH)
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
                load_datas(list(SOURCE_SPECS['entrepot']['tables'].keys()), verbose=False)
                load_ref()
                print("* FIN DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                print("* DÉBUT DU CHARGEMENT DES DONNÉES EXTERNES *")
                load_datas(external_data_spec['tables'], verbose=False, path_data=EXTERNAL_DATA_PATH)
                print("* FIN DU CHARGEMENT DES DONNÉES EXTERNES*")
                
            print("* DÉBUT GÉNÉRATION ", choosen_source, choosen_category," *")
            choosen_function()
            if(TYPE == 'distant'):
                download_datas(SOURCE_SPECS[choosen_source]['categories'][choosen_category]['generated'])
            print("* FIN GÉNÉRATION ", choosen_source, choosen_category," *")


    elif choice_key == "Test":
        print("* DÉBUT DE LA GÉNÉRATION TEST *")
        create_category_restructuration()
        print("* FIN DE LA GÉNÉRATION TEST *")





