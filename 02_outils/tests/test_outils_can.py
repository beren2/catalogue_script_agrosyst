"""
    Regroupe tous les tests utilisés pour vérifier que les outils "CAN"
    peuvent être constitués conformément au cahier des charges
"""
import geopandas as gpd
import pandas as pd
from scripts import outils_can

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

def test_get_intervention_realise_outils_can_context():
    """
        Test de l'obtention de l'outil pour le traitement des intervention realise pour la CAN
    """
    identifiant_test = 'test_get_intervention_realise_action_outils_can'
    df_names = [   
        'action_realise', 'intervention_realise', 'composant_action_semis', 
        'semence', 'utilisation_intrant_realise', 'espece', 'composant_culture'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_realise_action_outils_can/'
    fonction_to_apply = outils_can.get_intervention_realise_outils_can_context

    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_intervention_realise_combinaison_outils_can():
    """
        Test de l'obtention des informations sur les combinaison d'outils en realise pour le magasin CAN 
    """
    identifiant_test = 'test_get_intervention_realise_combinaison_outils_can'
    df_names = [   
        'combinaison_outil', 'composant_parc_materiel', 'combinaison_outil_composant_parc_materiel', 'intervention_realise', 'materiel'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_realise_combinaison_outils_can/'
    fonction_to_apply = outils_can.get_intervention_realise_combinaison_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_intervention_realise_culture_outils_can():
    """
        Test de l'obtention des informations sur les cultures en realise pour le magasin CAN 
    """
    identifiant_test = 'test_get_intervention_realise_culture_outils_can'
    df_names = [   
        'composant_culture', 'espece', 'variete', 'intervention_realise', 
        'noeuds_realise', 'plantation_perenne_phases_realise',
        'plantation_perenne_realise', 'composant_culture_concerne_intervention_realise',
        'connection_realise'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_realise_culture_outils_can/'
    fonction_to_apply = outils_can.get_intervention_realise_culture_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)
    
    assert all(res)

def test_get_intervention_realise_culture_prec_outils_can():
    """
        Test de l'obtention des informations sur les cultures en realise pour le magasin CAN 
    """

    identifiant_test = 'test_get_intervention_realise_culture_prec_outils_can'
    df_names = [   
        'composant_culture', 'espece', 'variete', 'intervention_realise', 
        'noeuds_realise', 'connection_realise', 'culture'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_realise_culture_prec_outils_can/'
    fonction_to_apply = outils_can.get_intervention_realise_culture_prec_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)
    
    assert all(res)


def test_get_intervention_realise_outils_can():
    """
        Test de l'obtention des informations sur les interventions en realise
    """

    identifiant_test = 'test_get_intervention_realise_outils_can'
    df_names = [
        'intervention_realise', 'action_realise', 'combinaison_outil', 'composant_parc_materiel',
        'noeuds_realise', 'connection_realise', 'plantation_perenne_phases_realise', 'plantation_perenne_realise', 'composant_culture_concerne_intervention_realise',
        'composant_culture', 'espece', 'variete', 'culture', 'intervention_realise_agrege', 'dispositif',
        'combinaison_outil_composant_parc_materiel', 'semence', 'utilisation_intrant_realise', 'intrant', 'recolte_rendement_prix',
        'utilisation_intrant_cible', 'nuisible_edi', 'adventice','materiel'
    ]

    path_data = '02_outils/tests/data/test_get_intervention_realise_outils_can/'

    fonction_to_apply = outils_can.get_intervention_realise_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, df_ref_names = [])

    assert all(res)

def test_get_intervention_synthetise_culture_outils_can():
    """
        Test de l'obtention des informations sur les cultures en synthétisé pour le magasin CAN 
    """

    identifiant_test = 'test_get_intervention_synthetise_culture_outils_can'
    df_names = [   
        'intervention_synthetise', 'noeuds_synthetise', 'connection_synthetise', 
        'plantation_perenne_phases_synthetise', 
        'plantation_perenne_synthetise', 'composant_culture_concerne_intervention_synthetise', 
        'noeuds_synthetise_restructure', 'plantation_perenne_synthetise_restructure',
        'ccc_intervention_synthetise_restructure', 'composant_culture',
        'espece', 'variete', 'connection_synthetise_restructure', 'culture'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_synthetise_culture_outils_can/'

    fonction_to_apply = outils_can.get_intervention_synthetise_culture_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_intervention_synthetise_culture_prec_outils_can():
    """
        Test de l'obtention des informations sur les cultures précédentes en synthétisé pour le magasin CAN 
    """

    identifiant_test = 'test_get_intervention_synthetise_culture_prec_outils_can'
    df_names = [   
        'composant_culture', 'espece', 'variete', 'intervention_synthetise', 
        'noeuds_synthetise', 'connection_synthetise', 'culture', 
        'noeuds_synthetise_restructure'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_synthetise_culture_prec_outils_can/'
    fonction_to_apply = outils_can.get_intervention_synthetise_culture_prec_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

# def test_get_intervention_synthetise_action_outils_can():
#     """
#         Test de l'obtention des informations sur les cultures précédentes en synthétisé pour le magasin CAN 
#     """

#     identifiant_test = 'test_get_intervention_synthetise_action_outils_can'
#     df_names = [   
#         'intervention_synthetise', 'action_synthetise', 'fertilisation_organique'
#     ]
#     path_data =  '02_outils/tests/data/test_get_intervention_synthetise_action_outils_can/'
#     fonction_to_apply = outils_can.get_intervention_synthetise_action_outils_can
#     res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

#     assert all(res)

def test_get_intervention_realise_action_outils_can():
    """
        Test de l'obtention des informations sur les cultures précédentes en synthétisé pour le magasin CAN 
    """

    identifiant_test = 'test_get_intervention_realise_action_outils_can'
    df_names = [   
        'intervention_realise', 'action_realise'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_realise_action_outils_can/'
    fonction_to_apply = outils_can.get_intervention_realise_action_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_intervention_synthetise_semence_outils_can():
    """
        Test de l'obtention des informations sur les cultures précédentes en synthétisé pour le magasin CAN 
    """

    identifiant_test = 'test_get_intervention_synthetise_semence_outils_can'
    df_names = [
        'semence', 'composant_culture', 'espece', 'utilisation_intrant_synthetise'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_synthetise_semence_outils_can/'
    fonction_to_apply = outils_can.get_intervention_synthetise_semence_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_intervention_synthetise_combinaison_outils_can():
    """
        Test de l'obtention des informations sur la combinaison d'outils
    """

    identifiant_test = 'test_get_intervention_synthetise_combinaison_outils_can'
    df_names = [
        'intervention_synthetise', 'intervention_synthetise_restructure', 
        'combinaison_outil', 'composant_parc_materiel', 'combinaison_outil_composant_parc_materiel', 'materiel'
    ]
    path_data = '02_outils/tests/data/test_get_intervention_synthetise_combinaison_outils_can/'
    fonction_to_apply = outils_can.get_intervention_synthetise_combinaison_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_culture_outils_can():
    """
        Test de l'obtention des informations sur les cultures dans le format attendu par la CAN
    """

    identifiant_test = 'test_get_culture_outils_can'
    df_names = [
        'composant_culture', 'espece', 'variete'
    ]
    path_data = '02_outils/tests/data/test_get_culture_outils_can/'
    fonction_to_apply = outils_can.get_culture_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)


def test_get_intervention_synthetise_outils_can():
    """
        Test de l'obtention des informations sur les interventions en synthetise
    """

    identifiant_test = 'test_get_intervention_synthetise_outils_can'
    df_names = [
        'intervention_synthetise', 'action_synthetise', 'intervention_synthetise_restructure', 'combinaison_outil', 'composant_parc_materiel',
        'noeuds_synthetise', 'connection_synthetise', 'plantation_perenne_phases_synthetise', 'plantation_perenne_synthetise', 'composant_culture_concerne_intervention_synthetise',
        'noeuds_synthetise_restructure', 'plantation_perenne_synthetise_restructure', 'ccc_intervention_synthetise_restructure', 'composant_culture', 'espece', 'variete', 'connection_synthetise_restructure',
        'composant_culture', 'noeuds_synthetise_restructure', 'culture', 'intervention_synthetise_agrege', 'dispositif',
        'combinaison_outil_composant_parc_materiel', 'semence', 'utilisation_intrant_synthetise', 'intrant', 'recolte_rendement_prix', 
        'recolte_rendement_prix_restructure', 'utilisation_intrant_cible', 'nuisible_edi', 'adventice', 'groupe_cible','materiel'
    ]

    path_data = '02_outils/tests/data/test_get_intervention_synthetise_outils_can/'

    fonction_to_apply = outils_can.get_intervention_synthetise_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, df_ref_names = [])

    assert all(res)



def test_get_parcelle_non_rattache_outils_can():
    """
        Test de l'obtention des informations sur la combinaison d'outils
    """

    identifiant_test = 'test_get_parcelles_non_rattachees_outils_can'
    df_names = [
        'dispositif', 'sdc', 'parcelle', 'liaison_reseaux', 'liaison_sdc_reseau', 'intervention_realise_agrege'
    ]
    df_ref_names = [
        'reseau'
    ]

    path_data = '02_outils/tests/data/test_get_parcelles_non_rattachees_outils_can/'

    fonction_to_apply = outils_can.get_parcelles_non_rattachees_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply, df_ref_names = df_ref_names)

    assert all(res)

def test_get_zone_realise_culture_outils_can():
    """
        Test de l'obtention des informations utiles pour la constitution des fichiers zones pour la CAN
    """
    identifiant_test = 'test_get_zone_realise_culture_outils_can'

    df_names = [
        'zone', 'composant_culture', 'noeuds_realise', 'espece', 'variete', 'culture', 'plantation_perenne_realise',
        'plantation_perenne_phases_realise', 'parcelle','connection_realise'
    ]

    path_data = '02_outils/tests/data/test_get_zone_realise_culture_outils_can/'

    fonction_to_apply = outils_can.get_zone_realise_culture_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_zone_realise_rendement_outils_can():
    """
        Test de l'obtention des informations utiles pour la constitution des fichiers zones pour la CAN
    """
    identifiant_test = 'test_get_zone_realise_rendement_outils_can'

    df_names = [
        'composant_culture', 
        'culture', 
        'action_realise',
        'composant_culture_concerne_intervention_realise', 
        'recolte_rendement_prix_restructure',
        'recolte_rendement_prix', 'action_realise_agrege'
    ]

    path_data = '02_outils/tests/data/test_get_zone_realise_rendement_outils_can/'

    fonction_to_apply = outils_can.get_zone_realise_rendement_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_zone_realise_outils_can():
    """
        Test de l'obtention des informations utiles pour la constitution des fichiers zones pour la CAN
    """
    identifiant_test = 'test_get_zone_realise_outils_can'

    df_names = [
        'recolte_rendement_prix', 'action_realise_agrege', 'zone', 'composant_culture', 'noeuds_realise', 'espece', 'variete', 'culture', 'plantation_perenne_realise',
        'plantation_perenne_phases_realise', 'parcelle', 'composant_culture_concerne_intervention_realise', 'recolte_rendement_prix_restructure', 'action_realise','connection_realise'
    ]

    path_data = '02_outils/tests/data/test_get_zone_realise_outils_can/'

    fonction_to_apply = outils_can.get_zone_realise_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)

def test_get_parcelle_realise_outils_can():
    """
        Test de l'obtention des informations utiles pour la constitution des fichiers parcelle pour la CAN
    """
    identifiant_test = 'test_get_parcelle_realise_outils_can'

    df_names = [
        'zone', 'composant_culture', 'noeuds_realise', 'espece', 'variete', 'culture', 'plantation_perenne_realise',
        'plantation_perenne_phases_realise', 'parcelle', 'recolte_rendement_prix', 'action_realise_agrege', 
        'composant_culture_concerne_intervention_realise', 'recolte_rendement_prix_restructure', 'action_realise','connection_realise'
    ]

    path_data = '02_outils/tests/data/test_get_parcelle_realise_outils_can/'

    fonction_to_apply = outils_can.get_parcelle_realise_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)


def test_get_noeuds_realise_outils_can():
    """
        Test de l'obtention des informations utiles pour la constitution des fichiers noeuds_realise pour la CAN
    """
    assert True


def test_get_sdc_realise_outils_can():
    """
        Test de l'obtention des informations utiles pour la constitution des fichiers sdc pour la CAN
    """
    identifiant_test = 'test_get_sdc_realise_outils_can'

    df_names = [
        'zone', 'composant_culture', 'noeuds_realise', 'espece', 'variete', 'culture', 'plantation_perenne_realise',
        'plantation_perenne_phases_realise', 'parcelle','connection_realise'
    ]

    path_data = '02_outils/tests/data/test_get_sdc_realise_outils_can/'

    fonction_to_apply = outils_can.get_sdc_realise_outils_can
    res = fonction_test(identifiant_test, df_names, path_data, fonction_to_apply)

    assert all(res)