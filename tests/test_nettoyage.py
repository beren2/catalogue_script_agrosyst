import pandas as pd
#from nettoyage import nettoyage
from scripts.nettoyage_global import nettoyage
from scripts.utils import fonctions_utiles

def test_debit_chantier_intervention_realise():
    """
        Test du débit de chantier des interventions en réalisé
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_debit_chantier_intervention_realise']

    # définition des lignes qui posent problème pour les débits de chantier en réalisé
    intervention_id_debit_chantier_problem_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '0']['id_ligne'])

    # définition des lignes qui ne posent pas problème pour les débits de chantier en réalisé et qui doivent par conséquent, passer le test
    intervention_id_debit_chantier_ok_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '1']['id_ligne'])

    # obtention des données
    path_data = 'tests/data/test_debit_chantier_intervention_realise/'
    path_intervention_realise = path_data+'intervention_realise.csv'
    df_intervention_realise = pd.read_csv(path_intervention_realise, sep = ',')

    # filtration pour les données problématiques
    index_problem_realise = df_intervention_realise['id'].isin(intervention_id_debit_chantier_problem_realise)
    # application de la fonction d'erreur aux lignes problématiques (elles doivent être signalées (0))
    code_test_problem = nettoyage.nettoyage_intervention(df_intervention_realise.loc[index_problem_realise])
    
    # filtration pour les données non-problématiques
    index_ok_realise = df_intervention_realise['id'].isin(intervention_id_debit_chantier_ok_realise)
    # application de la fonction d'erreur aux lignes non problématiques (elles doivent passées (1))
    code_test_ok = nettoyage.nettoyage_intervention(df_intervention_realise.loc[index_ok_realise])

    # toutes les lignes de problèmes doivent valoir 0
    res_problem = (code_test_problem.apply(lambda x : x[0]) == '0').all()
    # toutes les lignes sans problèmes doivent valoir 1 
    res_ok = (code_test_ok.apply(lambda x : x[0]) == '1').all()

    assert res_problem
    assert res_ok
    
def test_utilisation_intrant_dose_realise():
    """
        Test de la détection de dose trop hautes utilisées en réalisé
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_utilisation_intrant_dose_realise']

    # définition des lignes qui posent problème pour les débits de chantier en réalisé
    id_utilisation_intrant_dose_problem_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '0']['id_ligne'])

    # définition des lignes qui ne posent pas problème pour les débits de chantier en réalisé et qui doivent par conséquent, passer le test
    id_utilisation_intrant_dose_ok_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '1']['id_ligne'])

    # obtention des données
    path_data = 'tests/data/test_utilisation_intrant_dose/'
    path_utilisation_intrant_realise = path_data+'utilisation_intrant_realise.csv'
    df_utilisation_intrant_realise = pd.read_csv(path_utilisation_intrant_realise, sep =',')

    # filtration pour les données problématiques
    index_problem_realise = df_utilisation_intrant_realise['id'].isin(id_utilisation_intrant_dose_problem_realise)
    # application de la fonction d'erreur aux lignes problématiques (elles doivent être signalées (0))
    code_test_problem = nettoyage.nettoyage_utilisation_intrant(df_utilisation_intrant_realise.loc[index_problem_realise], saisie='realise', verbose=True, path_data=path_data)
    
    # filtration pour les données non-problématiques
    index_ok_realise = df_utilisation_intrant_realise['id'].isin(id_utilisation_intrant_dose_ok_realise)
    # application de la fonction d'erreur aux lignes non problématiques (elles doivent passées (1))
    code_test_ok = nettoyage.nettoyage_utilisation_intrant(df_utilisation_intrant_realise.loc[index_ok_realise], saisie='realise', verbose=True, path_data=path_data)
    
    # toutes les lignes de problèmes doivent valoir 0
    res_problem = (code_test_problem.apply(lambda x : x[0]) == '0').all()[0]
    # toutes les lignes sans problèmes doivent valoir 1 
    res_ok = (code_test_ok.apply(lambda x : x[0]) == '1').all()[0]

    assert res_problem
    assert res_ok

