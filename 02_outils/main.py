"""
    Fichier principal d'obtention des données des différents magasin de données
    À exécuter lors d'une mise à jour des données sur Datagrosyst.
    
    Ce script effectue les tâches suivantes  :
    1) Import des données : téléchargement des données de l'entrepôt en utilisant la connexion POSTGRESSQL (si besoin)
    2) Exécution des scripts de pré-traitement (nettoyage)
    3) Enregistrement des résultats dans la base entrepôt (mais avec un suffixe propre aux bases considérées)
"""
import configparser
import urllib
import psycopg2 as psycopg
from scripts import nettoyage
from scripts import restructuration 
from scripts import indicateur
from scripts import agregation
from scripts import outils_can
from sqlalchemy import create_engine
import pandas as pd

#Obtenir les paramètres de connexion pour psycopg2
config = configparser.ConfigParser()
config.read(r'../00_config/config.ini')

# La db de l'entrepot
DB_HOST = config.get('entrepot', 'host')
DB_PORT = config.get('entrepot', 'port')
DB_NAME_ENTREPOT = config.get('entrepot', 'database')
DB_USER = config.get('entrepot', 'user')
DB_PASSWORD = urllib.parse.quote(config.get('entrepot', 'password'))
DATABASE_URI_entrepot = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_ENTREPOT}'

print(DB_USER, DB_PASSWORD, DATABASE_URI_entrepot)

#Créer la connexion pour sqlalchemy (pour executer des requetes : uniquement pour l entrepot)
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_ENTREPOT}')

# Establish a connection to PostgreSQL
conn = engine.raw_connection()
cur = conn.cursor()

DATA_PATH = '/home/bvuittenez/Bureau/utils/data/'
EXTERNAL_DATA_PATH = 'data/external_data/'
path_metadata = 'data/metadonnees_tests.csv'
df_metadata = pd.read_csv(path_metadata)


def export_to_entrepot(df, name):
    """ permet d'exporter un dataframe dans une table de l'entrepôt avec """
    df.to_sql(name=name, con=engine, if_exists='replace')
    print("* CRÉATION TABLE ",name, " TERMINEE *")

donnees = {}

def import_df(df_name, path_data, sep):
    """
        importe un dataframe au chemin path_data+df_name+'.csv' et le stock dans le dictionnaire 'df' à la clé df_name
    """
    global donnees
    # attention : si on importe des noms qui contienennt "manquant", il faut effectuer des opérations --> implique que les autres soient déjà chargés.
    # if(df_name == 'intervention_realise_manquant_agrege'):
    #     first = donnees['utilisation_intrant_realise_agrege'].drop_duplicates(subset=['intervention_realise_id'])
    #     second = pd.read_csv(path_data+df_name+'.csv', sep = sep, low_memory=False)
    #     donnees[df_name] = pd.concat([first, second], axis=1)
    # elif(df_name == 'intervention_synthetise_manquant_agrege'):
    #     first = donnees['utilisation_intrant_synthetise_agrege'].drop_duplicates(subset=['intervention_synthetise_id'])
    #     second = pd.read_csv(path_data+df_name+'.csv', sep = sep, low_memory=False)
    #     donnees[df_name] = pd.concat([first, second], axis=1)
    # else:
    donnees[df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep, low_memory=False)

