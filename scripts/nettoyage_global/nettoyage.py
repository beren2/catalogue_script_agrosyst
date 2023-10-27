"""
	Regroupe les fonctions de nettoyage aux différentes échelles.
"""
import pandas as pd
import numpy as np
import scripts.nettoyage_global.fonctions_tests as ft



def nettoyage_utilisation_intrant(donnees, params=None, verbose=False):
    """
        Retourne une série de vecteurs binaire.
        La ligne i de cette série contient le vecteur test associé à la ligne i

                Paramètres:
                    donnees (df) : dataframe contenant les données d'intrants
                    params (dict): dictionnaire contenant les métadonnées que l'utilisateur 
                        souhaite modifié.
                    verbose (booleen) : booléen indiquant le niveau de détail (True = details 
                        maximum)
            
                Retourne:
                    res (Serie) : série binaire de taille n x m indiquant si les tests sont passés
    """
    # lecture des fichiers de métadonnées
    df_metadonnees_seuils = pd.read_csv('data/metadonnees_seuils.csv', index_col='id')
    df_metadonnees_tests = pd.read_csv('data/metadonnees_tests.csv', index_col='id')

    # selection des données pertinentes et conversion en dictionnaires
    metadata_seuils = df_metadonnees_seuils
    metadata_seuils = metadata_seuils.loc[metadata_seuils['script'] == 'nettoyage_intrant']
    metadata_seuils = metadata_seuils.T.to_dict()

    metadata_tests = df_metadonnees_tests
    metadata_tests = metadata_tests.loc[metadata_tests['script'] == 'nettoyage_intrant']
    metadata_tests = metadata_tests.T.to_dict()

    # modification des paramètres par l'utilisateur
    if params is not None:
        # l'utilisateur souhaite modifier les paramètres par défaut
        for key_params in params.keys():
            if key_params in metadata_seuils.keys():
                # on remplace la valeur du paramètre par celles de l'utilisateurs
                metadata_seuils[key_params] = params[key_params]

    # initialisation de la variable contenant les flags pour l'ensembles des tests
    codes_tests = []
    # application des tests pour obtention du "code_test"
    for test_index, test_key in enumerate(metadata_tests.keys()):
        test = metadata_tests[test_key]
        if verbose :
            print("Application du test :", test_index, test_key)

        # obtention de la fonction associée au test
        fonction_test = getattr(ft, test['fichier'])

        # application de la fonction
        code_test = np.array(fonction_test(donnees, metadata_seuils))

        # stockage des résultats
        codes_tests.append(code_test)

    df = pd.DataFrame(np.transpose(codes_tests)).astype('str')
    res = df.apply(lambda x : ''+''.join(x), axis=1)

    return res


def nettoyage_intervention(donnees, params=None, verbose=False):
    """
        Retourne une série de vecteurs binaire.
        La ligne i de cette série contient le vecteur test associé à la ligne i

                Paramètres:
                    donnees (df) : dataframe contenant les données d'interventions
                    params (dict): dictionnaire contenant les métadonnées que l'utilisateur 
                        souhaite modifié.
                    verbose (booleen) : booléen indiquant le niveau de détail (True = details 
                        maximum)
            
                Retourne:
                    res (Serie) : série binaire de taille n x m indiquant si les tests sont passés
    """
    # lecture des fichiers de métadonnées
    df_metadonnees_seuils = pd.read_csv('data/metadonnees_seuils.csv', index_col='id')
    df_metadonnees_tests = pd.read_csv('data/metadonnees_tests.csv', index_col='id')

    # selection des données pertinentes et conversion en dictionnaires
    metadata_seuils = df_metadonnees_seuils
    metadata_seuils = metadata_seuils.loc[metadata_seuils['script'] == 'nettoyage_intervention']
    metadata_seuils = metadata_seuils.T.to_dict()

    metadata_tests = df_metadonnees_tests
    metadata_tests = metadata_tests.loc[metadata_tests['script'] == 'nettoyage_intervention']
    metadata_tests = metadata_tests.T.to_dict()

    # modification des paramètres par l'utilisateur
    if params is not None:
        # l'utilisateur souhaite modifier les paramètres par défaut
        for key_params in params.keys():
            if key_params in metadata_seuils.keys():
                # on remplace la valeur du paramètre par celles de l'utilisateurs
                metadata_seuils[key_params] = params[key_params]

    # initialisation de la variable contenant les flags pour l'ensembles des tests
    codes_tests = []
    # application des tests pour obtention du "code_test"
    for test_index, test_key in enumerate(metadata_tests.keys()):
        test = metadata_tests[test_key]
        if verbose :
            print("Application du test :", test_index, test_key)

        # obtention de la fonction associée au test
        fonction_test = getattr(ft, test['fichier'])

        # application de la fonction
        code_test = np.array(fonction_test(donnees, metadata_seuils))

        # stockage des résultats
        codes_tests.append(code_test)

    df = pd.DataFrame(np.transpose(codes_tests)).astype('str')
    res = df.apply(lambda x : ''+''.join(x), axis=1)

    return res
            
