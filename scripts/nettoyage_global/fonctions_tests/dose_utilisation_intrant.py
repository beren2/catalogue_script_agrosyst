"""
    Fichier de test pour la dose de l'intrant 
    Permet de s'assurer que : 
        - la dose d'utilisation de l'intrant est inférieur à x fois la dose de référence. 
"""
import numpy as np
from scripts.utils import fonctions_utiles
import pandas as pd

def dose_utilisation_intrant(donnees, metadata_seuils, saisie):
    """
        Retourne une série binaire de taille n. 
        La ligne i de cette série contient 1 si le test est passé pour la ligne, 0 sinon.

                Paramètres:
                    donnees (df) : dataframe contenant les données d'intrants
                    metadata_seuils (df) : dataframe contenant les metadonnées sur les seuils 
                        du test

                Retourne:
                    code_test (Serie) : série binaire de taille n indiquant si le test est passé
    """
    # copie des données en local
    donnees_local = donnees.copy()


    multiple_dose_ref = float(metadata_seuils['multiple_dose_ref']['seuil'])

    df_utilisation_complet = fonctions_utiles.get_infos_all_utilisation_intrant(
        donnees_local.copy(), 
        saisie=saisie
    )
    
    index_same_unit = df_utilisation_complet.loc[(df_utilisation_complet['unite'] == df_utilisation_complet['unit_dose_ref_maa'])].index

    # on obtient le passage du test pour tous ceux remontés dans df_utilisation_complet
    df_utilisation_complet.loc[index_same_unit,'code_test'] = (
        (df_utilisation_complet.loc[index_same_unit, 'dose'] < multiple_dose_ref*df_utilisation_complet.loc[index_same_unit, 'dose_ref_maa']) 
    ).astype('int')

    left = donnees_local
    right = df_utilisation_complet[['id', 'code_test']]
    donnees_local = pd.merge(left, right, on = 'id', how='left')

    # les utilisations d'intrants qui n'ont pas de dose de références remontées passent le test par défaut.
    donnees_local['code_test'] = donnees_local['code_test'].fillna(1)

    return donnees_local['code_test']