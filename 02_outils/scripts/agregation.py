# pylint: disable-all

import pandas as pd

def get_aggreged_from_utilisation_intrant_synthetise(
    donnees
):
    """
        Permet d'obtenir toutes les agregations des échelles supérieures des utilisation d'intrants en synthétisé
    """
    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise']
    df_action_synthetise = donnees['action_synthetise']
    df_intervention_synthetise = donnees['intervention_synthetise']
    df_connection_synthetise = donnees['connection_synthetise']
    df_noeud_synthetise = donnees['noeuds_synthetise']
    df_plantation_perenne_phases_synthetise = donnees['plantation_perenne_phases_synthetise']
    df_plantation_perenne_synthetise = donnees['plantation_perenne_synthetise']
    df_synthetise = donnees['synthetise']
    df_sdc = donnees['sdc']
    df_dispositif = donnees['dispositif']

    # obtention de l'action sur laquelle a lieu l'utilisation d'intrant en synthétisé
    left = df_utilisation_intrant_synthetise[['id', 'action_synthetise_id']]
    right = df_action_synthetise[['id', 'intervention_synthetise_id']].rename(columns={'id' : 'action_synthetise_id'})
    merge = pd.merge(left, right, on = 'action_synthetise_id', how='left')

    # obtention de l'intervention sur laquelle a lieu l'action
    left = merge
    right = df_intervention_synthetise[['id', 'connection_synthetise_id', 'plantation_perenne_phases_synthetise_id']].rename(columns={'id' : 'intervention_synthetise_id'})
    merge = pd.merge(left, right, on = 'intervention_synthetise_id', how='left')

    merge_perenne = merge.loc[merge['connection_synthetise_id'].isna()]
    merge_assolee = merge.loc[merge['plantation_perenne_phases_synthetise_id'].isna()]
    #----------#
    # ASSOLÉES #
    #----------#
    # obtention de la connection sur laquelle a lieu l'action
    left = merge_assolee
    right = df_connection_synthetise[['id', 'cible_noeuds_synthetise_id']].rename(columns={'id' : 'connection_synthetise_id'})
    merge_assolee = pd.merge(left, right, on = 'connection_synthetise_id', how='left')

    # obtention du noeud et de la culture sur lequel a lieu l'action
    left = merge_assolee
    right = df_noeud_synthetise[['id', 'synthetise_id', 'culture_code']].rename(columns={'id' : 'cible_noeuds_synthetise_id'})
    merge_assolee = pd.merge(left, right, on = 'cible_noeuds_synthetise_id', how='left')

    #----------#
    # PERENNES #
    #----------#
    # obtention de la phase en synthétisé sur laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_phases_synthetise[['id', 'plantation_perenne_synthetise_id']].rename(columns={'id' : 'plantation_perenne_phases_synthetise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_synthetise_id', how='left')

    # obtention de la plantation perenne et du culture_code sur lequel a laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_synthetise[['id', 'synthetise_id', 'culture_code']].rename(columns={'id' : 'plantation_perenne_synthetise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_synthetise_id', how='left')

    merge = pd.concat([merge_assolee, merge_perenne], axis=0)


    # obtention du synthétisé sur lequel a lieu l'action --> attention, dans "campagnes", on a les campagnes concernées par le synthétisé, mais pas la campagne du sdc de référence !
    left = merge
    right = df_synthetise[['id', 'sdc_id']].rename(columns={'id' : 'synthetise_id'})
    merge = pd.merge(left, right, on = 'synthetise_id', how='left')

    # obtention du système de culture sur laquelle a lieu l'action --> cette fois on a une seule campagne de référence
    left = merge
    right = df_sdc[['id', 'campagne', 'dispositif_id']].rename(columns={'id' :'sdc_id', 'campagne' : 'sdc_campagne'})
    merge = pd.merge(left, right, on = 'sdc_id', how='left')

    # obtention du dispositif sur lequel a lieu l'action 
    left = merge 
    right = df_dispositif[['id', 'domaine_id']].rename(columns={'id' : 'dispositif_id'})
    merge = pd.merge(left, right, on = 'dispositif_id', how='left')

    merge = merge.set_index('id')
    return merge


