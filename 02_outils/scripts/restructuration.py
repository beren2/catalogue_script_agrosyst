"""
	Regroupe les fonctions qui constituent en des restructuration des fichiers initiaux afin de faciliter leur utilisation
"""
import pandas as pd

def restructuration_noeuds_synthetise(donnees):
    """
    Permet d'obtenir un DataFrame contenant la culture_id associé à un noeuds dans le mode de saisie synthétisé.

    Cette fonction, comme l'ensemble des fonctions de restructuration, 
    permet d'éviter à avoir à travailler avec les codes (qui permettent de lier des entités millésimées).

    La procédure est de charger la campagne du domaine sur laquelle est déclarée le noeuds synthétisé
    et d'aller chercher le culture_id correspondant à cette campagne et au culture_code pointé par le noeuds
    synthétisé.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'synthetise' : Systèmes synthétisés.
            - 'sdc' : Systèmes de cultures.
            - 'noeuds_synthetise' : Noeuds de rotation en synthétisé. 
            - 'culture' : Culture
            - 'domaine' : Domaine.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant, pour chaque noeuds_synthetise, le culture_id mobilisé sur ce noeuds.
            - `id` : Identifiant du noeuds synthétisé.
            - `culture_id` : identifiant de la culture déclaré sur le noeuds

    Exemple d'utilisation :
        donnees = {
            'synthetise': pd.DataFrame(...),
            'sdc': pd.DataFrame(...),
            'noeuds_synhtetise': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'domaine': pd.DataFrame(...)
        }
        result = restructuration_noeuds_synthetise(donnees)
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

    # fusion des informations une fois qu'on a le culture_code ET la campagne des deux côtés.
    left = donnees['noeuds_synthetise_extanded']
    right = donnees['culture_extanded'].reset_index()[['id', 'code', 'campagne']].rename(columns={'id' : 'culture_id'})
    donnees['noeuds_synthetise_restructure'] = pd.merge(left, right, left_on=['culture_code', 'campagne'], right_on=['code', 'campagne'])

    return donnees['noeuds_synthetise_restructure'].set_index('id')[['culture_id']]


def restructuration_connection_synthetise(donnees):
    """
    Permet d'obtenir un DataFrame contenant le culture_intermediaire_id associé à une connexion dans le mode de saisie synthétisé.

    Cette fonction, comme l'ensemble des fonctions de restructuration, 
    permet d'éviter à avoir à travailler avec les codes (qui permettent de lier des entités millésimées).

    La procédure est de charger la campagne du domaine sur laquelle est déclarée la connexion synthétisé
    et d'aller chercher le culture_id correspondant à cette campagne et au culture_code pointé par la connexion
    synthétisé.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'synthetise' : Systèmes synthétisés.
            - 'sdc' : Systèmes de cultures.
            - 'connection_synthetise' : Noeuds de rotation en synthétisé. 
            - 'culture' : Culture
            - 'domaine' : Domaine.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant, pour chaque noeuds_synthetise, le culture_id mobilisé sur ce noeuds.
            - `id` : Identifiant de la connexion synthétisé
            - `culture_intermediaire_id` : identifiant de la culture intermediaire déclarée sur la connection
    Note :
        Attention, une connexion qui ne possède pas de culture intermediaire sera absente du dataframe final. 

    Exemple d'utilisation :
        donnees = {
            'synthetise': pd.DataFrame(...),
            'sdc': pd.DataFrame(...),
            'noeuds_synhtetise': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'domaine': pd.DataFrame(...)
        }
        result = restructuration_noeuds_synthetise(donnees)

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

    # fusion des informations une fois qu'on a le culture_code ET la campagne des deux côtés.
    left = donnees['connection_synthetise_extanded'].reset_index()
    right = donnees['culture_extanded'].reset_index()[['id', 'code', 'campagne']].rename(columns={'id' : 'culture_intermediaire_id'})
    donnees['connection_synthetise_restructure'] = pd.merge(left, right, left_on=['culture_intermediaire_code', 'campagne'], right_on=['code', 'campagne'])

    return donnees['connection_synthetise_restructure'].set_index('id')[['culture_intermediaire_id']]


