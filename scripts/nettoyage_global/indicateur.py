"""
	Regroupe les fonctions qui consistent en des calculs d'indicateurs 
"""
import pandas as pd
import numpy as np
import scripts.utils.fonctions_utiles as fonctions_utiles


def indicateur_utilisation_intrant(donnees):
    """ 
        fonction permettant d'obtenir pour chaque utilsation d'intrants, la dose de référence utilisée
    """
    df_utilisation_intrant_realise = fonctions_utiles.get_infos_all_utilisation_intrant(donnees, saisie = 'realise')
    df_utilisation_intrant_synthetise = fonctions_utiles.get_infos_all_utilisation_intrant(donnees, saisie = 'synthetise')
    
    res = pd.concat([df_utilisation_intrant_realise, df_utilisation_intrant_synthetise], axis=0)

    return res[['id', 'dose_ref_maa', 'unit_dose_ref_maa', 'code_culture_maa', 'code_groupe_cible_maa', 'code_traitement_maa']].set_index('id')
