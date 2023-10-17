"""
    Fichier de test pour le débit de chantier_intervention. 
    Permet de s'assurer que : 
        - le débit de chantier est inférieur à des seuils minimaux
        - le débit de chantier est supérieur à des seuils maximaux
"""
import numpy as np

def debit_chantier_intervention(donnees, metadata_seuils):
    """
        Retourne une série binaire de taille n. 
        La ligne i de cette série contient 1 si le test est passé pour la ligne, 0 sinon.

                Paramètres:
                    donnees (df) : dataframe contenant les données d'interventions
                    metadata_seuils (df) : dataframe contenant les metadonnées sur les seuils 
                        du test

                Retourne:
                    code_test (Serie) : série binaire de taille n indiquant si le test est passé
    """
    # copie des données en local
    donnees_local = donnees.copy()

    # liste de toutes les unités disponibles
    list_debit_de_chantier_unite = ['HA_H', 'H_HA', 'VOY_H', 'BAL_H', 'T_H']
    donnees_local['code_test'] = 0 # par défaut, toutes les données passent le test

    for debit_de_chantier_unite in list_debit_de_chantier_unite:
        # selection des lignes dans la bonne unité
        donnees_courant = donnees_local.loc[
            donnees_local['debit_de_chantier_unite'] == debit_de_chantier_unite
        ]

        # obtention dans les métadonnées du seuil approprié pour l'unité
        seuil_courant_max = metadata_seuils['debit_chantier_max_'+debit_de_chantier_unite]['seuil']
        seuil_courant_min = metadata_seuils['debit_chantier_min_'+debit_de_chantier_unite]['seuil']

        # création des codes tests max en conséquence
        code_test_max = (donnees_courant['debit_de_chantier'] <= seuil_courant_max).astype(int)
        # création des codes tests min en conséquence
        code_test_min = (donnees_courant['debit_de_chantier'] > seuil_courant_min).astype(int)

        # si la ligne échoue à l'un des deux tests, on garde échec (0)
        donnees_local.loc[donnees_courant.index, 'code_test'] = np.minimum(code_test_min, code_test_max)

    return donnees_local['code_test']
    