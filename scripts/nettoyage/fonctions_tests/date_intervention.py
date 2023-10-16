"""
    Fichier de test pour les dates des interventions
    Permet de s'assurer que : 
        - la date de fin est bien après la date de début
"""
import pandas as pd

def date_intervention(donnees, metadata_seuils):
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

    # durée de l'intervention
    date_debut = donnees['date_debut']
    date_fin = donnees['date_fin']
    date_debut = pd.to_datetime(date_debut, format="%Y-%m-%d", errors='coerce')
    date_fin = pd.to_datetime(date_fin, format="%Y-%m-%d", errors='coerce')
    donnees['duree'] = date_fin - date_debut

    # obtention dans les métadonnées du seuil approprié
    seuil_duree_min = metadata_seuils['duree_intervention_min']['seuil']

    # filtration des interventions qui durent au moins seuil_duree_min
    code_test_duree_min = (donnees['duree'].dt.days > seuil_duree_min).astype(int)
    donnees.loc[donnees.index, 'code_test'] = code_test_duree_min

    return donnees['code_test']
    