def get_aggreged_from_utilisation_intrant_realise(
    donnees
):  
    """
        Permet d'obtenir toutes les agregations des échelles supérieures des utilisation d'intrants en réalisé
    """
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise']
    df_action_realise = donnees['action_realise']
    df_intervention_realise = donnees['intervention_realise']
    df_noeud_realise = donnees['noeuds_realise']
    df_plantation_perenne_phases_realise = donnees['plantation_perenne_phases_realise']
    df_plantation_perenne_realise = donnees['plantation_perenne_realise']
    df_zone = donnees['zone']
    df_parcelle = donnees['parcelle']
    df_sdc = donnees['sdc']
    df_dispositif = donnees['dispositif']

    # obtention de l'action sur laquelle a lieu l'utilisation d'intrant en synthétisé
    left = df_utilisation_intrant_realise[['id', 'action_realise_id']]
    right = df_action_realise[['id', 'intervention_realise_id']].rename(columns={'id' : 'action_realise_id'})
    merge = pd.merge(left, right, on = 'action_realise_id', how='left')

    # obtention de l'intervention sur laquelle a lieu l'action
    left = merge
    right = df_intervention_realise[['id', 'noeuds_realise_id', 'plantation_perenne_phases_realise_id']].rename(columns={'id' : 'intervention_realise_id'})
    merge = pd.merge(left, right, on = 'intervention_realise_id', how='left')

    merge_perenne = merge.loc[merge['noeuds_realise_id'].isna()]
    merge_assolee = merge.loc[merge['plantation_perenne_phases_realise_id'].isna()]
    #----------#
    # ASSOLÉES #
    #----------#

    # obtention du noeud sur lequel a laquelle a lieu l'action
    left = merge_assolee
    right = df_noeud_realise[['id', 'zone_id', 'culture_id']].rename(columns={'id' : 'noeuds_realise_id'})
    merge_assolee = pd.merge(left, right, on = 'noeuds_realise_id', how='left')

    #----------#
    # PERENNES #
    #----------#
    # obtention de la phase en synthétisé sur laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_phases_realise[['id', 'plantation_perenne_realise_id']].rename(columns={'id' : 'plantation_perenne_phases_realise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_realise_id', how='left')

    # obtention de la plantation sur perenne sur lequel a laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_realise[['id', 'zone_id']].rename(columns={'id' : 'plantation_perenne_realise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_realise_id', how='left')

    merge = pd.concat([merge_assolee, merge_perenne], axis=0)


    # obtention de la zone sur laquelle a lieu l'action
    left = merge
    right = df_zone[['id', 'parcelle_id']].rename(columns={'id' : 'zone_id'})
    merge = pd.merge(left, right, on = 'zone_id', how='left')

    # obtention de la parcelle sur laquelle a lieu l'action
    left = merge
    right = df_parcelle[['id', 'sdc_id']].rename(columns={'id' : 'parcelle_id'})
    merge = pd.merge(left, right, on = 'parcelle_id', how='left')

    # obtention du système de culture sur laquelle a lieu l'action --> cette fois on a une seule campagne de référence
    left = merge
    right = df_sdc[['id', 'campagne', 'dispositif_id']].rename(columns={'id' :'sdc_id', 'campagne' : 'sdc_campagne'})
    merge = pd.merge(left, right, on = 'sdc_id', how='left')

    # obtention du dispositif sur lequel a lieu l'action 
    left = merge 
    right = df_dispositif[['id', 'domaine_id']].rename(columns={'id' : 'dispositif_id'})
    merge = pd.merge(left, right, on = 'dispositif_id', how='left')

    merge = merge.set_index('id')

    return merge


