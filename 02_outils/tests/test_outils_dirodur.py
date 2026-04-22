"""
    Regroupe tous les tests utilisés pour vérifier que les outils "Dirodur" tournent correctement
"""
import geopandas as gpd
import pandas as pd
from scripts import outils_dirodur
from scripts.utils import dirodur_utiles

def import_df(df_name, path_data, sep, df, file_format='csv'):
    """
        importe un dataframe au chemin path_data+df_name+'.csv' et le stock dans le dictionnaire 'df' à la clé df_name
    """
    if file_format == 'csv' :
        df[df_name] = pd.read_csv(path_data+df_name+'.'+file_format, sep = sep, 
                                  dtype = {'codeinsee':str,
                                            'departement':str,
                                            'codepostal':str,
                                            'region':str,
                                            'arrondissement_code':str,
                                            'bassin_vie':str,
                                            'zone_emploi':str,
                                            
                                            'cell':str})
    if file_format == 'json' and df_name.startswith('geoVec') :
        # Utilise geopandas pour les json formater en geojson. Le nom du fichier json doit alors commencer par geoVec
        df[df_name] = gpd.read_file(path_data+df_name+'.'+file_format)
    if file_format == 'gpkg' :
        df[df_name] = gpd.read_file(path_data+df_name+'.'+file_format)