def restructuration_plantation_perenne_synthetise(donnees):
    """
    Permet d'obtenir un DataFrame contenant la culture_id associé à une plantation perenne dans le mode de saisie synthétisé.

    Cette fonction, comme l'ensemble des fonctions de restructuration, 
    permet d'éviter à avoir à travailler avec les codes (qui permettent de lier des entités millésimées).

    La procédure est de charger la campagne du domaine sur laquelle est déclarée la plantation perenne
    et d'aller chercher le culture_id correspondant à cette campagne et au culture_code pointé par la plantation perenne.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires :
            - 'synthetise' : Systèmes synthétisés.
            - 'sdc' : Systèmes de cultures.
            - 'plantation_perenne_synthetise' : Noeuds de rotation en synthétisé. 
            - 'culture' : Culture
            - 'domaine' : Domaine.
            - 'dispositif' : Dispositif.

    Returns:
        pd.DataFrame:
            Un DataFrame contenant, pour chaque plantation_perenne synthétisé, le culture_id mobilisé.
            - `id` : Identifiant de la plantation perenne synthétisé
            - `culture_id` : identifiant de la culture déclaré sur la plantation

    Exemple d'utilisation :
        donnees = {
            'synthetise': pd.DataFrame(...),
            'sdc': pd.DataFrame(...),
            'noeuds_synhtetise': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'domaine': pd.DataFrame(...)
        }
        result = restructuration_noeuds_synthetise(donnees)
    """
    donnees = donnees.copy()
    donnees['plantation_perenne_synthetise'] = donnees['plantation_perenne_synthetise'].set_index('id')
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    donnees['sdc'] = donnees['sdc'].set_index('id')
    donnees['dispositif'] = donnees['dispositif'].set_index('id')
    donnees['domaine'] = donnees['domaine'].set_index('id')
    donnees['culture'] = donnees['culture'].set_index('id')
    
    # obtention du culture_code pour la plantation_perenne
    left = donnees['plantation_perenne_synthetise'][['synthetise_id', 'culture_code']]
    right = donnees['synthetise'][['sdc_id']]
    donnees['plantation_perenne_synthetise_extanded'] = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    # obtention de la campagne de la plantation perenne
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

    # fusion des informations une fois qu'on a le culture_code ET la campagne des deux côtés.
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

    left = donnees['studied_extanded'].dropna(subset=['domaine_id'])
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
    donnees['synthetise'] = donnees['synthetise'].set_index('id')
    donnees['intervention_synthetise_agrege'] = donnees['intervention_synthetise_agrege'].set_index('id')
    donnees['combinaison_outil'] = donnees['combinaison_outil'].set_index('id')
    donnees['domaine'] = donnees['domaine'].set_index('id')

    # obtention de la campagne du sdc
    left = donnees['intervention_synthetise'][['combinaison_outil_code']]
    right = donnees['intervention_synthetise_agrege'][['sdc_campagne','synthetise_id']]
    donnees['intervention_synthetise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # obtention de la campagne du domaine auquel sont attachees les combinaisons d'outils
    left = donnees['combinaison_outil'][['code', 'domaine_id']]
    right = donnees['domaine'][['campagne']]
    donnees['combinaison_outil_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    # on fusionne les deux en s'assurant d'avoir à la fois la bonne campagne et le bon combinaison_outil_code.
    left = donnees['intervention_synthetise_extanded'].reset_index()
    right = donnees['combinaison_outil_extanded'].reset_index().rename(columns={'id' : 'combinaison_outil_id'})
    intervention_synthetise_extanded_1 = pd.merge(
        left, 
        right, 
        left_on=['combinaison_outil_code', 'sdc_campagne'], right_on=['code', 'campagne'], how='inner')

    # Cas manquants : combinaisons outils disponibles d'un meme code qui ne matchent pas avec la campagne du sdc
    # ancienne saisie : les combinaisons d outils proposees sont celles des campagnes du synthetisee
    # ex : campagnes de outils possible : 2022,2023 ; campagne sdc 2021; campagnes synthetise 2020,2021,2022
    # on prend la combinaison d outils de la campagne la plus recente pour un meme code

    # obtention de la serie de campagne du synthetise
    left = donnees['intervention_synthetise_extanded'].reset_index()
    right = donnees['synthetise'][['campagnes']].rename(columns={'campagnes' : 'campagnes_synthetise'})
    right['campagnes_synthetise'] = right['campagnes_synthetise'].str.split(', ')
    donnees['intervention_synthetise_extanded'] = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    # Join les campagnes possibles des combinaisons outils et de campagnes_synthetise
    missing = donnees['intervention_synthetise_extanded'][~donnees['intervention_synthetise_extanded']['id'].isin(intervention_synthetise_extanded_1['id'])]
    left = missing[~ missing['combinaison_outil_code'].isna()]
    right = donnees['combinaison_outil_extanded'].groupby('code')['campagne'].apply(list).reset_index().rename(columns={'code' : 'combinaison_outil_code', 'campagne' : 'domaine_campagne'})
    missing_extanded = pd.merge(left, right, on='combinaison_outil_code', how='left')

    missing_extanded['campagnes_synthetise'] = missing_extanded['campagnes_synthetise'].apply(lambda d: d if isinstance(d, list) else [])

    # on parcourt chaque ligne pour vérifier que les valeurs dans camapgnes synthétisé sont bien dans domaine_campagne (sinon, on laisse la ligne à [])
    missing_extanded['campagne_commune'] = missing_extanded.apply(
        lambda x: [value for value in x['campagnes_synthetise'] if int(value) in x['domaine_campagne']] if isinstance(x['domaine_campagne'], list)  else [],
        axis=1
    )

    missing_extanded['campagne_max'] = missing_extanded.apply(
        lambda x: int(max(x['campagne_commune'])) if len(x['campagne_commune']) > 0 else 0, 
        axis=1
    )

    left = missing_extanded
    right = donnees['combinaison_outil_extanded'].reset_index().rename(columns={'id' : 'combinaison_outil_id'})
    intervention_synthetise_extanded_2 = pd.merge(
        left, 
        right, 
        left_on=['combinaison_outil_code', 'campagne_max'], right_on=['code', 'campagne'], how='inner')[intervention_synthetise_extanded_1.columns]

    intervention_synthetise_extanded_1 = pd.concat([intervention_synthetise_extanded_1,intervention_synthetise_extanded_2])

    # Il reste encore des Cas manquants : 
    # ex : campagnes de outils possible : 2015 ; campagnes synthetise 2012, campagne sdc 2012
    # on prend la combinaison d outils de la campagne la plus recente pour un meme code
    
    comboutils_maxcampagne = donnees['combinaison_outil_extanded'].groupby('code')['campagne'].max()
    
    left = donnees['intervention_synthetise_extanded'][~donnees['intervention_synthetise_extanded']['id'].isin(intervention_synthetise_extanded_1['id'])]
    right = pd.merge(donnees['combinaison_outil_extanded'].reset_index(), comboutils_maxcampagne, 
                    on=['code', 'campagne'], how='inner').rename(columns={'id' : 'combinaison_outil_id'})
    
    intervention_synthetise_extanded_3 = pd.merge(
        left, 
        right, 
        left_on=['combinaison_outil_code'], right_on=['code'], how='inner')[intervention_synthetise_extanded_1.columns]

    donnees['intervention_synthetise_extanded'] = pd.concat([intervention_synthetise_extanded_1,intervention_synthetise_extanded_3])
       
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
        dernier noeuds de la zone précédent si le noeuds est le premier et que la zone précédente 
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


# def restructuration_noeuds_realise_BIS(donnees):
#     """
#         fonction permettant d'obtenir pour un noeuds en réalisé, le noeuds précédent si celui-ci existe. 
#         C'est à dire qu'on obtient le noeuds précédent si il existe sur la même zone, ou qu'on obtient le 
#         dernier noeuds de la zone précédent si le noeuds est le premier et que la zone précédente 
#         (liée avec le zone_code) existe. LIEN ENTRE PARCELLES ET ZONES
#     """
#     donnees = donnees.copy()
#     node = donnees['noeuds_realise'].rename(columns={
#         'id':'noeud_realise_id'})
#     zone = donnees['zone'][['id','code','nom','campagne','surface','parcelle_id']].rename(columns={
#         'id':'zone_id',
#         'code':'zone_code',
#         'nom':'zone_nom',
#         'surface':'zone_surface'})
#     parcelle = donnees['parcelle'][['id','code','nom','surface','sdc_id']].rename(
#         columns={ # ajout 'campagne' 'domaine_id' ?
#         'id':'parcelle_id',
#         'code':'parcelle_code',
#         'nom':'parcelle_nom',
#         'surface':'parcelle_surface'})
#     sdc = donnees['sdc'][['id','code','nom','code_dephy']].rename(columns={ # ajout 'campagne' ?
#         'id':'sdc_id',
#         'code':'sdc_code',
#         'nom':'sdc_nom'})
#     rest_node = restructuration_noeuds_realise(donnees[['noeuds_realise','zone']])
#     rest_node = rest_node.rename(columns={'id':'noeud_realise_id'})
#     # Besoin de donnees['intervention_realise']
#     list_zone_with_at_least_one_interv = node.loc[node['noeud_realise_id'].isin(set(donnees['intervention_realise'][['noeud_realise_id']])), 'zone_id'].unique()



#     zone = zone.loc[zone['zone_id'].isin(list_zone_with_at_least_one_interv)]
#     # Attention inner merge pour n'avoir que les noeud de la sélection des zones
#     df = node.merge(zone, on='zone_id', how='inner')
#     df = df.merge(parcelle, on='parcelle_id', how='left')
#     df = df.merge(sdc, on='sdc_id', how='left')
#     return df