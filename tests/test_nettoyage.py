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

    print(res_problem)
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
    path_intrant = path_data+'intrant.csv'
    path_intervention_realise = path_data+'intervention_realise.csv'
    path_plantation_perenne_realise = path_data+'plantation_perenne_realise.csv'
    path_plantation_perenne_phase_realise = path_data+'plantation_perenne_phase_realise.csv'
    path_composant_culture = path_data+'composant_culture.csv'
    path_noeuds_realise = path_data+'noeuds_realise.csv'
    path_utilisation_intrant_cible = path_data+'utilisation_intrant_cible.csv'
    path_intervention_synthetise = path_data+'intervention_synthetise.csv'
    path_plantation_perenne_phase_synthetise = path_data+'plantation_perenne_phase_synthetise.csv'
    path_plantation_perenne_synthetise = path_data+'plantation_perenne_synthetise.csv'
    path_noeuds_synthetise = path_data+'noeuds_synthetise.csv'
    path_utilisation_intrant_synthetise = path_data+'utilisation_intrant_synthetise.csv'
    path_connection_synthetise = path_data+'connection_synthetise.csv'
    path_culture = path_data+'culture.csv'

    df_utilisation_intrant_realise = pd.read_csv(path_utilisation_intrant_realise, sep = ',') 
    df_intrant = pd.read_csv(path_intrant, sep = ',') 
    df_intervention_realise = pd.read_csv(path_intervention_realise, sep = ',') 
    df_plantation_perenne_realise = pd.read_csv(path_plantation_perenne_realise, sep =',') 
    df_plantation_perenne_phase_realise = pd.read_csv(path_plantation_perenne_phase_realise, sep =',') 
    df_composant_culture = pd.read_csv(path_composant_culture, sep = ',')
    df_noeuds_realise = pd.read_csv(path_noeuds_realise, sep = ',')
    df_utilisation_intrant_cible = pd.read_csv(path_utilisation_intrant_cible, sep = ',')
    df_intervention_synthetise = pd.read_csv(path_intervention_synthetise, sep = ',')
    df_plantation_perenne_phase_synthetise = pd.read_csv(path_plantation_perenne_phase_synthetise, sep = ',')
    df_plantation_perenne_synthetise = pd.read_csv(path_plantation_perenne_synthetise, sep = ',')
    df_culture = pd.read_csv(path_culture, sep =',')
    df_noeuds_synthetise = pd.read_csv(path_noeuds_synthetise, sep = ',')
    df_utilisation_intrant_synthetise = pd.read_csv(path_utilisation_intrant_synthetise, sep = ',')
    df_connection_synthetise = pd.read_csv(path_connection_synthetise, sep = ',')

    # test de l'affectation des informations du traitement
    test_get_infos_traitement_realise = fonctions_utiles.get_infos_traitement(df_utilisation_intrant_realise[['id', 'intrant_id']], df_intrant)
    test_get_infos_traitement_synthetise = fonctions_utiles.get_infos_traitement(df_utilisation_intrant_synthetise[['id', 'intrant_id']], df_intrant)
    test_get_infos_traitement_ = pd.concat([test_get_infos_traitement_realise, test_get_infos_traitement_synthetise], axis=0)

    # test de l'affectation des informations de la culture
    test_get_infos_culture_realise = fonctions_utiles.get_infos_culture_realise(
        df_utilisation_intrant_realise, 
        df_intervention_realise, 
        df_noeuds_realise,
        df_plantation_perenne_realise,
        df_plantation_perenne_phase_realise,
        df_composant_culture,
    )
    test_get_infos_culture_synthetise = fonctions_utiles.get_infos_culture_synthetise(
        df_utilisation_intrant_synthetise, 
        df_intervention_synthetise, 
        df_connection_synthetise,
        df_noeuds_synthetise,
        df_plantation_perenne_synthetise,
        df_plantation_perenne_phase_synthetise,
        df_composant_culture,
        df_culture
    )
    test_get_infos_culture = pd.concat([test_get_infos_culture_realise, test_get_infos_culture_synthetise], axis=0)

    # test de l'affectation des informations de la cible
    test_get_infos_cible = fonctions_utiles.get_infos_cible(
        df_utilisation_intrant_cible
    )

    df_utilisation_intrant = pd.concat([df_utilisation_intrant_realise, df_utilisation_intrant_synthetise], axis=0)

    # Obtention des informations des traitements
    left = df_utilisation_intrant
    right = test_get_infos_traitement_[[
        'id',
        'id_produit', 
        'id_traitement', 
        'code_amm', 
        'code_traitement_maa'
    ]]
    total_merge_1 = pd.merge(left, right, on = 'id', how='left')

    # Obtention des informations des cultures
    left = total_merge_1 
    right = test_get_infos_culture[[
        'id', 
        'code_culture_maa'
    ]]
    total_merge_2 = pd.merge(left, right, on = 'id', how='left')

    # Obtention des informations sur les cibles
    left = total_merge_2
    right = test_get_infos_cible[[
        'id', 
        'code_groupe_cible_maa'
    ]]
    total_merge_3 = pd.merge(left, right, on = 'id', how='left')

    # On obtient une ligne dont la clé primaire est : [['id', 'code_amm', 'code_culture_maa', 'code_traitement_maa', 'code_groupe_cible_maa']]

    # test de l'obtention de la dose de référence
    test_get_dose_ref_ = fonctions_utiles.get_dose_ref(
        total_merge_3
    )

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