def get_leaking_aggreged_from_action_realise(
    aggreged_utilisation_intrant_realise, donnees
):
    """ 
        Permet d'obtenir toutes les actions qui ne sont pas déjà dans les utilisations d'intrants agrégées.
    """
    df_action_realise = donnees['action_realise']
    df_intervention_realise = donnees['intervention_realise']
    df_noeud_realise = donnees['noeuds_realise']
    df_plantation_perenne_phases_realise = donnees['plantation_perenne_phases_realise']
    df_plantation_perenne_realise = donnees['plantation_perenne_realise']
    df_zone = donnees['zone']
    df_parcelle = donnees['parcelle']
    df_sdc = donnees['sdc']
    df_dispositif = donnees['dispositif']
    
    # sélection uniquement de celles qui ne sont pas déjà dans l'échelle agrégée depuis intrant.
    merge = df_action_realise.loc[~df_action_realise['id'].isin(list(aggreged_utilisation_intrant_realise['action_realise_id']))]

    # obtention de l'intervention sur laquelle a lieu l'action
    merge = merge[['id', 'intervention_realise_id']]

    # obtention de l'intervention sur laquelle a lieu l'action
    left = merge
    right = df_intervention_realise[['id', 'noeuds_realise_id', 'plantation_perenne_phases_realise_id']].rename(columns={'id' : 'intervention_realise_id'})
    merge = pd.merge(left, right, on = 'intervention_realise_id', how='left')

    merge_perenne = merge.loc[merge['noeuds_realise_id'].isna()]
    merge_assolee = merge.loc[merge['plantation_perenne_phases_realise_id'].isna()]
    #----------#
    # ASSOLÉES #
    #----------#

    # obtention du noeud sur lequel a laquelle a lieu l'action
    left = merge_assolee
    right = df_noeud_realise[['id', 'zone_id', 'culture_id']].rename(columns={'id' : 'noeuds_realise_id'})
    merge_assolee = pd.merge(left, right, on = 'noeuds_realise_id', how='left')

    #----------#
    # PERENNES #
    #----------#
    # obtention de la phase en synthétisé sur laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_phases_realise[['id', 'plantation_perenne_realise_id']].rename(columns={'id' : 'plantation_perenne_phases_realise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_realise_id', how='left')

    # obtention de la plantation sur perenne sur lequel a laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_realise[['id', 'zone_id']].rename(columns={'id' : 'plantation_perenne_realise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_realise_id', how='left')

    merge = pd.concat([merge_assolee, merge_perenne], axis=0)


    # obtention de la zone sur laquelle a lieu l'action
    left = merge
    right = df_zone[['id', 'parcelle_id']].rename(columns={'id' : 'zone_id'})
    merge = pd.merge(left, right, on = 'zone_id', how='left')

    # obtention de la parcelle sur laquelle a lieu l'action
    left = merge
    right = df_parcelle[['id', 'sdc_id']].rename(columns={'id' : 'parcelle_id'})
    merge = pd.merge(left, right, on = 'parcelle_id', how='left')

    # obtention du système de culture sur laquelle a lieu l'action --> cette fois on a une seule campagne de référence
    left = merge
    right = df_sdc[['id', 'campagne', 'dispositif_id']].rename(columns={'id' :'sdc_id', 'campagne' : 'sdc_campagne'})
    merge = pd.merge(left, right, on = 'sdc_id', how='left')

    # obtention du dispositif sur lequel a lieu l'action 
    left = merge 
    right = df_dispositif[['id', 'domaine_id']].rename(columns={'id' : 'dispositif_id'})
    merge = pd.merge(left, right, on = 'dispositif_id', how='left')

    merge = merge.set_index('id')

    return merge



def get_leaking_aggreged_from_intervention_realise(
    aggreged_utilisation_intrant_realise, donnees
):
    """ 
        Permet d'obtenir toutes les interventions qui ne sont pas déjà dans les utilisations d'intrants agrégées.
    """
    df_intervention_realise = donnees['intervention_realise']
    df_noeud_realise = donnees['noeuds_realise']
    df_plantation_perenne_phases_realise = donnees['plantation_perenne_phases_realise']
    df_plantation_perenne_realise = donnees['plantation_perenne_realise']
    df_zone = donnees['zone']
    df_parcelle = donnees['parcelle']
    df_sdc = donnees['sdc']
    df_dispositif = donnees['dispositif']
    # sélection uniquement de celles qui ne sont pas déjà dans l'échelle agrégée depuis intrant.
    merge = df_intervention_realise.loc[~df_intervention_realise['id'].isin(list(aggreged_utilisation_intrant_realise['intervention_realise_id']))]

    # obtention de l'intervention sur laquelle a lieu l'action
    merge = merge[['id', 'noeuds_realise_id', 'plantation_perenne_phases_realise_id']]

    merge_perenne = merge.loc[merge['noeuds_realise_id'].isna()]
    merge_assolee = merge.loc[merge['plantation_perenne_phases_realise_id'].isna()]
    #----------#
    # ASSOLÉES #
    #----------#

    # obtention du noeud sur lequel a laquelle a lieu l'action
    left = merge_assolee
    right = df_noeud_realise[['id', 'zone_id', 'culture_id']].rename(columns={'id' : 'noeuds_realise_id'})
    merge_assolee = pd.merge(left, right, on = 'noeuds_realise_id', how='left')

    #----------#
    # PERENNES #
    #----------#
    # obtention de la phase en synthétisé sur laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_phases_realise[['id', 'plantation_perenne_realise_id']].rename(columns={'id' : 'plantation_perenne_phases_realise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_realise_id', how='left')

    # obtention de la plantation sur perenne sur lequel a laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_realise[['id', 'zone_id']].rename(columns={'id' : 'plantation_perenne_realise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_realise_id', how='left')

    merge = pd.concat([merge_assolee, merge_perenne], axis=0)


    # obtention de la zone sur laquelle a lieu l'action
    left = merge
    right = df_zone[['id', 'parcelle_id']].rename(columns={'id' : 'zone_id'})
    merge = pd.merge(left, right, on = 'zone_id', how='left')

    # obtention de la parcelle sur laquelle a lieu l'action
    left = merge
    right = df_parcelle[['id', 'sdc_id']].rename(columns={'id' : 'parcelle_id'})
    merge = pd.merge(left, right, on = 'parcelle_id', how='left')

    # obtention du système de culture sur laquelle a lieu l'action --> cette fois on a une seule campagne de référence
    left = merge
    right = df_sdc[['id', 'campagne', 'dispositif_id']].rename(columns={'id' :'sdc_id', 'campagne' : 'sdc_campagne'})
    merge = pd.merge(left, right, on = 'sdc_id', how='left')

    # obtention du dispositif sur lequel a lieu l'action 
    left = merge 
    right = df_dispositif[['id', 'domaine_id']].rename(columns={'id' : 'dispositif_id'})
    merge = pd.merge(left, right, on = 'dispositif_id', how='left')

    merge = merge.set_index('id')

    return merge


