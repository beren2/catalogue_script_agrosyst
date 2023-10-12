"""
La fonction filtration_intervention permet d'obtenir les interventions 
cohérentes selon plusieurs critères : 
- date de fin - date de début < duree_max_intervention
- nombre de passages < nombre_max_passages
"""
import pandas as pd

def filtration_intervention(data, duree_max_intervention = 5, nombre_max_passages = 10):
    """"
        data : 
            dictionnaire avec au moins 3 clés : ["intervention_realise", "intervention_synthetise"]
            data['intervention_realise']    : 
                df de 3 colonnes ["date_debut", "date_fin", "nombre_de_passage"]
            data['intervention_synthetise'] : 
                df de 3 colonnes ["date_debut", "date_fin", "nombre_de_passage"]
    """
    df_intervention_realise = data['intervention_realise']

    # DURÉES D'INTERVENTION
    # récupération des dates de débuts et de fin de toutes les interventions
    date_debut = df_intervention_realise['date_debut']
    date_fin = df_intervention_realise['date_fin']
    date_debut = pd.to_datetime(date_debut, format="%Y-%m-%d", errors='coerce')
    date_fin = pd.to_datetime(date_fin, format="%Y-%m-%d", errors='coerce')
    # ajout dans le dataframe de la duree de l'intervention
    duree_intervention = date_fin - date_debut
    # filtration des interventions < 10
    df_intervention_realise = df_intervention_realise.loc[
        duree_intervention.dt.days < duree_max_intervention
    ]
    # filtration des interventions qui durent au moins 0 jours
    df_intervention_realise = df_intervention_realise.loc[
        duree_intervention.dt.days >= 0
    ]


    # NOMBRE DE PASSAGES
    # récupération des dates de débuts et de fin de toutes les interventions
    df_intervention_realise = df_intervention_realise.loc[
        df_intervention_realise['nombre_de_passage'] < nombre_max_passages
    ]


    filtered_data = {
        'intervention_realise' : df_intervention_realise
    }

    return filtered_data
            