def import_dfs(df_names, data_path, sep = ',', verbose=False):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans la liste df_names
    """
    global donnees
    for df_name in df_names:
        if(verbose):
            print("- ", df_name)
        import_df(df_name, data_path, sep)


def copy_table_to_csv(table_name, csv_path, csv_name):
    """
        Permet de copier une table depuis la base de donnée distance dans un fichier local csv_path+csv_name.csv
    """
    with psycopg.connect(DATABASE_URI_entrepot) as connection:
        cursor = connection.cursor()

        with open(csv_path+csv_name+".csv", "wb") as f:
            cursor.copy_expert("COPY "+table_name+" TO STDOUT WITH CSV DELIMITER ',' HEADER", file=f)

def copy_tables_to_csv(table_names, csv_path, verbose=False):
    """
        permet de copier un ensemble de tables depuis la base de données distance dans des fichiers local au csv_path
    """
    for table_name in table_names : 
        if(verbose) :
            print("- ", table_name)
        copy_table_to_csv('entrepot_'+table_name, csv_path, table_name)

def download_datas(tables, verbose=False):
    """
        Télécharge toutes les données de l'entrepôt en local
    """
    copy_tables_to_csv(tables, DATA_PATH, verbose=verbose)

def load_datas(tables, verbose=False, path_data=DATA_PATH):
    """ permet de chager les tables dans la variable globale donnees"""
    global donnees
    import_dfs(tables, path_data, verbose=True)


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
        'ref_nuisible_edi', 'ref_correspondance_groupe_cible', 'ref_adventice', 'dose_ref_cible'
    ]
    import_dfs(refs, path, verbose=True)

def create_category_nettoyage():
    """
        Execute les requêtes pour créer le magasin de nettoyage
    """
    prefixe_source = 'nettoyage_'
    tables_nettoyage = []

    # nettoyage_intervention_realise
    suffixe_table = 'intervention'
    name_table = 'intervention_realise'
    df_nettoyage_intervention_realise = nettoyage.nettoyage_intervention(donnees)

    export_to_entrepot(df_nettoyage_intervention_realise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_intervention_realise.to_csv('entrepot_'+name_table+'_nettoyage.csv')

    # nettoyage_utilisation_intrant_realise
    suffixe_table = 'utilisation_intrant'
    name_table = 'utilisation_intrant_realise'
    df_nettoyage_utilisation_intrant_realise = nettoyage.nettoyage_utilisation_intrant(donnees, saisie='realise', verbose=False)

    export_to_entrepot(df_nettoyage_utilisation_intrant_realise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_utilisation_intrant_realise.to_csv(prefixe_source+suffixe_table+'_realise.csv')

    # nettoyage_utilisation_intrant_synthetise
    suffixe_table = 'utilisation_intrant'
    name_table = 'utilisation_intrant_synthetise'
    df_nettoyage_utilisation_intrant_synthetise = nettoyage.nettoyage_utilisation_intrant(donnees, saisie='synthetise', verbose=False)

    export_to_entrepot(df_nettoyage_utilisation_intrant_synthetise, 'entrepot_'+name_table+'_nettoyage')
    #df_nettoyage_utilisation_intrant_synthetise.to_csv(prefixe_source+suffixe_table+'_synthetise.csv')

def create_category_agregation():
    """
        Execute les requêtes pour créer le magasin d'agregation
    """

    # permet d'obtenir des tables agrégées pour avoir les niveaux supérieurs depuis les niveaux fins (raccourcis)
    aggreged_utilisation_intrant_synthetise = agregation.get_aggreged_from_utilisation_intrant_synthetise(
        donnees
    )
    export_to_entrepot(aggreged_utilisation_intrant_synthetise, 'entrepot_utilisation_intrant_synthetise_agrege')

    # permet d'obtenir des tables agrégées pour avoir les niveaux supérieurs depuis les niveaux fins (raccourcis)
    aggreged_utilisation_intrant_realise = agregation.get_aggreged_from_utilisation_intrant_realise(
        donnees
    )
    export_to_entrepot(aggreged_utilisation_intrant_realise, 'entrepot_utilisation_intrant_realise_agrege')


    # toutes les infos manquantes agrégées depuis l'action
    aggreged_leaking_action_realise = agregation.get_leaking_aggreged_from_action_realise(
        aggreged_utilisation_intrant_realise, donnees
    )
    export_to_entrepot(aggreged_leaking_action_realise, 'entrepot_action_realise_manquant_agrege')

    aggreged_leaking_action_synthetise = agregation.get_leaking_aggreged_from_action_synthetise(
        aggreged_utilisation_intrant_synthetise, donnees
    )
    export_to_entrepot(aggreged_leaking_action_synthetise, 'entrepot_action_synthetise_manquant_agrege')


    # toutes les infos manquantes agrégées depuis l'intervention 
    aggreged_leaking_intervention_realise = agregation.get_leaking_aggreged_from_intervention_realise(
        aggreged_utilisation_intrant_realise, donnees
    )
    export_to_entrepot(aggreged_leaking_intervention_realise, 'entrepot_intervention_realise_manquant_agrege')

    aggreged_leaking_intervention_synthetise = agregation.get_leaking_aggreged_from_intervention_synthetise(
        aggreged_utilisation_intrant_synthetise, donnees
    )
    export_to_entrepot(aggreged_leaking_intervention_synthetise, 'entrepot_intervention_synthetise_manquant_agrege')

def create_category_restructuration():
    """
        Execute les requêtes pour créer le magasin de restructuration
    """
    df_noeuds_synthetise_restructured = restructuration.restructuration_noeuds_synthetise(donnees)
    export_to_entrepot(df_noeuds_synthetise_restructured, 'entrepot_noeuds_synthetise_restructure')

    df_connection_synthetise_restructured = restructuration.restructuration_connection_synthetise(donnees)
    export_to_entrepot(df_connection_synthetise_restructured, 'entrepot_connection_synthetise_restructure')

    df_noeuds_realise_restructured = restructuration.restructuration_noeuds_realise(donnees)
    export_to_entrepot(df_noeuds_realise_restructured, 'entrepot_noeuds_realise_restructure')
    
    df_noeuds_realise_restructured = restructuration.restructuration_recolte_rendement_prix(donnees)
    export_to_entrepot(df_noeuds_realise_restructured, 'entrepot_recolte_rendement_prix_restructure')

    df_plantation_perenne_synthetise_restructured = restructuration.restructuration_plantation_perenne_synthetise(donnees)
    export_to_entrepot(df_plantation_perenne_synthetise_restructured, 'entrepot_plantation_perenne_synthetise_restructure')

    # Attention, en suivant parfaitement la convention de nommage, on aboutit à des noms de tables trop longs pour être pris en charge
    # par Postgres en tant que nom de table (taille maximum : 63), on raccourci donc : "composant_culture_concerne" en "ccc"
    df_composant_culture_concerne_intervention_synthetise_restructured = \
        restructuration.restructuration_composant_culture_concerne_intervention_synthetise(donnees)
    export_to_entrepot(
        df_composant_culture_concerne_intervention_synthetise_restructured,
        'entrepot_ccc_intervention_synthetise_restructure'
    )

    df_intervention_synthetise_restructure = restructuration.restructuration_intervention_synthetise(donnees)
    export_to_entrepot(df_intervention_synthetise_restructure, 'entrepot_intervention_synthetise_restructure')

def create_category_indicateur():
    """
        Execute les requêtes pour créer le magasin des indicateurs
    """
    df_utilsation_intrant_indicateur = indicateur.indicateur_utilisation_intrant(donnees)
    export_to_entrepot(df_utilsation_intrant_indicateur, 'entrepot_utilisation_intrant_indicateur')

def create_category_outils_can():
    """
        Execute les requêtes pour créer le magasin des outils utils pour la génération des csv CAN
    """
    # création de l'outil permettant de filtrer les entités (dispositifs)
    df_dispositif_filtres_outils_can = outils_can.dispositif_filtres_outils_can(donnees)
    export_to_entrepot(df_dispositif_filtres_outils_can, 'entrepot_dispositif_filtres_outils_can')

    # création de l'outil permettant de filtrer les entités (domaine)
    df_domaine_filtres_outils_can = outils_can.domaine_filtres_outils_can(donnees)
    export_to_entrepot(df_domaine_filtres_outils_can, 'entrepot_domaine_filtres_outils_can')

    df_parcelle_non_ratachee_outils_can = outils_can.get_parcelles_non_rattachees_outils_can(donnees)
    export_to_entrepot(df_parcelle_non_ratachee_outils_can, 'entrepot_parcelle_non_rattachee_outils_can')

    df_culture_outils_can = outils_can.get_culture_outils_can(donnees)
    export_to_entrepot(df_culture_outils_can, 'entrepot_culture_outils_can')

    df_intervention_realise_outils_can = outils_can.get_intervention_realise_outils_can(donnees)
    export_to_entrepot(df_intervention_realise_outils_can, 'entrepot_intervention_realise_outils_can')

    df_intervention_synthetise_outils_can = outils_can.get_intervention_synthetise_outils_can(donnees)
    export_to_entrepot(df_intervention_synthetise_outils_can, 'entrepot_intervention_synthetise_outils_can')

    df_recolte_outils_can = outils_can.get_recolte_outils_can(donnees)
    export_to_entrepot(df_recolte_outils_can, 'entrepot_recolte_outils_can')

def create_category_test():
    """ 
            Execute les requêtes pour créer le magasin des outils utils pour la génération des csv CAN
    """
    df_recolte_outils_can = outils_can.get_recolte_outils_can(donnees)
    export_to_entrepot(df_recolte_outils_can, 'entrepot_recolte_outils_can')


entrepot_spec = {
    'tables' : [
        'semence', 'plantation_perenne_phases_realise', 'plantation_perenne_phases_synthetise', 'modele_decisionnel', 
        'composant_culture_concerne_intervention_synthetise', 'domaine', 'dispositif', 'modele_decisionnel_maitrise', 
        'modele_decisionnel_strategie', 'modele_decisionnel_strategie_culture', 'plantation_perenne_realise', 
        'intervention_realise_performance', 'intervention_synthetise_performance', 
        'bilan_campagne_regional_pressionbioagresseur', 'bilan_campagne_regional_generalites', 'coordonees_gps_domaine', 
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
        'composant_action_semis', 'reseau', 'liaison_sdc_reseau', 'liaison_reseaux'
    ]
}

external_data_spec = {
    'tables' : [
    ]
}

# déclaration des dépendances entre les différentes catégories
magasin_specs = {
    'nettoyage' : {
        'explication' : "Les données de la source nettoyage permettent d'obtenir des informations utiles pour le nettoyage et la manipulation des différentes entités.",
        'categories' : {
            'nettoyage' : {
                'function' : create_category_nettoyage,
                'dependances' : [], 
                'generated' : [
                    'intervention_realise_nettoyage', 
                    'utilisation_intrant_realise_nettoyage',
                    'utilisation_intrant_synthetise_nettoyage'
                ]
            },
            'agregation' : {
                'function' : create_category_agregation,
                'dependances' : [],
                'generated' : [
                    'utilisation_intrant_realise_agrege',
                    'utilisation_intrant_synthetise_agrege', 
                    'intervention_synthetise_manquant_agrege', 
                    'intervention_realise_manquant_agrege',
                    'action_realise_manquant_agrege', 
                    'action_synthetise_manquant_agrege',
                ]
            },
            'agregation_complet' : {
                'function' : None,
                'dependances' : [{
                    'magasin' : 'nettoyage', 
                    'categorie': 'agregation'
                }
                ],
                'generated' : [
                    'utilisation_intrant_realise_agrege', 
                    'utilisation_intrant_synthetise_agrege',
                    'intervention_synthetise_agrege', 
                    'intervention_realise_agrege',
                    'action_realise_agrege', 
                    'action_synthetise_agrege'
                ]
            },
            'restructuration' : {
                'function' : create_category_restructuration,
                'dependances' : [{
                    'magasin' : 'nettoyage', 
                    'categorie': 'agregation_complet'
                }],
                'generated' : [
                    'noeuds_synthetise_restructure', 
                    'noeuds_realise_restructure',
                    'connection_synthetise_restructure',
                    'recolte_rendement_prix_restructure',
                    'plantation_perenne_synthetise_restructure',
                    'ccc_intervention_synthetise_restructure', 
                    'intervention_synthetise_restructure'
                ]
            },
            'indicateur' : {
                'function' : create_category_indicateur,
                'dependances' : [],
                'generated' : [
                    'utilisation_intrant_indicateur', 
                ]
            },
            'outils_can' : {
                'function' : create_category_outils_can,
                'dependances' : [{
                    'magasin' : 'nettoyage', 
                    'categorie': 'restructuration'
                },
                {
                    'magasin' : 'nettoyage', 
                    'categorie': 'agregation_complet'
                }],
                'generated' : [
                    'dispositif_filtres_CAN'
                    'intervention_realise_outils_can', 
                    'intervention_synthetise_outils_can',
                    'parcelle_non_rattachee_outils_can',
                    'recolte_outils_can'
                ]
            },
            'test' : {
                'function' : create_category_test,
                'dependances' : [{
                    'magasin' : 'nettoyage', 
                    'categorie': 'restructuration'
                },
                {
                    'magasin' : 'nettoyage', 
                    'categorie': 'agregation_complet'
                }],
                'generated' : [
                    'recolte_outils_can'
                ]
            },
        }
    }
}




# à terme, cet ordre devra être généré automatiquement à partir des dépendances --> mais pour l'instant plus simple comme ça
steps = [
    {'magasin' : 'nettoyage', 'categorie' : 'nettoyage'},
    {'magasin' : 'nettoyage', 'categorie' : 'agregation'},
    {'magasin' : 'nettoyage', 'categorie' : 'agregation_complet'},
    {'magasin' : 'nettoyage', 'categorie' : 'restructuration'},
    {'magasin' : 'nettoyage', 'categorie' : 'indicateur'},
    {'magasin' : 'nettoyage', 'categorie' : 'outils_can'}
]

options_categories = {}

for magasin_key, magasin in magasin_specs.items():
    for categorie_key in magasin['categories']:
        options_categories[categorie_key +' ('+ magasin_key+')'] = {'magasin' : magasin_key, 'categorie' : categorie_key}
        categorie = magasin['categories'][categorie_key]
        dependances = categorie['dependances']

history = []


options = {
        "Tout générer" : [],
        "Générer une catégorie" : [],  
        "Télécharger une catégorie" : [],  
        "Téléchargement de l'entrepôt" : [],
        "Quitter" : []
}

donnees = {}
while True:
    print("")
    print("")
    print("**** Bienvenue dans notre interface de génération du magasin de données : ****")
    print("")
    print("Veuillez choisir une option parmi les suivantes :")
    print("")
    for i, option in enumerate(options.keys()):
        print(f"{i + 1}. {option}")
    
    choice = int(input("Entrez votre choix (1, 2 ...) : "))
    choice_key = list(options.keys())[choice - 1]
    
    if choice_key == "Quitter":
        print("Au revoir !")
        break
    elif choice_key == 'Tout générer':
        print("* DÉBUT DU TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        download_datas(entrepot_spec['tables'], verbose=False)
        print("* FIN DU TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        print("* DÉBUT DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        load_datas(entrepot_spec['tables'], verbose=False)
        print("* FIN DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        print("* DÉBUT DU CHARGEMENT DES DONNÉES EXTERNES *")
        load_datas(external_data_spec['tables'], verbose=False, path_data=EXTERNAL_DATA_PATH)
        print("* FIN DU CHARGEMENT DES DONNÉES EXTERNES*")
        print("* DÉBUT DU CHARGEMENT DES RÉFÉRENTIELS *")
        print("Attention, penser à les mettre à jour manuellement.")
        load_ref()
        print("* FIN DU CHARGEMENT DES RÉFÉRENTIELS*")

        for step in steps :
            current_magasin = step['magasin']
            current_category = step['categorie']
            print("* DÉBUT GÉNÉRATION ", current_magasin, current_category," *")
            choosen_function = magasin_specs[current_magasin]['categories'][current_category]['function']

            if(current_category == 'agregation_complet'):
                # Lors de la génération de agregation_complet, il faut aussi créer les dataframes.
                generate_data_agreged(verbose=False)
                download_data_agreged(verbose=False)
            else :
                choosen_function()
                download_datas(magasin_specs[current_magasin]['categories'][current_category]['generated'])
                load_datas(magasin_specs[current_magasin]['categories'][current_category]['generated'])
            print("* FIN GÉNÉRATION ", current_magasin, current_category," *")
    elif choice_key == 'Téléchargement de l\'entrepôt':
        print("* DÉBUT DU TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
        download_datas(entrepot_spec['tables'], verbose=False)
        print("* FIN DU TÉLÉCHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
    elif choice_key == 'Télécharger une catégorie':
        print("")
        print("Veuillez choisir la catégorie à télécharger")
        print("")
        for i, option_category in enumerate(options_categories.keys()):
                    print(f"{i + 1}. {option_category}")
        choice = int(input("Entrez votre choix (1, 2 ...) : "))
        choosen_value = list(options_categories.values())[choice - 1]
        choosen_magasin = choosen_value['magasin']
        choosen_category = choosen_value['categorie']
        choosen_function = magasin_specs[choosen_magasin]['categories'][choosen_category]['function']
        choosen_generated = magasin_specs[choosen_magasin]['categories'][choosen_category]['generated']

        if(choosen_category == 'agregation_complet'):
            # Attention, dans ce cas les données à télécharger ne sont pas celles stockées, il faut préalablement les reconstituer
            # Chargement de toutes les données incomplètes
            print("* DÉBUT DU CHARGEMENT DES DONNÉES AGREGATION PARTIELLES *")             
            choosen_dependances = magasin_specs[choosen_magasin]['categories'][choosen_category]['dependances']
            for choosen_dependance in choosen_dependances:
                categorie_dependance = magasin_specs[choosen_dependance['magasin']]['categories'][choosen_dependance['categorie']]
                if(len(categorie_dependance['generated']) != 0):
                    if(categorie_dependance['generated'][0] not in donnees):
                        print("* DÉBUT DU CHARGEMENT DES DONNÉES DES MAGASINS NÉCESSAIRES *")
                        load_datas(categorie_dependance['generated'], verbose=False)
                        print("* FIN DU CHARGEMENT DES DONNÉES DES MAGASINS NÉCESSAIRES *")
                            
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
        choosen_magasin = choosen_value['magasin']
        choosen_category = choosen_value['categorie']
        choosen_function = magasin_specs[choosen_magasin]['categories'][choosen_category]['function']
        choosen_dependances = magasin_specs[choosen_magasin]['categories'][choosen_category]['dependances']
        for choosen_dependance in choosen_dependances:
            categorie_dependance = magasin_specs[choosen_dependance['magasin']]['categories'][choosen_dependance['categorie']]
            if(len(categorie_dependance['generated']) != 0):
                if(categorie_dependance['generated'][0] not in donnees):
                    print("* DÉBUT DU CHARGEMENT DES DONNÉES DES MAGASINS NÉCESSAIRES *")
                    load_datas(categorie_dependance['generated'], verbose=False)
                    print("* FIN DU CHARGEMENT DES DONNÉES DES MAGASINS NÉCESSAIRES *")
                

        print("Import des données de l'entrepôt au besoin")

        
        if(choosen_category == 'agregation_complet'):
            # Si on a choisi de générer agregation_complet, il faut aussi load les données agrégées complètes
            generate_data_agreged(verbose=False)
            download_data_agreged(verbose=False)
        else :
            # on vérifie que les données n'ont pas été déjà chargées
            if('domaine' not in donnees):
                print("* DÉBUT DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                load_datas(entrepot_spec['tables'], verbose=False)
                load_ref()
                print("* FIN DU CHARGEMENT DES DONNÉES DE L'ENTREPÔT *")
                print("* DÉBUT DU CHARGEMENT DES DONNÉES EXTERNES *")
                load_datas(external_data_spec['tables'], verbose=False, path_data=EXTERNAL_DATA_PATH)
                print("* FIN DU CHARGEMENT DES DONNÉES EXTERNES*")
                
            print("* DÉBUT GÉNÉRATION ", choosen_magasin, choosen_category," *")
            choosen_function()
            print("* FIN GÉNÉRATION ", choosen_magasin, choosen_category," *")


    elif choice_key == "Test":
        print("* DÉBUT DE LA GÉNÉRATION TEST *")
        create_category_restructuration()
        print("* FIN DE LA GÉNÉRATION TEST *")





