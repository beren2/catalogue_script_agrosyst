"""
    Regroupe tous les tests utilisés pour vérifier que le magasin de données "nettoyage" est bien fonctionnel.
"""
import pandas as pd
import numpy as np
from scripts import nettoyage
from scripts import restructuration
from scripts.utils import fonctions_utiles
from scripts import indicateur
from scripts import agregation




def import_df(df_name, path_data, sep, df):
    """
        importe un dataframe au chemin path_data+df_name+'.csv' et le stock dans le dictionnaire 'df' à la clé df_name
    """
    df[df_name] = pd.read_csv(path_data+df_name+'.csv', sep = sep).replace({'\r\n': '\n'}, regex=True)

def import_dfs(df_names, path_data,  df, sep = ','):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans la liste df_names
    """
    for df_name in df_names : 
        import_df(df_name, path_data, sep, df)

    return df


def fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, \
                  metadonnee_file='02_outils/tests/metadonnees_tests_unitaires.csv', \
                    df_ref_names = None, path_ref = '02_outils/data/referentiels/', key_name='id'):
    """
        Fonction qui permet de tester 
    """
    df_metadonnees = pd.read_csv(metadonnee_file)
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == identifiant_test]

    # dictionnaire donnant pour chaque identifiant d'entité (par exemple intervention_id), les colonnes à tester
    colonne_to_test_for_ligne = df_metadonnees.groupby('id_ligne').agg({'colonne_testee' : ','.join}).to_dict()['colonne_testee']
    for (key, value) in colonne_to_test_for_ligne.items():
        colonne_to_test_for_ligne[key] = value.split(',')

    donnees_ = import_dfs(df_names, path_data, {}, sep = ',')
    donnees_ref = {}
    if(not df_ref_names is None):
        # dans le cas où on a des données sensibles, celles-ci sont encryptées et importées
        donnees_ref = import_dfs(df_ref_names, path_ref, {}, sep = ',')
    donnees = donnees_ | donnees_ref
    
    donnees_computed = fonction_to_apply(donnees)
    donnees_computed = donnees_computed.reset_index().set_index(key_name).reset_index()

    res = []
    for entite_id in list(colonne_to_test_for_ligne.keys()):
        colonnes_to_test = colonne_to_test_for_ligne[entite_id]

        # valeur trouvée :
        output = donnees_computed.loc[donnees_computed[key_name] == entite_id]
        output = output[colonnes_to_test].fillna('').astype('str')

        # valeur attendue :
        expected_output = df_metadonnees.loc[(df_metadonnees['id_ligne'] == entite_id) & (df_metadonnees['colonne_testee'].isin(colonnes_to_test))]
        expected_output = expected_output.pivot(columns='colonne_testee', values='valeur_attendue', index='id_ligne').fillna('')

        for colonne_to_test in colonnes_to_test:
            print(output[colonne_to_test].values)
            print(expected_output[colonne_to_test].values)
            if(len(expected_output[colonne_to_test].values) > 0):
                is_null_value_expected = (expected_output[colonne_to_test].values[0] == '')

            if((output[colonne_to_test].values != expected_output[colonne_to_test].values) or (len(output[colonne_to_test].values) == 0 and not is_null_value_expected)):
                res.append(False)
            else:
                res.append(True)

    return res

def test_debit_chantier_intervention_realise():
    """
        Test du débit de chantier des interventions en réalisé
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_debit_chantier_intervention_realise']

    # définition des lignes qui posent problème pour les débits de chantier en réalisé
    intervention_id_debit_chantier_problem_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '0']['id_ligne'])

    # définition des lignes qui ne posent pas problème pour les débits de chantier en réalisé et qui doivent par conséquent, passer le test
    intervention_id_debit_chantier_ok_realise = list(df_metadonnees.loc[df_metadonnees['valeur_attendue'] == '1']['id_ligne'])

    # obtention des données
    df_names = ['intervention_realise']
    path_data = '02_outils/tests/data/test_debit_chantier_intervention_realise/'
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
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
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
    path_data = '02_outils/tests/data/test_utilisation_intrant_dose_realise/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # obtention des référentiels
    path_ref = '02_outils/data/referentiels/'
    refs_names = [
        'ref_nuisible_edi',
        'ref_correspondance_groupe_cible', 
        'ref_adventice',
        'dose_ref_cible', 
        'ref_culture_maa', 
        'ref_acta_traitement_produit'
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
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
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
    path_data = '02_outils/tests/data/test_utilisation_intrant_dose/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    # obtention des référentiels
    path_ref = '02_outils/data/referentiels/'
    refs_names = [
        'ref_nuisible_edi',
        'ref_correspondance_groupe_cible', 
        'ref_adventice',
        'dose_ref_cible', 
        'ref_culture_maa',
        'ref_acta_traitement_produit'
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
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_get_infos_traitement']

    # obtention des données
    path_data = '02_outils/tests/data/test_get_infos_traitement/'
    path_utilisation_intrant_realise = path_data+'utilisation_intrant_realise.csv'
    path_intrant = path_data+'intrant.csv'
    df_utilisation_intrant_realise = pd.read_csv(path_utilisation_intrant_realise, sep = ',')
    df_intrant = pd.read_csv(path_intrant, sep = ',')

    # obtention des métadonnées des "fonctions_tests" (attention, rien à voir avec les tests unitaires, juste des fonctions qui viennent
    # qualifier les données en testant si des valeurs dépassent certaines valeurs seuilles).
    path_data = '02_outils/data/'
    path_metadonnes_tests = path_data+'metadonnees_tests.csv'
    path_metadonnes_seuils = path_data+'metadonnees_seuils.csv'
    df_metadonnees_tests = pd.read_csv(path_metadonnes_tests, sep = ',')
    df_metatonnees_seuils = pd.read_csv(path_metadonnes_seuils, sep = ',')

    # obtention des métadonnées des référentiels
    path_ref_acta_traitement_produit = path_data+'referentiels/ref_acta_traitement_produit.csv'
    df_ref_acta_traitement_produit = pd.read_csv(path_ref_acta_traitement_produit)
    df_ref_acta_traitement_produit = df_ref_acta_traitement_produit.loc[df_ref_acta_traitement_produit['active']]

    # application de la méthode à tester
    utilisation_intrant_id_code_amm_expected = df_metadonnees[['id_ligne', 'valeur_attendue', 'colonne_testee']]
    test_get_infos_traitement_realise = fonctions_utiles.get_infos_traitement(df_utilisation_intrant_realise[['id', 'intrant_id']], df_intrant, df_ref_acta_traitement_produit)

    # on merge les dataframe obtenus et attendus
    left = utilisation_intrant_id_code_amm_expected.rename(columns={
        'id_ligne' : 'id'
    })
    right = test_get_infos_traitement_realise
    merge = pd.merge(left, right, on = 'id') 

    # la valeur attendue doit toujours être égale à la valeur trouvée
    res_ok = (merge['valeur_attendue'].astype('int') == merge['code_amm'].astype('int')).all()

    assert res_ok

def test_get_utilisation_intrant_in_unit():
    """ 
        test de l'obtention de l'utilisation dans la dose souhaitée
    """
    # obtention des données
    path_data = '02_outils/tests/data/test_utilisation_intrant_dose/'
    df_names = [    
                    'utilisation_intrant_realise'     
                ]
    donnees = import_dfs(df_names, path_data, {}, sep = ',')
    path_ref = '02_outils/data/referentiels/'
    refs_names = [
        'conversion_utilisation_intrant'
    ]
    donnees = import_dfs(refs_names, path_ref, donnees, sep = ',')

    donnees['utilisation_intrant'] = donnees['utilisation_intrant_realise']
    fonctions_utiles.get_utilisation_intrant_in_unit(donnees)

    return True

def test_get_dose_ref():
    """
        Test de l'obtention de la dose de référence
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
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
    path_data = '02_outils/tests/data/test_utilisation_intrant_dose/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')


    # obtention des référentiels
    path_ref = '02_outils/data/referentiels/'
    refs_names = [
        'ref_nuisible_edi',
        'ref_correspondance_groupe_cible', 
        'ref_adventice',
        'dose_ref_cible',
        'ref_culture_maa',
        'ref_acta_traitement_produit'
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

def test_identification_pz0():
    """
        Test du tag des sdc par le type de donnees attendue
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_identification_pz0']

    # obtention des données
    df_names = [    
                    'domaine',
                    'dispositif',
                    'sdc',
                    'synthetise',
                    'parcelle',
                    'zone',
                    'intervention_synthetise_agrege',
                    'intervention_realise_agrege'
                ]
    path_data = '02_outils/tests/data/test_identification_pz0/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')
    
    external_data_path = '02_outils/tests/data/test_identification_pz0/'
    import_df('BDD_donnees_attendues_CAN', external_data_path, sep = ',', df = donnees)

    # application de la fonction d'identification des pz0
    result_function = indicateur.identification_pz0(donnees)
    
    df_metadonnees.set_index('id_ligne',inplace = True)
    comparaison = pd.merge(result_function,df_metadonnees[['valeur_attendue']], left_index=True, right_index=True, how = 'left').reset_index()
    
    print(comparaison.loc[comparaison['valeur_attendue'] != comparaison['pz0'],].values)

    res_test = (comparaison['valeur_attendue'] == comparaison['pz0']).all()
    assert res_test
  
def test_connection_synthetise_restructured():
    """
        Test de l'obtention des connexions synthétisés restructurées
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_connection_synthetise_restructured']

    # obtention des données
    df_names = [   
                    'connection_synthetise', 
                    'noeuds_synthetise', 
                    'synthetise', 
                    'sdc', 
                    'domaine',
                    'culture'
                ]
    path_data = '02_outils/tests/data/test_connection_synthetise_restructured/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    connection_synthetise_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'culture_intermediaire_id'][['id_ligne', 'valeur_attendue']]
    connection_synthetise = restructuration.restructuration_connection_synthetise(donnees)

    left = connection_synthetise_expected[['id_ligne', 'valeur_attendue']].rename(columns={'id_ligne' : 'connection_synthetise_id', 'valeur_attendue' : 'culture_intermediaire_id_expected'})
    right = connection_synthetise.reset_index()[['id', 'culture_intermediaire_id']].rename(columns={'id' : 'connection_synthetise_id'})
    merge = pd.merge(left, right, on='connection_synthetise_id', how='left')

    # on enlève ceux pour lesquelles on est sensé trouver "NaN" 
    merge = merge.dropna()

    # on vérifie que toutes les culture_id sont bien conforme à ceux qu'on attendait 
    res_valeur_ok = (merge['culture_intermediaire_id_expected'] == merge['culture_intermediaire_id']).all()

    assert res_valeur_ok

def test_intervention_synthetise_restructured():
    """
        Test de l'obtention des combinaisons outils d intervention synthetise restructuree
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_intervention_synthetise_restructured']

    # obtention des données
    df_names = ['intervention_synthetise',
                'synthetise',
                'intervention_synthetise_agrege',
                'combinaison_outil',
                'domaine']

    path_data = '02_outils/tests/data/test_intervention_synthetise_restructured/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    intervention_synthetise_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'combinaison_outil_id'][['id_ligne', 'valeur_attendue']]
    intervention_synthetise = restructuration.restructuration_intervention_synthetise(donnees)

    left = intervention_synthetise_expected[['id_ligne', 'valeur_attendue']].rename(columns={'id_ligne' : 'intervention_synthetise_id', 'valeur_attendue' : 'combinaison_outil_id_expected'})
    right = intervention_synthetise.reset_index().rename(columns={'id' : 'intervention_synthetise_id'})
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # on vérifie que toutes les culture_id sont bien conforme à ceux qu'on attendait 
    res_valeur_ok = (merge['combinaison_outil_id_expected'] == merge['combinaison_outil_id']).all()

    assert res_valeur_ok

def test_restructuration_noeuds_realise():
    """
        Test de l'obtention des noeuds realises restructures
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_noeuds_realise_restructured']

    # obtention des données
    df_names = [   
                    'noeuds_realise', 'zone'
                ]
    path_data = '02_outils/tests/data/test_noeuds_realise_restructured/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    noeuds_realise_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'precedent_noeuds_realise_id'][['id_ligne', 'valeur_attendue']]
    noeuds_realise = restructuration.restructuration_noeuds_realise(donnees)

    left = noeuds_realise_expected[['id_ligne', 'valeur_attendue']].rename(columns={'id_ligne' : 'noeuds_realise_id', 'valeur_attendue' : 'precedent_noeuds_realise_id_expected'})
    right = noeuds_realise.reset_index()[['id', 'precedent_noeuds_realise_id']].rename(columns={'id' : 'noeuds_realise_id'})
    merge = pd.merge(left, right, on='noeuds_realise_id', how='left')

    # on enlève ceux pour lesquelles on est sensé trouver "NaN" 
    merge = merge.dropna()

    # on vérifie que toutes les culture_id sont bien conforme à ceux qu'on attendait 
    res_valeur_ok = (merge['precedent_noeuds_realise_id_expected'] == merge['precedent_noeuds_realise_id']).all()

    assert res_valeur_ok

def test_restructuration_recolte_rendement_prix():
    """
        Test de l'obtention des recoltes rendement prix restructurés
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_recolte_rendement_prix_restructured']

    # obtention des données
    df_names = [   
                    'action_realise_agrege', 'action_synthetise_agrege', 
                    'recolte_rendement_prix', 'composant_culture', 
                    'domaine', 'culture'
                ]

    path_data = '02_outils/tests/data/test_recolte_rendement_prix_restructured/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    recolte_rendement_prix_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'composant_culture_id'][
        ['id_ligne', 'valeur_attendue']
    ]
    recolte_rendement_prix = restructuration.restructuration_recolte_rendement_prix(donnees)

    left = recolte_rendement_prix_expected[['id_ligne', 'valeur_attendue']].rename(columns={
        'id_ligne' : 'recolte_rendement_prix_id', 'valeur_attendue' : 'composant_culture_id_expected'
    })
    right = recolte_rendement_prix.reset_index()[['id', 'composant_culture_id']].rename(columns={
        'id' : 'recolte_rendement_prix_id'
    })
    merge = pd.merge(left, right, on='recolte_rendement_prix_id', how='left')

    # on enlève ceux pour lesquelles on est sensé trouver "NaN" 
    merge = merge.dropna()

    # on vérifie que toutes les culture_id sont bien conforme à ceux qu'on attendait 
    res_valeur_ok = (merge['composant_culture_id'] == merge['composant_culture_id_expected']).all()

    assert res_valeur_ok


