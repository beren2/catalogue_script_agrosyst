import pandas as pd
#from nettoyage import nettoyage
from scripts.nettoyage_global import nettoyage

def test_debit_chantier_intervention_realise():
    """
        Test du débit de chantier des interventions en réalisé
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_debit_chantier_intervention_realise']

    # définition des lignes qui posent problème pour les débits de chantier en réalisé
    intervention_id_debit_chantier_problem_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == 0]['id_ligne'])

    # définition des lignes qui ne posent pas problème pour les débits de chantier en réalisé et qui doivent par conséquent, passer le test
    intervention_id_debit_chantier_ok_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == 1]['id_ligne'])

    # obtention des données
    path_intervention_realise = 'tests/data/intervention_realise.csv'
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

    return 0