def get_leaking_aggreged_from_action_synthetise(
    aggreged_utilisation_intrant_synthetise, donnees
):
    """
        Permet d'obtenir toutes les actions qui ne sont pas déjà dans les utilisations d'intrants agrégées en synthétisé.
    """
    df_action_synthetise = donnees['action_synthetise']
    df_intervention_synthetise = donnees['intervention_synthetise']
    df_connection_synthetise = donnees['connection_synthetise']
    df_noeud_synthetise = donnees['noeuds_synthetise']
    df_plantation_perenne_phases_synthetise = donnees['plantation_perenne_phases_synthetise']
    df_plantation_perenne_synthetise = donnees['plantation_perenne_synthetise']
    df_synthetise = donnees['synthetise']
    df_sdc = donnees['sdc']
    df_dispositif = donnees['dispositif']
    # sélection uniquement de celles qui ne sont pas déjà dans l'échelle agrégée depuis intrant.
    merge = df_action_synthetise.loc[~df_action_synthetise['id'].isin(list(aggreged_utilisation_intrant_synthetise['action_synthetise_id']))]

    # obtention de l'intervention sur laquelle a lieu l'action
    merge = merge[['id', 'intervention_synthetise_id']]

    # obtention de l'intervention sur laquelle a lieu l'action
    left = merge
    right = df_intervention_synthetise[['id', 'connection_synthetise_id', 'plantation_perenne_phases_synthetise_id']].rename(columns={'id' : 'intervention_synthetise_id'})
    merge = pd.merge(left, right, on = 'intervention_synthetise_id', how='left')

    merge_perenne = merge.loc[merge['connection_synthetise_id'].isna()]
    merge_assolee = merge.loc[merge['plantation_perenne_phases_synthetise_id'].isna()]
    #----------#
    # ASSOLÉES #
    #----------#
    # obtention de la connection sur laquelle a lieu l'action
    left = merge_assolee
    right = df_connection_synthetise[['id', 'cible_noeuds_synthetise_id']].rename(columns={'id' : 'connection_synthetise_id'})
    merge_assolee = pd.merge(left, right, on = 'connection_synthetise_id', how='left')

    # obtention du noeud sur lequel a laquelle a lieu l'action
    left = merge_assolee
    right = df_noeud_synthetise[['id', 'synthetise_id']].rename(columns={'id' : 'cible_noeuds_synthetise_id'})
    merge_assolee = pd.merge(left, right, on = 'cible_noeuds_synthetise_id', how='left')

    #----------#
    # PERENNES #
    #----------#
    # obtention de la phase en synthétisé sur laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_phases_synthetise[['id', 'plantation_perenne_synthetise_id']].rename(columns={'id' : 'plantation_perenne_phases_synthetise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_synthetise_id', how='left')

    # obtention de la plantation sur perenne sur lequel a laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_synthetise[['id', 'synthetise_id']].rename(columns={'id' : 'plantation_perenne_synthetise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_synthetise_id', how='left')

    merge = pd.concat([merge_assolee, merge_perenne], axis=0)


    # obtention du synthétisé sur lequel a lieu l'action --> attention, dans "campagnes", on a les campagnes concernées par le synthétisé, mais pas la campagne du sdc de référence !
    left = merge
    right = df_synthetise[['id', 'sdc_id']].rename(columns={'id' : 'synthetise_id'})
    merge = pd.merge(left, right, on = 'synthetise_id', how='left')

    # obtention du système de culture sur laquelle a lieu l'action --> cette fois on a une seule campagne de référence
    left = merge
    right = df_sdc[['id', 'campagne', 'dispositif_id']].rename(columns={'id' :'sdc_id', 'campagne' : 'sdc_campagne'})
    merge = pd.merge(left, right, on = 'sdc_id', how='left')

    # obtention du dispositif sur lequel a lieu l'action 
    left = merge 
    right = df_dispositif[['id', 'domaine_id']].rename(columns={'id' : 'dispositif_id'})
    merge = pd.merge(left, right, on = 'dispositif_id', how='left')

    merge = merge.set_index('id')
    return merge


