"""
    Fichier de test pour les interventions
    Permet de s'assurer que : 
        - la date de semis est conforme :
            - si on sème une espèce particulière, on vérifie que l'espèce peut être semée à cette époque dans le référentiel.
"""
import pandas as pd

def date_semis(donnees, metadata_seuils, donnees_aux=None):
    """
        Retourne une série binaire de taille n. 
        La ligne i de cette série contient 1 si le test est passé pour la ligne, 0 sinon.

                Paramètres:
                    donnees (df) : dataframe contenant les données d'interventions
                    donnees_aux (dict de df) : dictionnaire de dataframe contenant les données auxiliaires utilisées pour le test.
                    metadata_seuils (df) : dataframe contenant les metadonnées sur les seuils 
                        du test

                Retourne:
                    code_test (Serie) : série binaire de taille n indiquant si le test est passé
    """




    date_debut = pd.to_datetime(date_debut, format="%Y-%m-%d", errors='coerce')
    date_fin = pd.to_datetime(date_fin, format="%Y-%m-%d", errors='coerce')
    donnees_local['duree'] = date_fin - date_debut

    # obtention dans les métadonnées du seuil approprié
    seuil_duree_min = metadata_seuils['duree_intervention_min']['seuil']

    # filtration des interventions qui durent au moins seuil_duree_min
    code_test_duree_min = (donnees_local['duree'].dt.days >= seuil_duree_min).astype(int)
    donnees_local['code_test'] = code_test_duree_min

    return donnees_local['code_test']
    