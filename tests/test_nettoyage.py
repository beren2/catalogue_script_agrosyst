"""
    Regroupe tous les tests utilisés pour vérifier que le magasin de données "nettoyage" est bien fonctionnel.
"""

import pandas as pd
#from nettoyage import nettoyage
from scripts.nettoyage_global import nettoyage
from scripts.utils import fonctions_utiles



def import_df(df_name, path_data, sep, df):
    """
        importe un dataframe au chemin path_data+df_name+'.csv' et le stock dans le dictionnaire 'df' à la clé df_name
    """
    df[df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep)

def import_dfs(df_names, path_data,  df, sep = ','):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans la liste df_names
    """
    for df_name in df_names : 
        import_df(df_name, path_data, sep, df)

    return df

        

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
    df_names = ['intervention_realise']
    path_data = 'tests/data/test_debit_chantier_intervention_realise/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')
    print(donnees.keys())
    df_intervention_realise = donnees['intervention_realise']

    # filtration pour les données problématiques
    index_problem_realise = df_intervention_realise['id'].isin(intervention_id_debit_chantier_problem_realise)
    # données qui posent problème
    donnees_problem = donnees.copy()
    donnees_problem['intervention_realise'] = donnees_problem['intervention_realise'].loc[index_problem_realise]
    # application de la fonction d'erreur aux lignes problématiques (elles doivent être signalées (0))
    code_test_problem = nettoyage.nettoyage_intervention(donnees_problem)

    # filtration pour les données non-problématiques
    index_ok_realise = df_intervention_realise['id'].isin(intervention_id_debit_chantier_ok_realise)
    # données qui ne posent pas de problème
    donnees_ok = donnees.copy()
    donnees_ok['intervention_realise'] = donnees_ok['intervention_realise'].loc[index_ok_realise]
    # application de la fonction d'erreur aux lignes non problématiques (elles doivent passées (1))
    code_test_ok = nettoyage.nettoyage_intervention(donnees_ok)
    

    # toutes les lignes de problèmes doivent valoir 0
    res_problem = (code_test_problem['debit_chantier'] == 0).all()
    # toutes les lignes sans problèmes doivent valoir 1 
    res_ok = (code_test_ok['debit_chantier'] == 1).all()

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
    df_names = [    
                    'composant_culture', 'culture', 'intervention_realise', 'intrant', 'noeuds_realise',
                    'plantation_perenne_phases_realise', 
                    'plantation_perenne_realise', 'utilisation_intrant_cible',
                    'utilisation_intrant_realise'        
                ]
    path_data = 'tests/data/test_utilisation_intrant_dose_realise/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # obtention des référentiels
    path_ref = 'data/referentiels/'
    refs_names = [
        'ref_nuisible_edi',
        'ref_correspondance_groupe_cible', 
        'ref_adventice',
        'dose_ref_cible'
    ]

    donnees = import_dfs(refs_names, path_ref, donnees, sep = ',')
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise']

    # filtration pour les données problématiques
    index_problem_realise = df_utilisation_intrant_realise['id'].isin(id_utilisation_intrant_dose_problem_realise)
    # données qui posent problème
    donnees_problem = donnees.copy()
    donnees_problem['utilisation_intrant_realise'] = donnees_problem['utilisation_intrant_realise'].loc[index_problem_realise]
    # application de la fonction d'erreur aux lignes problématiques (elles doivent être signalées (0))
    code_test_problem = nettoyage.nettoyage_utilisation_intrant(donnees_problem, saisie='realise', verbose=True)
    
    # filtration pour les données non-problématiques
    index_ok_realise = df_utilisation_intrant_realise['id'].isin(id_utilisation_intrant_dose_ok_realise)
    # données qui ne posent pas de problème
    donnees_ok = donnees.copy()
    donnees_ok['utilisation_intrant_realise'] = donnees_ok['utilisation_intrant_realise'].loc[index_ok_realise]
    # application de la fonction d'erreur aux lignes non problématiques (elles doivent passées (1))
    code_test_ok = nettoyage.nettoyage_utilisation_intrant(donnees_ok, saisie='realise', verbose=True)
    
    # toutes les lignes de problèmes doivent valoir 0
    res_problem = (code_test_problem['dose_ref'] == 0).all()
    # toutes les lignes sans problèmes doivent valoir 1 
    res_ok = (code_test_ok['dose_ref'] == 1).all()

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
    id_utilisation_intrant_dose_problem_synthetise= list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '0']['id_ligne'])

    # définition des lignes qui ne posent pas problème pour les débits de chantier en réalisé et qui doivent par conséquent, passer le test
    id_utilisation_intrant_dose_ok_synthetise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '1']['id_ligne'])


    # obtention des données
    df_names = [    
                    'composant_culture', 'connection_synthetise', 'culture', 'intervention_synthetise', 'intrant', 'noeuds_synthetise',
                    'plantation_perenne_phases_synthetise', 
                    'plantation_perenne_synthetise', 'utilisation_intrant_cible',
                    'utilisation_intrant_synthetise'        
                ]
    path_data = 'tests/data/test_utilisation_intrant_dose/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # obtention des référentiels
    path_ref = 'data/referentiels/'
    refs_names = [
        'ref_nuisible_edi',
        'ref_correspondance_groupe_cible', 
        'ref_adventice',
        'dose_ref_cible'
    ]

    donnees = import_dfs(refs_names, path_ref, donnees, sep = ',')
    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise']


    # filtration pour les données problématiques
    index_problem_synthetise = df_utilisation_intrant_synthetise['id'].isin(id_utilisation_intrant_dose_problem_synthetise)
    # données qui posent problème
    donnees_problem = donnees.copy()
    donnees_problem['utilisation_intrant_synthetise'] = donnees_problem['utilisation_intrant_synthetise'].loc[index_problem_synthetise]
    # application de la fonction d'erreur aux lignes problématiques (elles doivent être signalées (0))
    code_test_problem = nettoyage.nettoyage_utilisation_intrant(donnees_problem, saisie='synthetise')
    
    # filtration pour les données non-problématiques
    index_ok_synthetise = df_utilisation_intrant_synthetise['id'].isin(id_utilisation_intrant_dose_ok_synthetise)
     # données qui ne posent pas de problème
    donnees_ok = donnees.copy()
    donnees_ok['utilisation_intrant_synthetise'] = donnees_ok['utilisation_intrant_synthetise'].loc[index_ok_synthetise]
    # application de la fonction d'erreur aux lignes non problématiques (elles doivent passées (1))
    code_test_ok = nettoyage.nettoyage_utilisation_intrant(donnees_ok, saisie='synthetise')
    
    # toutes les lignes de problèmes doivent valoir 0
    res_problem = (code_test_problem['dose_ref'] == 0).all()
    # toutes les lignes sans problèmes doivent valoir 1 
    res_ok = (code_test_ok['dose_ref'] == 1).all()

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
    df_names = [    
                    'utilisation_intrant_realise',
                    'utilisation_intrant_synthetise',
                    'intrant',
                    'composant_culture',
                    'utilisation_intrant_cible', 
                    'culture',
                    'intervention_realise', 
                    'intervention_synthetise',
                    'plantation_perenne_realise', 
                    'plantation_perenne_synthetise',
                    'plantation_perenne_phases_realise',
                    'plantation_perenne_phases_synthetise',
                    'noeuds_realise', 'noeuds_synthetise',
                    'connection_synthetise'
                ]
    path_data = 'tests/data/test_utilisation_intrant_dose/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # obtention des référentiels
    path_ref = 'data/referentiels/'
    refs_names = [
        'ref_nuisible_edi',
        'ref_correspondance_groupe_cible', 
        'ref_adventice',
        'dose_ref_cible'
    ]
    donnees = import_dfs(refs_names, path_ref, donnees, sep = ',')

    # obtention de la dose de référence à partir de la fonction get_infos_all_utilisation_intrant
    df_utilisation_intrant_realise = fonctions_utiles.get_infos_all_utilisation_intrant(donnees, saisie = 'realise')
    df_utilisation_intrant_synthetise = fonctions_utiles.get_infos_all_utilisation_intrant(donnees, saisie = 'synthetise')
    
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


def test_identification_pz0_realise():
    """
        Test de l'identification d'un pz0 realise (zone)
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_identification_pz0_realise']

    # obtention des données
    df_names = [    
                    'noeuds_realise',
                    'noeuds_synthetise',
                    'parcelle',
                    'plantation_perenne_realise',
                    'plantation_perenne_synthetise', 
                    'sdc',
                    'synthetise', 
                    'zone'
                ]
    path_data = 'tests/data/test_identification_pz0_entier/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # application de la fonction d'identification des pz0
    code_test = nettoyage.nettoyage_zone(donnees)
    
    df_metadonnees.set_index('id_ligne',inplace = True)
    comparaison = pd.merge(code_test,df_metadonnees[['valeur_attendue']], left_index=True, right_index=True)
    print(comparaison)
    res_test = (comparaison['valeur_attendue'].astype('int') == comparaison['pz0'].astype('int')).all()
    assert res_test


    
def test_identification_pz0_synthetise():
    """
        Test de l'identification d'un pz0 synthetise
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('tests/data/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_identification_pz0_synthetise']

    # obtention des données
    df_names = [    
                    'noeuds_realise',
                    'noeuds_synthetise',
                    'parcelle',
                    'plantation_perenne_realise',
                    'plantation_perenne_synthetise', 
                    'sdc',
                    'synthetise', 
                    'zone'
                ]
    path_data = 'tests/data/test_identification_pz0/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # application de la fonction d'identification des pz0
    code_test = nettoyage.nettoyage_synthetise(donnees)
    
    df_metadonnees.set_index('id_ligne',inplace = True)
    comparaison = pd.merge(code_test,df_metadonnees[['valeur_attendue']], left_index=True, right_index=True)
    print(comparaison)
    res_test = (comparaison['valeur_attendue'].astype('int') == comparaison['pz0'].astype('int')).all()
    assert res_test