def test_utilisation_intrant_dose_synthetise():
    """
        Test de la détection de dose trop hautes utilisées en synthétisé
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_utilisation_intrant_dose_synthetise']

    # définition des lignes qui posent problème pour les débits de chantier en réalisé
    id_utilisation_intrant_dose_problem_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '0']['id_ligne'])

    # définition des lignes qui ne posent pas problème pour les débits de chantier en réalisé et qui doivent par conséquent, passer le test
    id_utilisation_intrant_dose_ok_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '1']['id_ligne'])

    # obtention des données
    path_data = 'tests/data/test_utilisation_intrant_dose/'
    path_utilisation_intrant_realise = path_data+'utilisation_intrant_synthetise.csv'
    df_utilisation_intrant_realise = pd.read_csv(path_utilisation_intrant_realise, sep =',')

    # filtration pour les données problématiques
    index_problem_realise = df_utilisation_intrant_realise['id'].isin(id_utilisation_intrant_dose_problem_realise)
    # application de la fonction d'erreur aux lignes problématiques (elles doivent être signalées (0))
    code_test_problem = nettoyage.nettoyage_utilisation_intrant(df_utilisation_intrant_realise.loc[index_problem_realise], saisie='synthetise', path_data=path_data)
    
    # filtration pour les données non-problématiques
    index_ok_realise = df_utilisation_intrant_realise['id'].isin(id_utilisation_intrant_dose_ok_realise)
    # application de la fonction d'erreur aux lignes non problématiques (elles doivent passées (1))
    code_test_ok = nettoyage.nettoyage_utilisation_intrant(df_utilisation_intrant_realise.loc[index_ok_realise], saisie='synthetise', path_data=path_data)
    
    # toutes les lignes de problèmes doivent valoir 0
    res_problem = (code_test_problem.apply(lambda x : x[0]) == '0').all()[0]
    # toutes les lignes sans problèmes doivent valoir 1 
    res_ok = (code_test_ok.apply(lambda x : x[0]) == '1').all()[0]

    assert res_problem
    assert res_ok



def test_get_infos_traitement():
    """
        Test de l'obtention du code amm.
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_get_infos_traitement']

    # obtention des données
    path_data = 'tests/data/test_get_infos_traitement/'
    path_utilisation_intrant_realise = path_data+'utilisation_intrant_realise.csv'
    path_intrant = path_data+'intrant.csv'
    df_utilisation_intrant_realise = pd.read_csv(path_utilisation_intrant_realise, sep = ',')
    df_intrant = pd.read_csv(path_intrant, sep = ',')

    # application de la méthode à tester
    utilisation_intrant_id_code_amm_expected = df_metadonnees[['id_ligne', 'valeur_attendue', 'colonne_testee']]
    test_get_infos_traitement_realise = fonctions_utiles.get_infos_traitement(df_utilisation_intrant_realise[['id', 'intrant_id']], df_intrant)

    # on merge les dataframe obtenus et attendus
    left = utilisation_intrant_id_code_amm_expected.rename(columns={
        'id_ligne' : 'id'
    })
    right = test_get_infos_traitement_realise
    merge = pd.merge(left, right, on = 'id') 

    # la valeur attendue doit toujours être égale à la valeur trouvée
    res_ok = (merge['valeur_attendue'].astype('int') == merge['code_amm'].astype('int')).all()

    assert res_ok

def test_get_dose_ref():
    """
        Test de l'obtention de la dose de référence
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_get_dose_ref']

    # obtention des données
    path_data = 'tests/data/test_get_dose_ref/'
    path_utilisation_intrant_realise = path_data+'utilisation_intrant_realise.csv'
    path_utilisation_intrant_synthetise = path_data+'utilisation_intrant_synthetise.csv'

    df_utilisation_intrant_realise = pd.read_csv(path_utilisation_intrant_realise, sep = ',') 
    df_utilisation_intrant_synthetise = pd.read_csv(path_utilisation_intrant_synthetise, sep = ',')

    # obtention de la dose de référence à partir de la fonction get_infos_all_utilisation_intrant
    df_utilisation_intrant_realise = fonctions_utiles.get_infos_all_utilisation_intrant(df_utilisation_intrant_realise, saisie = 'realise', path_data=path_data)
    df_utilisation_intrant_synthetise = fonctions_utiles.get_infos_all_utilisation_intrant(df_utilisation_intrant_synthetise, saisie = 'synthetise', path_data=path_data)
    
    test_get_dose_ref_ = pd.concat([df_utilisation_intrant_realise, df_utilisation_intrant_synthetise], axis=0)

    # obtention de la dose de référence attendue
    dose_ref_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'dose_ref_maa'][['id_ligne', 'valeur_attendue']]
    dose_ref_unit_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'dose_ref_maa_unit'][['id_ligne', 'valeur_attendue']]

    left = dose_ref_expected.rename(columns={
        'id_ligne' : 'id',
        'valeur_attendue' : 'dose_ref_expected'
    })
    right = test_get_dose_ref_
    merge = pd.merge(left, right, on = 'id', how='left')

    left = merge 
    right = dose_ref_unit_expected.rename(columns={
        'id_ligne' : 'id',
        'valeur_attendue' : 'dose_ref_unit_expected'
    })
    merge = pd.merge(left, right, on = 'id', how='left')[
        ['id', 'dose_ref_expected', 'dose_ref_unit_expected', 'dose_ref_maa', 'unit_dose_ref_maa']
    ]

    # la valeur attendue doit toujours être égale à la valeur trouvée
    res_valeur_ok = (merge['dose_ref_expected'].astype('float') == merge['dose_ref_maa'].astype('float')).all()
    res_unit_ok = (merge['dose_ref_unit_expected'] == merge['unit_dose_ref_maa']).all()


    assert res_valeur_ok
    assert res_unit_ok

