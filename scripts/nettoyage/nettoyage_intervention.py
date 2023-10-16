"""
La fonction filtration_intervention permet d'obtenir les interventions 
cohérentes selon plusieurs critères : 
Pour le réalisé : 
    - date de fin > date de début
    - nombre de passages < nombre_max_passages
Pour le synthétisé : 
    - 
"""
import pandas as pd
import fonctions_tests as ft        # pylint: disable=import-error
import numpy as np

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
                    code_test (Serie) : série binaire de taille n indiquant si le test est passé
    """
    # lecture des fichiers de métadonnées
    df_metadonnees_seuils = pd.read_csv('../data/metadonnees_seuils.csv', index_col='id')
    df_metadonnees_tests = pd.read_csv('../data/metadonnees_tests.csv', index_col='id')

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
        codes_tests.append(code_test)

    #df_intervention_realise = donnees['intervention_realise']
    #df_intervention_synthetise = donnees['intervention_synthetise']

    # DURÉES D'INTERVENTION
    # obtention de la durée de l'intervention
    #date_debut = df_intervention_realise['date_debut']
    #date_fin = df_intervention_realise['date_fin']
    #date_debut = pd.to_datetime(date_debut, format="%Y-%m-%d", errors='coerce')
    #date_fin = pd.to_datetime(date_fin, format="%Y-%m-%d", errors='coerce')
    #duree_intervention = date_fin - date_debut

    # filtration des interventions qui durent au moins 0 jours
    #df_intervention_realise = df_intervention_realise.loc[
    #    duree_intervention.dt.days >= 0
    #]

    # filtrer les interventions qui ont un débit de chantier trop important

    #filtered_data = {
    #    'intervention_realise' : df_intervention_realise
    #}

    return codes_tests
            