def get_leaking_aggreged_from_intervention_synthetise(
    aggreged_utilisation_intrant_realise, donnees
):
    """
        Permet d'obtenir toutes les actions qui ne sont pas déjà dans les interventions agrégées en synthétisé.
    """
    df_intervention_synthetise = donnees['intervention_synthetise']
    df_connection_synthetise = donnees['connection_synthetise']
    df_noeud_synthetise = donnees['noeuds_synthetise']
    df_plantation_perenne_phases_synthetise = donnees['plantation_perenne_phases_synthetise']
    df_plantation_perenne_synthetise = donnees['plantation_perenne_synthetise']
    df_synthetise = donnees['synthetise']
    df_sdc = donnees['sdc']
    df_dispositif = donnees['dispositif']
    merge = df_intervention_synthetise.loc[~df_intervention_synthetise['id'].isin(list(aggreged_utilisation_intrant_realise['intervention_synthetise_id']))]

    # obtention de l'intervention sur laquelle a lieu l'action
    merge = merge[['id', 'connection_synthetise_id', 'plantation_perenne_phases_synthetise_id']]

    merge_perenne = merge.loc[merge['connection_synthetise_id'].isna()]
    merge_assolee = merge.loc[merge['plantation_perenne_phases_synthetise_id'].isna()]
    #----------#
    # ASSOLÉES #
    #----------#
    # obtention de la connection sur laquelle a lieu l'action
    left = merge_assolee
    right = df_connection_synthetise[['id', 'cible_noeuds_synthetise_id']].rename(columns={'id' : 'connection_synthetise_id'})
    merge_assolee = pd.merge(left, right, on = 'connection_synthetise_id', how='left')

    # obtention du noeud sur lequel a laquelle a lieu l'action
    left = merge_assolee
    right = df_noeud_synthetise[['id', 'synthetise_id']].rename(columns={'id' : 'cible_noeuds_synthetise_id'})
    merge_assolee = pd.merge(left, right, on = 'cible_noeuds_synthetise_id', how='left')

    #----------#
    # PERENNES #
    #----------#
    # obtention de la phase en synthétisé sur laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_phases_synthetise[['id', 'plantation_perenne_synthetise_id']].rename(columns={'id' : 'plantation_perenne_phases_synthetise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_synthetise_id', how='left')

    # obtention de la plantation sur perenne sur lequel a laquelle a lieu l'action
    left = merge_perenne
    right = df_plantation_perenne_synthetise[['id', 'synthetise_id']].rename(columns={'id' : 'plantation_perenne_synthetise_id'})
    merge_perenne = pd.merge(left, right, on = 'plantation_perenne_synthetise_id', how='left')

    merge = pd.concat([merge_assolee, merge_perenne], axis=0)


    # obtention du synthétisé sur lequel a lieu l'action --> attention, dans "campagnes", on a les campagnes concernées par le synthétisé, mais pas la campagne du sdc de référence !
    left = merge
    right = df_synthetise[['id', 'sdc_id']].rename(columns={'id' : 'synthetise_id'})
    merge = pd.merge(left, right, on = 'synthetise_id', how='left')

    # obtention du système de culture sur laquelle a lieu l'action --> cette fois on a une seule campagne de référence
    left = merge
    right = df_sdc[['id', 'campagne', 'dispositif_id']].rename(columns={'id' :'sdc_id', 'campagne' : 'sdc_campagne'})
    merge = pd.merge(left, right, on = 'sdc_id', how='left')

    # obtention du dispositif sur lequel a lieu l'action 
    left = merge 
    right = df_dispositif[['id', 'domaine_id']].rename(columns={'id' : 'dispositif_id'})
    merge = pd.merge(left, right, on = 'dispositif_id', how='left')

    merge = merge.set_index('id')
    return merge