def test_get_aggreged_from_utilisation_intrant_synthetise():
    """
        Test de l'obtention des agregation depuis l'utilisation intrant synthetise
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_get_aggreged_from_utilisation_intrant_synthetise']

    # obtention des données
    df_names = [   
                    'utilisation_intrant_synthetise', 'action_synthetise', 
                    'intervention_synthetise', 'connection_synthetise', 
                    'noeuds_synthetise', 'plantation_perenne_phases_synthetise',
                    'plantation_perenne_synthetise','synthetise',
                    'sdc','dispositif'
                ]
                
    path_data = '02_outils/tests/data/test_get_aggreged_from_utilisation_intrant_synthetise/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    aggreged_utilisation_intrant_synthetise_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'toutes'][
        ['id_ligne', 'valeur_attendue']
    ]
    aggreged_utilisation_intrant_synthetise = agregation.get_aggreged_from_utilisation_intrant_synthetise(donnees)
    aggreged_utilisation_intrant_synthetise = aggreged_utilisation_intrant_synthetise.apply(lambda row: ','.join(row.values.astype(str)), axis=1)

    left = aggreged_utilisation_intrant_synthetise_expected[['id_ligne', 'valeur_attendue']].rename(columns={
        'id_ligne' : 'utilisation_intrant_synthetise_id', 'valeur_attendue' : 'aggreged_utilisation_intrant_synthetise_expected'
    })
    right = aggreged_utilisation_intrant_synthetise.reset_index().rename(columns={
        'id' : 'utilisation_intrant_synthetise_id',
        0 : 'aggreged_utilisation_intrant_synthetise'
    })
    merge = pd.merge(left, right, on='utilisation_intrant_synthetise_id', how='left')

    # on enlève ceux pour lesquelles on est sensé trouver "NaN" 
    merge = merge.dropna()

    # on vérifie que toutes les culture_id sont bien conforme à ceux qu'on attendait 
    res_valeur_ok = (merge['aggreged_utilisation_intrant_synthetise'] == merge['aggreged_utilisation_intrant_synthetise_expected']).all()

    assert res_valeur_ok


def test_get_aggreged_from_utilisation_intrant_realise():
    """
        Test de l'obtention des agregation depuis l'utilisation intrant realise
    """
    # lecture du fichier de métadonnées sur les tests
    df_metadonnees = pd.read_csv('02_outils/tests/metadonnees_tests_unitaires.csv')
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == 'test_get_aggreged_from_utilisation_intrant_realise']

    # obtention des données
    df_names = [   
                    'utilisation_intrant_realise', 'action_realise', 
                    'intervention_realise', 'noeuds_realise', 
                    'plantation_perenne_phases_realise','plantation_perenne_realise',
                    'zone','parcelle','sdc','dispositif','domaine'
                ]
    
    path_data = '02_outils/tests/data/test_get_aggreged_from_utilisation_intrant_realise/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')

    aggreged_utilisation_intrant_realise_expected = df_metadonnees.loc[df_metadonnees['colonne_testee'] == 'toutes'][
        ['id_ligne', 'valeur_attendue']
    ]
    aggreged_utilisation_intrant_realise = agregation.get_aggreged_from_utilisation_intrant_realise(donnees)
    aggreged_utilisation_intrant_realise = aggreged_utilisation_intrant_realise.apply(lambda row: ','.join(row.values.astype(str)), axis=1)

    left = aggreged_utilisation_intrant_realise_expected[['id_ligne', 'valeur_attendue']].rename(columns={
        'id_ligne' : 'utilisation_intrant_realise_id', 'valeur_attendue' : 'aggreged_utilisation_intrant_realise_expected'
    })
    right = aggreged_utilisation_intrant_realise.reset_index().rename(columns={
        'id' : 'utilisation_intrant_realise_id',
        0 : 'aggreged_utilisation_intrant_realise'
    })
    merge = pd.merge(left, right, on='utilisation_intrant_realise_id', how='left')

    # on enlève ceux pour lesquelles on est sensé trouver "NaN" 
    merge = merge.dropna()

    # on vérifie que toutes les culture_id sont bien conforme à ceux qu'on attendait 
    res_valeur_ok = (merge['aggreged_utilisation_intrant_realise'] == merge['aggreged_utilisation_intrant_realise_expected']).all()

    assert res_valeur_ok



def test_get_typologie_culture_CAN():
    """
        Test de l'obtention des typologies d'espece et de cultures 
    """
    identifiant_test = 'test_get_typologie_culture_CAN'
    df_names = [   
                    'composant_culture', 'culture', 
                    'espece',
                    'typo_especes_typo_culture','typo_especes_typo_culture_marai' # referentiel CAN
                ]
    path_data = '02_outils/tests/data/test_get_typologie_culture_CAN/'
    fonction_to_apply = indicateur.get_typologie_culture_CAN

    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, key_name='culture_id')

    res = pd.Series(res).fillna(False).all()

    assert res


def extract_good_rotation_diagram():
    """
        Test de l'obtention de la liste de "bon" synthétisé pour la suite (soit la fonction poids des rotations en synthétisé)
        ATTENTION va prendre les même données d'entrée que la fonction test_get_connexion_weight_in_synth_rotation(. donc path_data ne change pas
    """
    df_names = [   
                    'noeuds_synthetise', 'connection_synthetise'
                ]
    path_data = '02_outils/tests/data/test_get_connexion_weight_in_synth_rotation/'
    donnees = import_dfs(df_names, path_data, {}, sep = ',')
    res_to_test, _ = indicateur.extract_good_rotation_diagram(donnees)
    
    good_to_check = ['fr.inra.agrosyst.api.entities.practiced.PracticedSystem_d4a1b64c-afa0-440f-92e1-30a483871ab4',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_00b5a0b4-39a6-4822-802b-e81fd44386a2',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_05e5d9d6-ad2b-43b2-b37a-1f32850e37a1',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_61f75804-3823-4fae-9ce1-82bfa3d7e41e',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_41ae9d22-5515-44d8-9a7f-8254c42149eb',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_2f68d851-cb30-402f-bfc6-b0abf37c49a8',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_1e606337-4238-437b-9856-a302b2431efd',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_91611752-8cd2-42f1-b19f-97186597ab64',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_445dd407-58f6-403e-8dd6-8352166a0131',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_0316e326-6369-4ec7-ab50-b983c3aa0b3d',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_000f911f-5e67-4280-ae77-35098c17aa5d',
    'fr.inra.agrosyst.api.entities.practiced.PracticedSystem_592b3792-8ad0-4213-ab98-a948f444ed04']

    if set(list(res_to_test)) == set(good_to_check) : res = True
    else : res = False

    assert res



def test_get_connexion_weight_in_synth_rotation():
    """
        Test de l'obtention des poids des rotations en synthétisé
    """
    identifiant_test = 'test_get_connexion_weight_in_synth_rotation'
    df_names = [   
                    'noeuds_synthetise', 'connection_synthetise'
                ]
    path_data = '02_outils/tests/data/test_get_connexion_weight_in_synth_rotation/'
    fonction_to_apply = indicateur.get_connexion_weight_in_synth_rotation_for_test

    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, key_name='connexion_id')

    res = pd.Series(res).fillna(False).all()

    assert res