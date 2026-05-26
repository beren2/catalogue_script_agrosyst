"""
	Regroupe les fonctions permettant de générer les outils utils lors de la génération du magasin "DiRoDur".
"""
from datetime import datetime
import pandas as pd
import numpy as np


def filtered_entities_sdc_level(donnees):
    """
    Cette fonction permet de filtrer les entités que l'on veut présente dans le dataframe principale de la table SDC du magasin DIRODUR.
    Globalement il y a en premier lieu un filtre sur les entités avec intervention (par construction),
      puis des filtre sur la filiere GCPE ; 
      sur une entité unique par sdc ; 
      sur les années trop veilles (ne devrait pas être présente) ou trop récentes (pas encore assez consolidées) ; 
      et enfin sur les alertes (petite expection si les cultures sont des prairies temporaires plus de 50% du temps).

    Entree: 
        'synthetise',
        'sdc',
        'typologie_assol_can_realise',
        'typologie_can_rotation_synthetise',
        'entite_unique_par_sdc_nettoyage',
        'sdc_realise_performance',
        'synthetise_synthetise_performance',
        'intervention_synthetise_agrege',
        'intervention_realise_agrege'
        ==> Utilise les outils indicateurs, nettoyages et agregations !

    Retourne:
        2 df << sdc_realise, synthetises = filtered_entities_sdc_level(donnees) >>
        avec une colonne d'entité : sdc_id ou synthetise_id
        et la colonne "in_dirodur", un booléen : True -> à garder dans dirodur
    """
    lst_alerte_col = ['alerte_ferti_n_tot', 'alerte_ift_cible_non_mil_chim_tot_hts',
        'alerte_ift_cible_non_mil_f', 'alerte_ift_cible_non_mil_h',
        'alerte_ift_cible_non_mil_i', 'alerte_ift_cible_non_mil_biocontrole',
        'alerte_co_irrigation_std_mil', 'alerte_msn_std_mil_avec_autoconso',
        'alerte_nombre_interventions_phyto', 'alerte_pb_std_mil_avec_autoconso',
        'alerte_rendement', 'alertes_charges', 'alerte_cm_std_mil',
        'alerte_co_semis_std_mil', 'alerte_tps_travail_total']

    int_r = donnees['intervention_realise_agrege'][['id','sdc_id']]
    sdc_real = donnees['sdc_realise_performance'][['sdc_id']+lst_alerte_col]
    sdc = donnees['sdc'][['id','filiere','campagne']].rename(columns={'id':'sdc_id'})
    typo_re = donnees['typologie_assol_can_realise'][['sdc_id','typocan_assol_dvlp']]

    int_s = donnees['intervention_synthetise_agrege'][['id','synthetise_id','sdc_id']]
    sdc_synth = donnees['synthetise_synthetise_performance'][['synthetise_id']+lst_alerte_col]
    typo_sy = donnees['typologie_can_rotation_synthetise'][['synthetise_id','typocan_rotation']]

    synth = donnees['synthetise'][['id']].rename(columns={'id':'synthetise_id'}) # besoin que pour la fin
    unique_entity = donnees['entite_unique_par_sdc_nettoyage']

    # 0. Avant tout : Par le jeu des merge on ne garde que les synthé ou sdc qui ont des interventions !
    sdc_real = int_r.merge(sdc_real, on='sdc_id', how='left').merge(sdc, on='sdc_id', how='left').merge(typo_re, on='sdc_id', how='left')
    sdc_real = sdc_real.groupby('sdc_id').first().reset_index().drop(columns='id')

    sdc_synth = int_s.merge(sdc_synth, on='synthetise_id', how='left').merge(sdc, on='sdc_id', how='left').merge(typo_sy, on='synthetise_id', how='left')
    sdc_synth = sdc_synth.groupby('synthetise_id').first().reset_index().drop(columns='id')

    # 1. on filtre selon la filière GCPE
    sdc_real = sdc_real.loc[sdc_real['filiere'].isin(['POLYCULTURE_ELEVAGE','GRANDES_CULTURES'])]
    sdc_synth = sdc_synth.loc[sdc_synth['filiere'].isin(['POLYCULTURE_ELEVAGE','GRANDES_CULTURES'])]

    # 2. on filtre grace à l'outil d'entité unique par sdc
    # il regarde dans un sdc s'il y a plusieurs synthétisé et ou zone de réalisé et en choisi un seul
    lst_unqiue_entity_real = unique_entity.loc[unique_entity['entite_retenue']=='realise_retenu','sdc_id'].tolist()
    sdc_real = sdc_real.loc[sdc_real['sdc_id'].isin(lst_unqiue_entity_real)]

    lst_unqiue_entity_synth = unique_entity.loc[unique_entity['entite_retenue']!='realise_retenu','entite_retenue'].to_list()
    sdc_synth = sdc_synth.loc[sdc_synth['synthetise_id'].isin(lst_unqiue_entity_synth)]

    # 3. on va filtré l'année en cours pour le magasin car les données sont surement en cours de saisie ou en cours de consolidation par les IR. En gros au 1° avril on accorde l'ajout de l'année n-1
    # Définir les années limites (seuils strictes !)
    if datetime.now().month <= 3 :  annees_max = datetime.now().year - 1
    else :                          annees_max = datetime.now().year
    annees_trop_vieille = 2004 # des pz0 attendues jusqu'en 2005

    sdc_synth = sdc_synth.loc[((pd.to_numeric(sdc_synth['campagne'], errors='coerce')) > annees_trop_vieille) & 
                            ((pd.to_numeric(sdc_synth['campagne'], errors='coerce')) < annees_max)]
    sdc_real = sdc_real.loc[((pd.to_numeric(sdc_real['campagne'], errors='coerce')) > annees_trop_vieille) & 
                            ((pd.to_numeric(sdc_real['campagne'], errors='coerce')) < annees_max)]


    # 4. on filtre par alertes
    list_alerte_ok = ["Pas d'alerte", "Cette alerte n'existe pas dans cette filière", "Cette alerte n'existe pas encore dans cette filière"]

    def filtrer_alertes(df, lst_alerte_col, list_alerte_ok, name_culture_col):
        # Masque pour les colonnes d'alertes sauf 1
        autres_colonnes = [col for col in lst_alerte_col if col != 'alerte_cm_std_mil']
        mask_autres = df[autres_colonnes].apply(
            lambda x: x.isin(list_alerte_ok) | x.isna()
        ).all(axis=1)

        # Mask pour les alertes de CM lorsque la culture est majoritairement de la prairie
        mask_cm = (
            df['alerte_cm_std_mil'].isin(list_alerte_ok) |
            df['alerte_cm_std_mil'].isna() |
            ((df['alerte_cm_std_mil'].str.contains('<', na=False)) & (df[name_culture_col] == "prairie temporaire >= 50 % assolement"))
            )

        mask_final = mask_autres & mask_cm
        return df[mask_final]


    sdc_real = filtrer_alertes(sdc_real, lst_alerte_col, list_alerte_ok, 'typocan_assol_dvlp')
    sdc_synth = filtrer_alertes(sdc_synth, lst_alerte_col, list_alerte_ok, 'typocan_rotation')

    # On prend tout les sdc, et tout les synthetise, on leur tag s'ils appartiennent ou non à dirodur
    final_real = sdc[['sdc_id']]
    final_real['in_dirodur'] = np.where(final_real['sdc_id'].isin(sdc_real['sdc_id']), True, False)

    final_synth = synth[['synthetise_id']]
    final_synth['in_dirodur'] = np.where(final_synth['synthetise_id'].isin(sdc_synth['synthetise_id']), True, False)

    # On exporte la liste pour les realise et la liste pour les synthe
    return final_real, final_synth