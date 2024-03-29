"""
    Fichier de test pour les dates des interventions
    Permet de s'assurer que : 
        - la date de fin est bien après la date de début
"""
import pandas as pd

def date_intervention(donnees, metadata_seuils, donnees_aux=None):
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
    df_intervention = donnees['intervention_realise'].copy()

    print(donnees_aux is None)

    # durée de l'intervention
    date_debut = df_intervention['date_debut']
    date_fin = df_intervention['date_fin']
    date_debut = pd.to_datetime(date_debut, format="%Y-%m-%d", errors='coerce')
    date_fin = pd.to_datetime(date_fin, format="%Y-%m-%d", errors='coerce')
    df_intervention['duree'] = date_fin - date_debut

    # obtention dans les métadonnées du seuil approprié
    seuil_duree_min = metadata_seuils['duree_intervention_min']['seuil']

    # filtration des interventions qui durent au moins seuil_duree_min
    code_test_duree_min = (df_intervention['duree'].dt.days >= seuil_duree_min).astype(int)
    df_intervention['code_test'] = code_test_duree_min

    return df_intervention['code_test']
    