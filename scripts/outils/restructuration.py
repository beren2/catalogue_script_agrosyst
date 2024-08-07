"""
	Regroupe les fonctions qui constituent en des restructuration des fichiers initiaux afin de faciliter leur utilisation
"""
import pandas as pd

def restructuration_noeuds_synthetise(donnees):
    """ 
        fonction permettant d'obtenir pour chaque noeuds_synthetise, le bon culture_id plutôt que le culture_code
    """
    donnees = donnees.copy()
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')

    # obtention de la campagne pour le noeuds synthétisé
    left = donnees['noeuds_synthetise'][['id', 'culture_code', 'synthetise_id']]
    right = donnees['synthetise'][['sdc_id']]
    merge = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    left = merge
    right = donnees['sdc'][['campagne']]
    donnees['noeuds_synthetise_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    # obtention de la campagne pour la cutlure
    left = donnees['culture'].set_index('id')
    right = donnees['domaine'].set_index('id')[['campagne']]
    donnees['culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['noeuds_synthetise_extanded']
    right = donnees['culture_extanded'].reset_index()[['id', 'code', 'campagne']].rename(columns={'id' : 'culture_id'})
    donnees['noeuds_synthetise_restructure'] = pd.merge(left, right, left_on=['culture_code', 'campagne'], right_on=['code', 'campagne'])

    return donnees['noeuds_synthetise_restructure'].set_index('id')[['culture_id']]


def restructuration_connection_synthetise(donnees):
    """
        fonction permettant d'obtenir, pour chaque connection_synthetise, un culture_intermediaire_id plutôt qu'un culture_intermediaire_code
    """
    donnees = donnees.copy()
    donnees['noeuds_synthetise'] = donnees['noeuds_synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    # obtention de la campagne pour la connexion en synthétisé
    left = donnees['connection_synthetise'][['id', 'cible_noeuds_synthetise_id', 'culture_intermediaire_code']]
    right = donnees['noeuds_synthetise'][['culture_code', 'synthetise_id']].rename(columns={'id' : 'noeuds_synthetise_id'})
    merge = pd.merge(left, right, left_on='cible_noeuds_synthetise_id', right_index=True, how='left').set_index('id')

    left = merge
    right = donnees['synthetise'][['sdc_id']]
    merge = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    left = merge
    right = donnees['sdc'][['campagne']]
    donnees['connection_synthetise_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')[['culture_intermediaire_code', 'campagne']].dropna()

    # obtention de la campagne pour la culture
    left = donnees['culture'].set_index('id')
    right = donnees['domaine'].set_index('id')[['campagne']]
    donnees['culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['connection_synthetise_extanded'].reset_index()
    right = donnees['culture_extanded'].reset_index()[['id', 'code', 'campagne']].rename(columns={'id' : 'culture_intermediaire_id'})
    donnees['connection_synthetise_restructure'] = pd.merge(left, right, left_on=['culture_intermediaire_code', 'campagne'], right_on=['code', 'campagne'])

    return donnees['connection_synthetise_restructure'].set_index('id')[['culture_intermediaire_id']]


def restructuration_plantation_perenne_synthetise(donnees):
    """
        fonction permettant d'obtenir, pour chaque plantation perenne en synthétisé
        un culture_id plutôt qu'un culture_code
    """
    donnees = donnees.copy()
    donnees['plantation_perenne_synthetise'] = donnees['plantation_perenne_synthetise'].set_index('id')
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')
    donnees['dispositif'] = donnees['dispositif'].set_index('id')
    donnees['domaine'] = donnees['domaine'].set_index('id')
    donnees['culture'] = donnees['culture'].set_index('id')

    left = donnees['plantation_perenne_synthetise'][['synthetise_id', 'culture_code']]
    right = donnees['synthetise'][['sdc_id']]
    donnees['plantation_perenne_synthetise_extanded'] = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    left = donnees['plantation_perenne_synthetise_extanded']
    right = donnees['sdc']['dispositif_id']
    donnees['plantation_perenne_synthetise_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    left = donnees['plantation_perenne_synthetise_extanded']
    right = donnees['dispositif']['domaine_id']
    donnees['plantation_perenne_synthetise_extanded'] = pd.merge(left, right, left_on='dispositif_id', right_index=True, how='left')

    left = donnees['plantation_perenne_synthetise_extanded']
    right = donnees['domaine']['campagne']
    donnees['plantation_perenne_synthetise_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['culture'][['code', 'domaine_id']]
    right = donnees['domaine'][['campagne']]
    donnees['culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['plantation_perenne_synthetise_extanded'][['culture_code', 'campagne']].reset_index()
    right = donnees['culture_extanded'].reset_index().rename(columns={'code' : 'culture_code', 'id' : 'culture_id'})
    final = pd.merge(left, right, on=['culture_code', 'campagne'], how='inner')[['id', 'culture_id']]

    return final.set_index('id')

def restructuration_composant_culture_concerne_intervention_synthetise(donnees):
    """
        fonction permettant d'obtenir, pour chaque composant de culture concerné par une intervention en synthétisé
        un culture_id plutôt qu'un culture_code
    """
    donnees = donnees.copy()


    donnees['composant_culture_concerne_intervention_synthetise'] = \
        donnees['composant_culture_concerne_intervention_synthetise'].set_index('id')
    donnees['intervention_synthetise_agrege'] = donnees['intervention_synthetise_agrege'].set_index('id')
    donnees['culture'] = donnees['culture'].set_index('id')
    donnees['domaine'] = donnees['domaine'].set_index('id')
    donnees['composant_culture'] = donnees['composant_culture'].set_index('id')

    left = donnees['composant_culture_concerne_intervention_synthetise'][['composant_culture_code', 'intervention_synthetise_id']]
    right = donnees['intervention_synthetise_agrege'][['domaine_id']]
    donnees['studied_extanded'] = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True, how='left')

    left = donnees['studied_extanded']
    right = donnees['domaine'][['campagne']]
    donnees['studied_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['composant_culture'][['code', 'culture_id']]
    right = donnees['culture'][['domaine_id']]
    donnees['composant_culture_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')


    left = donnees['composant_culture_extanded']
    right = donnees['domaine'][['campagne']]
    donnees['composant_culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    left = donnees['studied_extanded'][['composant_culture_code', 'campagne']].reset_index()
    right = donnees['composant_culture_extanded'].reset_index().rename(
        columns={'code' : 'composant_culture_code', 'id' : 'composant_culture_id'}
    )
    final = pd.merge(left, right, on=['composant_culture_code', 'campagne'], how='inner')[['id', 'composant_culture_id']]

    return final.set_index('id')


def restructuration_intervention_synthetise(donnees):
    """
        fonction permettant de remplacer le combinaison_outil_code par un combinaison_outil_id dans les intervention en synthétisé
    """
    donnees = donnees.copy()

    donnees['intervention_synthetise'] = donnees['intervention_synthetise'].set_index('id')
    donnees['connection_synthetise'] = donnees['connection_synthetise'].set_index('id')
    donnees['noeuds_synthetise'] = donnees['noeuds_synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    donnees['intervention_synthetise_agrege'] = donnees['intervention_synthetise_agrege'].set_index('id')
    donnees['combinaison_outil'] = donnees['combinaison_outil'].set_index('id')
    donnees['domaine'] = donnees['domaine'].set_index('id')

    # obtention de la campagne informations grace au dataframe agrégé. 
    left = donnees['intervention_synthetise'][['combinaison_outil_code']]
    right = donnees['intervention_synthetise_agrege'][['sdc_campagne']]
    donnees['intervention_synthetise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # obtention des infos sur toutes les combinaisons d'outils
    left = donnees['combinaison_outil'][['code', 'domaine_id']]
    right = donnees['domaine'][['campagne']]
    donnees['combinaison_outil_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    # on fusionne les deux en s'assurant d'avoir à la fois la bonne campagne et le bon combinaison_outil_code.
    left = donnees['intervention_synthetise_extanded'].reset_index()
    right = donnees['combinaison_outil_extanded'].reset_index().rename(columns={'id' : 'combinaison_outil_id'})
    donnees['intervention_synthetise_extanded'] = pd.merge(
        left, 
        right, 
        left_on=['combinaison_outil_code', 'sdc_campagne'], right_on=['code', 'campagne'], how='inner'
    ).set_index('id')

    # Étape nécessaire (cf ticket : TODO : remplir le nom du ticket)
    donnees['intervention_synthetise_extanded'] = donnees['intervention_synthetise_extanded'].reset_index(
    ).drop_duplicates(subset=['id']).set_index('id')

    # on ne sélectionne que les données souhaitées 
    return donnees['intervention_synthetise_extanded'][['combinaison_outil_id']]

def restructuration_recolte_rendement_prix(donnees):
    """
        fonction permettant de remplacer le composant_culture_code dans la table recolte_rendement_prix par un composant_culture_id,
    """
    donnees = donnees.copy()

    donnees['action_realise_agrege'] = donnees['action_realise_agrege'].set_index('id')
    donnees['action_synthetise_agrege'] = donnees['action_synthetise_agrege'].set_index('id')
    donnees['recolte_rendement_prix'] = donnees['recolte_rendement_prix'].set_index('id')
    donnees['composant_culture'] = donnees['composant_culture'].set_index('id')
    donnees['domaine'] = donnees['domaine'].set_index('id')
    donnees['culture'] = donnees['culture'].set_index('id')

    # obtention d'un seul dataframe pour toutes les actions agrégées
    donnees['action_agrege'] = pd.concat([donnees['action_realise_agrege'], donnees['action_synthetise_agrege']])

    # on récupère la campagne sur laquelle a lieu l'action
    left = donnees['recolte_rendement_prix'][['action_id', 'composant_culture_code']]
    right = donnees['action_agrege'][['sdc_campagne']].rename(columns={'sdc_campagne' : 'campagne'})
    donnees['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='action_id', right_index=True, how='left')

    # on récupère la campagne associé à chaque composant de culture
    left = donnees['composant_culture'][['culture_id', 'code']].rename(columns={'code' : 'composant_culture_code'})
    right = donnees['culture'][['domaine_id']]
    donnees['composant_culture_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    left = donnees['composant_culture_extanded']
    right = donnees['domaine'][['campagne']]
    donnees['composant_culture_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    # attention, certains composants cultures sont associés à une culture absente du df['culture'] --> il s'agit des cultures appartenant à un domaine inactivé.
    donnees['composant_culture_extanded'] = donnees['composant_culture_extanded'].dropna()

    # à présent, on a toutes les informations de l'intervention de récolte et des composants de culture pour choisir le bon composant_culture_id parmis ceux disponibles avec le code
    left = donnees['recolte_rendement_prix_extanded'].reset_index()
    right = donnees['composant_culture_extanded'].reset_index().rename(columns={'id' : 'composant_culture_id'})
    final = pd.merge(left, right, on=['composant_culture_code', 'campagne'], how='inner').set_index('id')

    return final[['composant_culture_id']]

def restructuration_noeuds_realise(donnees):
    """
        fonction permettant d'obtenir pour un noeuds en réalisé, le noeuds précédent si celui-ci existe. 
        C'est à dire qu'on obtient le noeuds précédent si il existe sur la même zone, ou qu'on obtient le 
        dernier noeuds de la zone précédent si le noeuds et le premier et que la zone précédente 
        (liée avec le zone_code) existe.
    """
    donnees = donnees.copy()
    donnees['noeuds_realise'] = donnees['noeuds_realise'].set_index('id')
    donnees['zone'] = donnees['zone'].set_index('id')

    # ÉTAPE 1 : 

    # On considère tous les noeuds pour lesquels on a d'autres noeuds dans la zone et qui ne sont pas les premiers dans leurs zones
    # On leur affecte en précédent le noeuds au rang maximal situé juste avant eux.

    donnees['noeuds_realise_extanded'] = donnees['noeuds_realise'].reset_index().rename(columns={'id' : 'noeuds_realise_id'})

    # Auto-jointure sur le DataFrame
    merged_df = donnees['noeuds_realise_extanded'].merge(donnees['noeuds_realise_extanded'], on='zone_id', suffixes=('', '_comp'))

    # Filtrage des paires où le rang du nœud comparé est inférieur
    condition = (merged_df['rang_comp'] < merged_df['rang']) & (merged_df['noeuds_realise_id'] != merged_df['noeuds_realise_id_comp'])

    filtered_df = merged_df[condition]

    # Sélectionner le rang_id le plus élevé parmi les nœuds ayant un rang inférieur
    idx_max = filtered_df.groupby('noeuds_realise_id')['rang_comp'].idxmax()
    max_rang_df = filtered_df.loc[idx_max, ['noeuds_realise_id', 'noeuds_realise_id_comp', 'rang_comp']].rename(
        columns={'noeuds_realise_id_comp' : 'precedent_noeuds_realise_id'}
    )

    # Comptage des nœuds répondant à la condition pour chaque nœud
    count = filtered_df.groupby('noeuds_realise_id').size().reset_index(name='nb_noeuds_inferieurs')

    # Fusionner avec le DataFrame original pour obtenir le résultat final
    df_etape_1 = donnees['noeuds_realise_extanded'].merge(max_rang_df, on='noeuds_realise_id', how='left')
    df_etape_1 = df_etape_1.merge(count, on='noeuds_realise_id', how='left')
    df_etape_1['nb_noeuds_inferieurs']= df_etape_1['nb_noeuds_inferieurs'].fillna(0)

    df_etape_1_save = df_etape_1.set_index('noeuds_realise_id')

    # derniers nettoyages 
    df_etape_1 = df_etape_1_save.loc[~df_etape_1_save['precedent_noeuds_realise_id'].isna()][['precedent_noeuds_realise_id']]


    # ÉTAPE 2 : 

    # On considère tous les autres noeuds, ceux pour lesquelles il faut aller chercher si possible le dernier noeud du zone_id précédent dans le zone_code.

    # 1ère étape : affectation de la zone_id sur la campagne d'avant si possible
    left = donnees['noeuds_realise'].loc[~donnees['noeuds_realise'].index.isin(list(df_etape_1.index))]
    right = donnees['zone'][['code', 'campagne']].rename(columns={'campagne' : 'campagne_courante'})
    merge = pd.merge(left, right, left_on='zone_id', right_index=True)

    left = merge.reset_index()
    right = donnees['zone'][['campagne', 'code']].reset_index().rename(columns={'id' : 'zone_id_before', 'campagne' : 'campagne_before'})
    merge = pd.merge(left, right, left_on='code', right_on='code', how='left')

    zone_before = (merge['campagne_courante'] == merge['campagne_before'] + 1)
    zone_before_idx = zone_before[zone_before].index

    donnees['noeuds_realise_extanded'] = merge.loc[zone_before_idx].set_index('id')

    # 2ème étape : affectation aux zones du dernier noeuds
    left = donnees['noeuds_realise'][['rang', 'zone_id']] 
    right = donnees['zone']
    merge = pd.merge(left, right, left_on='zone_id', right_index=True, how='left')

    idx_rang_max = merge.groupby('zone_id')['rang'].idxmax()

    left = donnees['zone']
    right = donnees['noeuds_realise'].loc[idx_rang_max.values][['zone_id']].reset_index().rename(columns={'id' : 'precedent_noeuds_realise_id'})
    donnees['zone_extanded'] = pd.merge(left, right, left_index=True, right_on='zone_id', how='left').set_index('zone_id')[['precedent_noeuds_realise_id']]

    # 3 ème étape fusion des informations
    left = donnees['noeuds_realise_extanded']
    left.index = left.index.rename('noeuds_realise_id')
    right = donnees['zone_extanded']
    df_etape_2 = pd.merge(left, right, left_on='zone_id_before', right_index=True, how='left') 

    # derniers nettoyages 
    df_etape_2 = df_etape_2.loc[~df_etape_2['precedent_noeuds_realise_id'].isna()][['precedent_noeuds_realise_id']]

    final = pd.concat([df_etape_1, df_etape_2])

    final.index.rename('id', inplace=True)

    return final

