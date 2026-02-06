"""
	Regroupe les fonctions de nettoyage aux différentes échelles.
"""
import pandas as pd
import numpy as np
import scripts.utils.fonction_nettoyage as ft


def nettoyage_utilisation_intrant(donnees, saisie='realise', params=None, verbose=False, path_metadata = '02_outils/data/'):
    """
        Retourne une série de vecteurs binaire.
        La ligne i de cette série contient le vecteur test associé à la ligne i

                Paramètres:
                    donnees (dict) : dictionnaire contenant les données utiles : 
                        clés avec les dataframes correspondants : 
                            'composant_culture', 'connection_synthetise', 'culture', 'intervention_realise', 
                            'intervention_synthetise', 'intrant', 'noeuds_realise', 'noeuds_synhtetise', 
                            'plantation_perenne_phases_realise', 'plantation_perenne_phases_synthetise', 
                            'plantation_perenne_realise', 'plantation_perenne_synthetise', 'utilisation_intrant_cible',
                            'utilisation_intrant_realise', 'utilisation_intrant_synthetise'
                    params (dict): dictionnaire contenant les métadonnées que l'utilisateur 
                        souhaite modifié. (cf data/metadonnees_seuils.csv avec le script "nettoyage_utilisation_intrant")
                    verbose (booleen) : booléen indiquant le niveau de détail (True = details 
                        maximum)
            
                Retourne:
                    res (Serie) : série binaire de taille n x m indiquant si les tests sont passés
    """
    # lecture des fichiers de métadonnées
    df_metadonnees_seuils = pd.read_csv(path_metadata+'metadonnees_seuils.csv', index_col='id')
    df_metadonnees_tests = pd.read_csv(path_metadata+'metadonnees_tests.csv', index_col='id')

    # selection des données pertinentes et conversion en dictionnaires
    metadata_seuils = df_metadonnees_seuils
    metadata_seuils = metadata_seuils.loc[metadata_seuils['script'] == 'nettoyage_utilisation_intrant']
    metadata_seuils = metadata_seuils.T.to_dict()

    metadata_tests = df_metadonnees_tests
    metadata_tests = metadata_tests.loc[metadata_tests['script'] == 'nettoyage_utilisation_intrant']
    metadata_tests = metadata_tests.T.to_dict()

    # modification des paramètres par l'utilisateur
    if params is not None:
        # l'utilisateur souhaite modifier les paramètres par défaut
        for key_params in params.keys():
            if key_params in metadata_seuils.keys():
                # on remplace la valeur du paramètre par celles de l'utilisateurs
                metadata_seuils[key_params]['seuil'] = params[key_params]

    # initialisation de la variable contenant les flags pour l'ensembles des tests
    codes_tests = {}
    # application des tests pour obtention du "code_test"
    for test_index, test_key in enumerate(metadata_tests.keys()):
        test = metadata_tests[test_key]
        
        if verbose :
            print("Application du test :", test_index, test_key)

        # obtention de la fonction associée au test
        fonction_test = getattr(ft, test['fichier'])
        
        # application de la fonction
        codes_tests[test_key]= np.array(fonction_test(donnees, metadata_seuils, saisie))
    
    df = pd.DataFrame.from_dict(codes_tests)
    ids = donnees['utilisation_intrant_'+saisie].reset_index()['id']
    res_2 = pd.concat([ids, df], axis=1).set_index('id')

    return res_2


def nettoyage_intervention(donnees, params=None, verbose=False, path_metadata='02_outils/data/'):
    """
        Retourne une série de vecteurs binaire.
        La ligne i de cette série contient le vecteur test associé à la ligne i

                Paramètres:
                    donnees (dict) : dictionnaire contenant les données utiles :
                        intervention_realise : df des intervention en réalisé
                    params (dict): dictionnaire contenant les métadonnées que l'utilisateur 
                        souhaite modifié.
                    verbose (booleen) : booléen indiquant le niveau de détail (True = details 
                        maximum)
                Retourne:
                    res (Serie) : série binaire de taille n x m indiquant si les tests sont passés
    """
    # lecture des fichiers de métadonnées
    df_metadonnees_seuils = pd.read_csv(path_metadata+'metadonnees_seuils.csv', index_col='id')
    df_metadonnees_tests = pd.read_csv(path_metadata+'metadonnees_tests.csv', index_col='id')

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
                metadata_seuils[key_params]['seuil'] = params[key_params]

    # initialisation de la variable contenant les flags pour l'ensembles des tests
    codes_tests = {}
    # application des tests pour obtention du "code_test"
    for test_index, test_key in enumerate(metadata_tests.keys()):
        test = metadata_tests[test_key]
        if verbose :
            print("Application du test :", test_index, test_key)

        # obtention de la fonction associée au test
        fonction_test = getattr(ft, test['fichier'])

        # application de la fonction
        codes_tests[test_key]= np.array(fonction_test(donnees, metadata_seuils))

    df = pd.DataFrame.from_dict(codes_tests)
    ids = donnees['intervention_realise'].reset_index()['id']
    res_2 = pd.concat([ids, df], axis=1).set_index('id')
    
    return res_2