def import_dfs(df_names, data_path, sep = ',', df=None, file_format='csv'):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans la liste df_names
    """
    if df is None:
        df = {}
    for df_name in df_names : 
        import_df(df_name, path_data=data_path, df = df, sep = sep, file_format=file_format)

    return df

def import_dfs_withExtension(df_names_withExt:dict, data_path):
    """
        stocke dans le dictionnaire df tous les dataframes indiqués dans le dictionnaire df_names_withExt qui prend en key l'extension des fichiers, lié à une liste de nom de fichiers
    """
    all_df = {}
    for x in df_names_withExt :
        if isinstance(x, str) and x in {'json', 'gpkg', 'csv'}:
            df_names = df_names_withExt[x]
            df_dict = import_dfs(df_names, data_path, file_format=x)
            all_df = {**all_df, **df_dict}
        else :
            raise Exception("Les clefs du dictionnaire doivent être 'csv' ou 'json' ou 'gpkg'") 
    return all_df

def fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, metadonnee_file='02_outils/tests/metadonnees_tests_unitaires.csv', df_ref_names = None, path_ref = '02_outils/data/referentiels/', key_name='id', multi_extension:bool = False):
    """
        Fonction qui permet de tester 
    """
    df_metadonnees = pd.read_csv(metadonnee_file)
    df_metadonnees = df_metadonnees.loc[df_metadonnees['identifiant_test'] == identifiant_test]

    # dictionnaire donnant pour chaque identifiant d'entité (par exemple intervention_id), les colonnes à tester
    colonne_to_test_for_ligne = df_metadonnees.groupby('id_ligne').agg({'colonne_testee' : ','.join}).to_dict()['colonne_testee']
    for (key, value) in colonne_to_test_for_ligne.items():
        colonne_to_test_for_ligne[key] = value.split(',')

    if multi_extension :
        donnees_ = import_dfs_withExtension(df_names, data_path = path_data)
    else :
        donnees_ = import_dfs(df_names, path_data, df = {}, sep = ',')
    donnees_ref = {}
    if(not df_ref_names is None):
        # dans le cas où on a des données sensibles, celles-ci sont encryptées et importées
        donnees_ref = import_dfs(df_ref_names, path_ref, df = {}, sep = ',')
    donnees = donnees_ | donnees_ref
    
    donnees_computed = fonction_to_apply(donnees)
    #donnees_computed.to_csv('~/Bureau/Datagrosyst/catalogue_script_agrosyst/02_outils/tests/'+'TEST_RESULT_'+ identifiant_test +'.csv')

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
            print(expected_output[colonne_to_test].values == output[colonne_to_test].values)
            if(len(expected_output[colonne_to_test].values) > 0):
                is_null_value_expected = (expected_output[colonne_to_test].values[0] == '')

            if((output[colonne_to_test].values != expected_output[colonne_to_test].values) or (len(output[colonne_to_test].values) == 0 and not is_null_value_expected)):
                res.append(False)
            else:
                res.append(True)

    return res

def test_get_temporal_status_for_each_sdc_dirodur():
    """
        Test de l'obtention des informations sur l'etat_temporel des sdc Dirodur
    """

    identifiant_test = 'test_get_temporal_status_for_each_sdc_dirodur'
    df_names = [
        'synthetise', # util + etat_temp
        'sdc', # util + etat_temp
        'typologie_assol_can_realise', # util
        'typologie_can_rotation_synthetise', # util
        'entite_unique_par_sdc_nettoyage', # util
        'sdc_realise_performance', # util
        'synthetise_synthetise_performance', # util
        'intervention_synthetise_agrege', # util
        'intervention_realise_agrege', # util
        'identification_pz0', # etat_temporel
        'zone', # etat_temporel
        'parcelle' # etat_temporel
    ]
    path_data = '02_outils/tests/data/test_get_temporal_status_for_each_sdc_dirodur/'
    fonction_to_apply = outils_dirodur.get_temporal_status_for_each_sdc_dirodur
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, key_name='sdc_id')

def test_get_intervention_realise_culture_outils_can():
    """
        Test de l'obtention des qualification de rendement pour le magasin DiRoDur
    """

    identifiant_test = 'test_get_rendement_realise_filtre_outils_dirodur'
    df_names = [   
        'variete',
        'espece',
        'composant_culture',
        'destination_valorisation',
        'recolte_rendement_prix',
        'recolte_rendement_prix_restructure',
        'action_realise',
        'action_realise_agrege'
    ]
    path_data = '02_outils/tests/data/test_get_rendement_realise_filtre_outils_dirodur/'

    path_ref = '02_outils/data/external_data/'
    refs_names = [
        'correspondance_destination_gcpe_dirodur'
    ]

    fonction_to_apply = outils_dirodur.get_rendement_filtre_realise_outils_dirodur    
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, df_ref_names = refs_names, path_ref = path_ref)

    assert all(res)

def test_get_intervention_synthetise_culture_outils_can():
    """
        Test de l'obtention des qualification de rendement pour le magasin DiRoDur
    """

    identifiant_test = 'test_get_rendement_synthetise_filtre_outils_dirodur'
    df_names = [   
        'variete',
        'espece',
        'composant_culture',
        'destination_valorisation',
        'recolte_rendement_prix',
        'recolte_rendement_prix_restructure',
        'action_synthetise',
        'action_synthetise_agrege'
    ]
    path_data = '02_outils/tests/data/test_get_rendement_synthetise_filtre_outils_dirodur/'

    path_ref = '02_outils/data/external_data/'
    refs_names = [
        'correspondance_destination_gcpe_dirodur'
    ]

    fonction_to_apply = outils_dirodur.get_rendement_filtre_synthetise_outils_dirodur    
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, df_ref_names = refs_names, path_ref = path_ref)

    assert all(res)


def test_get_itk_filtre_outils_dirodur():
    """
        Test de l'obtention des fomtres sur les itk pour le magasin DiRoDur
        TODO : FINALISER CE TEST (normal si ne passe pas 24/06/2026) 
    """

    identifiant_test = 'test_get_itk_filtre_outils_dirodur'
    df_names = [   
        'sdc', 
        'synthetise',
        'itk_realise_performance',
        'itk_synthetise_performance',
        'connection_synthetise',
        'noeuds_synthetise',
        'noeuds_synthetise_restructure',
        'noeuds_realise',
        'parcelle',
        'typologie_can_culture',
        'zone'
    ]

    path_data = '02_outils/tests/data/test_get_itk_filtre_outils_dirodur/'

    fonction_to_apply = outils_dirodur.get_itk_filtre_outils_dirodur
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)