def entite_unique_par_sdc(donnees):
    """
        Outil permettant de renvoyer l'entité retenue pour un sdc_id.
        
        Parfois un sdc_id peut avoir un ou plusieurs synthétisés et/ou un réalisé (constitué d'un ensemble de parcelles attachées). On veut une seul entité par sdc_id
                
        Coté synthétisé, on part des performances de synthétisé plutôt que de la table brut des synthétisés. En effet il y a des synthétisé sans performances car sans cultures (174 pour l'export du 20260130). Il serait idiot de les prendre dans un sdc plutot que les réalisé avec des perfromances.
        Pour les réalisé, par construction, nous ne prenons pas les parcelles non rattachés à un sdc

        On utilise le principe de priorité pour ne gardé ensuite que le sdc_id si seul le réalisé est retenue, ou le synthtisé_id retenue. On utilise nottament le fait qu'un synthétisé est toujours prioritaire face à un réalisé. Puis, pour les multiples synthétisés, on regarde le taux de complétion, le fait que les campagnes soient tri-annuels ou non, la validation du synthétisé, et la dernière date de mise à jour du synthétisé.

        Ensuite on retourne un dataframe avec le sdc_id et l'entité retenue (tag réalisé ou synthétisé_id)
    """
    # lsite des colonne dont on a besoin dans les performances pour calculer un taux de complétude
    list_tx_comp = ['ift_cible_non_mil_tx_comp','co_tot_std_mil_tx_comp','co_decomposees_std_mil_tx_comp','cm_std_mil_tx_comp','pb_std_mil_tx_comp']

    synthetise = donnees['synthetise'][['id','valide','derniere_maj','sdc_id','campagnes']].copy()
    perf_synth = donnees['synthetise_synthetise_performance'][['synthetise_id']+list_tx_comp].copy()
    parcelle = donnees['parcelle'][['id','sdc_id']].copy() # attention ne prends pas en compte les parcelles non rattachées
    
    # merge synthétisé aux perfromances des synthétisés
    # attention on a des synthétisés sans performances (174 au 30 janvier 2026)
    # il ne faut pas que ces synthétisés sans performances soient prioritaires par rapport à un réalisé saisi !
    perf_synth = perf_synth.copy()
    perf_synth.loc[:, 'tx_compl'] = perf_synth[list_tx_comp].sum(axis=1)
    perf_synth.drop(columns=list_tx_comp, inplace=True)

    perf_synth = perf_synth.merge(synthetise.rename(columns={'id':'synthetise_id'}), on='synthetise_id', how='left')
    perf_synth['calcul'] = 'synth'

    # Pour le réalisé on prend juste les sdc_id qui provient de la table parcelle
    real = pd.DataFrame(data = {"sdc_id" : parcelle['sdc_id'].unique(), "calcul" : 'real'})

    # Union des entités en réalisé et en synthétisé
    df = pd.concat([perf_synth, real])
    
    # Mise en place des variables qui permettrons de choisir une entité plutot qu'une autre
    df['calcul'] = df['calcul'].apply(lambda x: 0 if x == 'synth' else 1)
    df['tx_compl'] = df['tx_compl'].fillna(-float('inf'))
    df['campagnes'] = df['campagnes'].astype(str).fillna('0000').apply(lambda x: 0 if len(x) == 16 else 1)
    df['valide'] = df['valide'].fillna('f').apply(lambda x: 0 if x == 't' else 1)
    df['derniere_maj'] = df['derniere_maj'].fillna('0001-01-01 00:00:00.000')

    # On priorise les valeurs selon plusieurs méthodes
    df.sort_values(
        by=[
            'calcul',       # On priorise les synthétisé
            'tx_compl',     # On priorise la somme des taux de complétion les plus hautes
            'campagnes',    # On priorise les triannuels
            'valide',       # On priorise les entités validées
            'derniere_maj'  # On fini par prioriser les entités dont la denrière maj est la plus récente
        ],
        ascending=[True, False, True, True, False],
        inplace=True
    )

    # On groupe par sdc_id et on tague l'entité prioritaire
    df['est_prioritaire'] = df.groupby('sdc_id').cumcount() == 0

    ############ Priorisation selon la CAN ############
    # # On priorise les valeurs selon la méthode de la CAN
    # df.sort_values(
    #     by=[
    #         'calcul',       # On priorise les synthétisé
    #         'derniere_maj'  # On fini par prioriser les entités dont la denrière maj est la plus récente
    #     ],
    #     ascending=[True, False],
    #     inplace=True
    # )

    # df['est_prioritaire_CAN'] = df.groupby('sdc_id').cumcount() == 0
    ############ 73 lignes sur ~34500 diffèrent avec la méthode précédente au 30-01-2026 ############

    df = df.loc[df['est_prioritaire'], ['sdc_id','synthetise_id']]
    df['synthetise_id'] = np.where(df['synthetise_id'].isnull(), "realise_retenu", df['synthetise_id'])
    df.rename(columns={'synthetise_id':'entite_retenue'}, inplace=True)

    return df.set_index('sdc_id')